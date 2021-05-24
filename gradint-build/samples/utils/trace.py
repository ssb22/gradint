#!/usr/bin/env python2

# trace.py: script to generate raytraced animations of Gradint lessons
# Version 1.3 (c) 2018-19,2021 Silas S. Brown.  License: GPL

#  The Disney Pixar film "Inside Out" (2015) represented
#  memories as spheres.  I don't have their CGI models, but
#  we can do spheres in POV-Ray and I believe that idea is
#  simple enough to be in the public domain (especially if
#  NOT done like Pixar did it) - hopefully this might show
#  some people how Gradint's method is supposed to work
#  (especially if they've seen the Inside Out film).

# This script generates the POV-Ray scenes from a lesson.
# Gradint is run normally (passing any extra command-line arguments on,
# must include outputFile so audio can be included in the animation)
# and then the animation is written to /tmp/gradint.mp4.

# Optionally add a static image representing each word (image will be
# placed onto the spheres, and projected onto the back wall
# when that word is being recalled)
# e.g. word1_en.wav, word1_zh.wav, word1.jpg
# (or png or gif).

# Optionally add an mp4 video of a word in a particular language
# e.g. word1_en.mp4 (probably best synchronised to word1_en.wav),
# can also do this for commentsToAdd and orderlessCommentsToAdd files

# Requires POV-Ray, ffmpeg, and the Python packages vapory
# and futures (use sudo pip install futures vapory) -
# futures is used to run multiple instances of POV-Ray on
# multi-core machines.

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--fps",default=15,dest="theFPS",
                  help="Frames per second (10 is insufficient for fast movement, so recommend at least 15)")
parser.add_option("--res",default=480,
                  help="Y-resolution: 240=NTSC VCD, 288=PAL VCD, 480=DVD, 720=Standard HD (Blu-Ray), 1080=Full HD (Blu-Ray)")
parser.add_option("--translucent",action="store_true",default=False,dest="translucent_spheres_when_picture_visible",
                  help="Translucent spheres when picture visible (slows down rendering but is better quality)")
parser.add_option("--minutes",default=0,
                  help="Maximum number of minutes to render (0 = unlimited, the default; can limit for test runs)")
parser.add_option("--quality",default=9,dest="povray_quality",
                  help="POVRay quality setting, default 9: 1=ambient light only, 2=lighting, 4,5=shadows, 8=reflections 9-11=radiosity etc")

options, args = parser.parse_args()
globals().update(options.__dict__)
theFPS,res,minutes,povray_quality = int(theFPS),int(res),int(minutes),int(povray_quality)

if res in [240,288]:
    width_height_antialias = (352,res,0.3) # VCD.  antialias=None doesn't look very good at 300x200, cld try it at higher resolutions (goes to the +A param, PovRay default is 0.3 if -A specified without param; supersample (default 9 rays) if colour differs from neighbours by this amount)
elif res==480: width_height_antialias = (640,480,0.001) # 480p (DVD)
elif res==720: width_height_antialias = (1280,720,None) # Standard HD (Blu-Ray)
elif res==1920: width_height_antialias = (1920,1080,None) # Full HD (Blu-Ray)
else: raise Exception("Unknown vertical resolution specified: "+repr(res))
debug_frame_limit = minutes * theFPS * 60

import sys,os,traceback
oldName = __name__ ; from vapory import * ; __name__ = oldName
from concurrent.futures import ProcessPoolExecutor

assert os.path.exists("gradint.py"), "You must move trace.py to the top-level Gradint directory and run it from there"
sys.argv = [sys.argv[0]]+args
import gradint
assert gradint.outputFile, "You must run trace.py with gradint parameters that include outputFile"

try: xrange
except: xrange = range
S,B = gradint.S,gradint.B

class MovableParam:
    def __init__(self): self.fixed = []
    def fixAt(self,t,value):
        while any(x[0]==t and not x[1]==value for x in self.fixed): t += 0.2
        self.fixed.append((t,value))
    def getPos(self,t):
        assert self.fixed, "Should fixAt before getPos"
        self.fixed.sort()
        for i in xrange(len(self.fixed)):
            if self.fixed[i][0] >= t:
                if i: # interpolate
                    if self.fixed[i-1][1]==None: return None
                    duration = self.fixed[i][0]-self.fixed[i-1][0]
                    progress = t-self.fixed[i-1][0]
                    return (self.fixed[i][1]*progress + self.fixed[i-1][1]*(duration-progress))*1.0/duration
                else: return self.fixed[i][1] # start position
        return self.fixed[-1][1]

class MovablePos:
    def __init__(self): self.x,self.y,self.z = MovableParam(),MovableParam(),MovableParam()
    def fixAt(self,t,*args):
        if args[0]==None: x=y=z=None
        else: x,y,z = args
        self.x.fixAt(t,x),self.y.fixAt(t,y),self.z.fixAt(t,z)
    def getPos(self,t):
        r=(self.x.getPos(t),self.y.getPos(t),self.z.getPos(t))
        if r==(None,None,None): return None
        else: return r

SceneObjects = set()

class MovableSphere(MovablePos):
    def __init__(self,radius=0.5,colour="prompt",imageFilename=None):
        MovablePos.__init__(self)
        self.colour = colour
        self.imageFilename = imageFilename
        self.radius = MovableParam()
        self.radius.fixAt(-1,radius)
        SceneObjects.add(self)
    # fixAt(t,x,y,z) inherited
    def obj(self,t):
        pos = self.getPos(t)
        if not pos: return # not in scene at this time
        r = self.radius.getPos(t)
        if self.imageFilename:
            if translucent_spheres_when_picture_visible and bkgScrFade.getPos(t) < 1: transmittence = 0.5
            else: transmittence = 0.3
            if r > 0.5: img = wallPic(t) # we're the one that's playing: 'back-copy' video frame if any
            else: img = None
            if not img: img = self.imageFilename
            return Sphere(list(pos),r,colour(self.colour,t),Texture(Pigment(ImageMap('"'+S(img)+'"',"once","interpolate 2","transmit all "+str(transmittence)),'scale',[1.5*r,1.5*r,1],'translate',list(pos),'translate',[-.75*r,-.75*r,0])))
        else: return Sphere(list(pos),r,colour(self.colour,t))

class ObjCollection:
    def __init__(self): self.objs = set()
    def add(self,obj,dx,dy,dz): self.objs.add((obj,dx,dy,dz))
    def get(self,dx,dy,dz): # should be small so:
        for o,ddx,ddy,ddz in self.objs:
            if (ddx,ddy,ddz) == (dx,dy,dz): return o
    def fixAt(self,t,*args):
        if args[0]==None: x=y=z=None
        else: x,y,z = args
        for obj,dx,dy,dz in self.objs:
            if args==[None]: obj.fixAt(t,None,None,None)
            else: obj.fixAt(t,x+dx,y+dy,z+dz)

eventTrackers = {}
def EventTracker(rowNo,imageFilename=None):
    if not rowNo in eventTrackers:
        eventTrackers[rowNo] = ObjCollection()
        eventTrackers[rowNo].add(MovableSphere(1,"l1",imageFilename),-1,0,0)
        eventTrackers[rowNo].add(MovableSphere(1,"l2",imageFilename),+1,0,0)
        eventTrackers[rowNo].numRepeats = 0
    return eventTrackers[rowNo]
rCache = {}
def repeatSphere(rowNo,numRepeats=0):
    if not (rowNo,numRepeats) in rCache:
        rCache[(rowNo,numRepeats)] = MovableSphere(0.1,"prompt")
    return rCache[(rowNo,numRepeats)]
def addRepeat(rowNo,t=0,length=0):
    et = EventTracker(rowNo)
    rpt = repeatSphere(rowNo,et.numRepeats)
    if length:
        rpt.fixAt(-1,None) # not exist yet (to save a tiny bit of POVRay computation)
        rpt.fixAt(t-1,4*rowNo+1,0,61) # behind far wall
        rpt.fixAt(t,4*rowNo-1,0,0) # ready to be 'batted'
        et.fixAt(t,4*rowNo,0,10) # we're at bottom
        camera_lookAt.fixAt(t,4*rowNo,0,10)
        camera_lookAt.fixAt(t+length,4*rowNo,10,10)
        camera_position.x.fixAt(t+length/2.0,4*rowNo)
        # careful with Y : try to avoid sudden vertical motion between 2 sequences
        camera_position.y.fixAt(t+length*.2,1)
        camera_position.y.fixAt(t+length*.8,4)
        camera_position.z.fixAt(t+length*.2,-10)
        camera_position.z.fixAt(t+length*.8,-5)
    et.add(rpt,0,1+0.2*et.numRepeats,0) # from now on we keep this marker
    et.fixAt(t+length,4*rowNo,10,10) # at end of repeat (or at t=0) we're at top, and the repeat marker is in place
    et.numRepeats += 1

camera_position = MovablePos()
camera_lookAt = MovablePos()
def cam(t): return Camera('location',list(camera_position.getPos(t)),'look_at',list(camera_lookAt.getPos(t)))
def lights(t): return [LightSource([camera_position.x.getPos(t)+10, 15, -20], [1.3, 1.3, 1.3])]

background_screen = [] # (startTime,endTime,picture)
background_screen_size = 50
bkgScrFade = MovableParam() ; bkgScrFade.fixAt(-1,1)
bkgScrX = MovableParam()
def wallPic(t):
    if bkgScrFade.getPos(t) == 1: return # no picture if we're faded out
    for st,et,pic in background_screen:
        if st <= t <= et:
            if B(pic).endswith(B(os.extsep+"mp4")):
                # need to take single frame from time t-st
                out = B(pic)[:-4]+B("-"+str(t-st)+os.extsep+"jpg")
                if not os.path.exists(out): # (TODO: if its frame rate is low enough, we might already have the same frame even at a slightly different t-st)
                    cmd = "ffmpeg -n -threads 1 -accurate_seek -ss "+str(t-st)+" -i "+S(pic)+" -vframes 1 -q:v 1 "+S(out)+" </dev/null >/dev/null"
                    print (cmd)
                    os.system(cmd)
                    if not os.path.exists(out):
                        # print ("ffmpeg FAIL: skipping picture")
                        continue # at t=et there might be a static image next
                return out
            else: return pic
        elif st > t: return
def wall(t):
    picToUse = wallPic(t)
    if picToUse: return [Plane([0, 0, 1], 60, Texture(Pigment('color', [1, 1, 1])), Texture(Pigment(ImageMap('"'+S(picToUse)+'"',"once","transmit all "+str(bkgScrFade.getPos(t))),'scale',[background_screen_size,background_screen_size,1],'translate',[bkgScrX.getPos(t)-background_screen_size/2,0,0])), Finish('ambient',0.9))]
    else: return [Plane([0, 0, 1], 60, Texture(Pigment('color', [1, 1, 1])), Finish('ambient',0.9))] # TODO: why does this look brighter than with ImageMap at transmit all 1.0 ?

ground = Plane( [0, 1, 0], -1, Texture( Pigment( 'color', [1, 1, 1]), Finish( 'phong', 0.1, 'reflection',0.4, 'metallic', 0.3))) # from vapory example

def colour(c,t=None):
    c = {"l1":[.8,1,.2],"l2":[.5,.5,.9],"prompt":[1,.6,.5]}[c] # TODO: better colours
    if translucent_spheres_when_picture_visible and not t==None and bkgScrFade.getPos(t) < 1: return Texture(Pigment('color',c,'filter',0.7))
    else: return Texture(Pigment('color',c))
def scene(t):
    """ Returns the scene at time 't' (in seconds) """
    return Scene(cam(t), lights(t) + wall(t) + [ground] + [o for o in [x.obj(t) for x in SceneObjects] if not o==None])

def Event_draw(self,startTime,rowNo,inRepeat): pass
gradint.Event.draw = Event_draw

def CompositeEvent_draw(self,startTime,rowNo,inRepeat):
  if self.eventList:
    t = startTime
    for i in self.eventList:
      i.draw(t,rowNo,True)
      t += i.length
    if inRepeat: return
    # Call addRepeat, but postpone the start until the
    # first loggable event, to reduce rapid camera mvt
    st0 = startTime
    for i in self.eventList:
      if i.makesSenseToLog(): break
      else: startTime += i.length
    if startTime==t: startTime = st0 # shouldn't happen
    addRepeat(rowNo,startTime,t-startTime)
gradint.CompositeEvent.draw=CompositeEvent_draw

def Event_colour(self,language):
    if self.makesSenseToLog():
      if language==gradint.firstLanguage: return "l1"
      else: return "l2"
    else: return "prompt"
gradint.Event.colour = Event_colour

def eDraw(startTime,length,rowNo,colour):
    minR = 0.5
    if colour in ["l1","l2"]:
        if colour=="l1": delta = -1
        else: delta = +1
        et = EventTracker(rowNo).get(delta,0,0)
        r = et.radius
        if hasattr(et,"imageFilename"):
            background_screen.append((startTime,startTime+length,et.imageFilename))
            bkgScrX.fixAt(startTime,4*rowNo)
            bkgScrX.fixAt(startTime+length,4*rowNo)
    else:
        r = repeatSphere(rowNo,EventTracker(rowNo).numRepeats).radius
        minR = 0.1
    maxR = min(max(length,minR*1.5),minR*3) # TODO: vary with event's volume, so cn see the syllables? (partials can do that anyway)
    r.fixAt(startTime,minR)
    r.fixAt(startTime+length,minR)
    if length/2.0 > 0.5:
        r.fixAt(startTime+0.5,maxR)
        # TODO: wobble in the middle?
        r.fixAt(startTime+length-0.5,maxR)
    else: r.fixAt(startTime+length/2.0,maxR)

def SampleEvent_draw(self,startTime,rowNo,inRepeat):
    if B(self.file).startswith(B(gradint.partialsDirectory)): l=B(self.file).split(B(os.sep))[1]
    else: l = gradint.languageof(self.file)
    eDraw(startTime,self.length,rowNo,self.colour(S(l)))
gradint.SampleEvent.draw = SampleEvent_draw
def SynthEvent_draw(self,startTime,rowNo,inRepeat): eDraw(startTime,self.length,rowNo,self.colour(self.language))
gradint.SynthEvent.draw = SynthEvent_draw

def runGradint():
  gradint.gluedListTracker=[]
  gradint.waitBeforeStart=0
  gradint.main()
  gradint.gluedListTracker.sort(key=lambda e:e[0].glue.length+e[0].glue.adjustment)
  duration = 0
  for l,row in zip(gradint.gluedListTracker,xrange(len(gradint.gluedListTracker))):
    def check_for_pictures():
     for gluedEvent in l:
      event = gluedEvent.event
      try: el=event.eventList
      except: el=[event]
      for j in el:
       try: el2=j.eventList
       except: el2=[j]
       for i in el2:
        if hasattr(i,"file") and B("_") in B(i.file):
         for imgExt in ["gif","png","jpeg","jpg"]:
          imageFilename = B(i.file)[:B(i.file).rindex(B("_"))]+B(os.extsep+imgExt) # TODO: we're assuming no _en etc in the image filename (projected onto both L1 and L2)
          if os.path.exists(imageFilename):
              return EventTracker(row,os.path.abspath(imageFilename))
    check_for_pictures()
    if hasattr(l[0],"timesDone"): timesDone = l[0].timesDone
    else: timesDone = 0
    for i in xrange(timesDone): addRepeat(row)
    glueStart = 0
    for i in l:
      i.event.draw(i.getEventStart(glueStart),row,False)
      glueStart = i.getAdjustedEnd(glueStart)
      duration = max(duration,glueStart)
  for t,e in gradint.lastLessonMade.events: # check for videos
      if hasattr(e,"file") and hasattr(e,"exactLen"):
          video = B(e.file)[:B(e.file).rindex(B(os.extsep))]+B(os.extsep+"mp4")
          if os.path.exists(video): # overwrite static image while playing
              background_screen.append((t,t+e.exactLen,os.path.abspath(video)))
  background_screen.sort()
  i = 0
  while i < len(background_screen)-1:
      if background_screen[i][1] > background_screen[i+1][1]: # overlap: we end after next one ends: insert a jump-back-to-us after
          background_screen.insert(i+2,(background_screen[i+1][1],background_screen[i][1],background_screen[i][2])) # restore old after new one ends
      if background_screen[i][1] > background_screen[i+1][0] and background_screen[i][0] < background_screen[i+1][0]: # overlap: we end after next one starts, but we start before it starts
          background_screen[i] = (background_screen[i][0],background_screen[i+1][0],background_screen[i][2]) # new one takes precedence
      if background_screen[i][0]==background_screen[i+1][0]: # equal start, but next one might be longer
          background_screen[i+1]=(background_screen[i][1],background_screen[i+1][1],background_screen[i+1][2])
      if background_screen[i][-1]==background_screen[i+1][-1] and background_screen[i][1]+5>=background_screen[i+1][0]:
          # turning off for 5 seconds or less, then turning back on again with the SAME image: might as well merge
          background_screen[i] = (background_screen[i][0],background_screen[i+1][1],background_screen[i][2])
          del background_screen[i+1]
      else: i += 1
  for i in xrange(len(background_screen)):
      startTime,endTime,img = background_screen[i]
      if i and startTime > background_screen[i-1][1] + 0.5:
          bkgScrFade.fixAt(startTime,1) # start faded out
      # else (less than 0.5sec between images) don't try to start faded out
      fadeOutTime = endTime
      if i<len(background_screen)-1:
          if endTime + 0.5 > background_screen[i+1][0]:
              fadeOutTime = None # as above (< 0.5sec between images)
          else: fadeOutTime = max(fadeOutTime,min(background_screen[i+1][0]-1,fadeOutTime+5))
          if not fadeOutTime == None:
              # don't move the screen during any extended fade-out:
              for ii in xrange(len(bkgScrX.fixed)):
                  if bkgScrX.fixed[ii][0]==endTime:
                      bkgScrX.fixed[ii]=((fadeOutTime,bkgScrX.fixed[ii][1]))
                      break
      if not fadeOutTime==None: bkgScrFade.fixAt(fadeOutTime,1)
      if endTime >= startTime+0.5:
          bkgScrFade.fixAt(startTime+0.5,0.3)
          bkgScrFade.fixAt(endTime-0.5,0.3)
      else:
          bkgScrFade.fixAt((startTime+endTime)/2.0,0.3)
  return duration

def tryFrame(f):
    frame,numFrames = f
    print ("Making frame "+str(frame)+" of "+str(numFrames))
    try:
        try: os.mkdir("/tmp/"+repr(frame)) # vapory writes a temp .pov file and does not change its name per process, so better be in a process-unique directory
        except: pass
        os.chdir("/tmp/"+repr(frame))
        scene(frame*1.0/theFPS).render(width=width_height_antialias[0], height=width_height_antialias[1], antialiasing=width_height_antialias[2], quality=povray_quality, outfile="/tmp/frame%05d.png" % frame)
        # TODO: TURN OFF JITTER with -J if using anti-aliasing in animations
        os.chdir("/tmp") ; os.system('rm -r '+repr(frame))
        return None
    except:
        if frame==0: raise
        traceback.print_exc()
        sys.stderr.write("Frame %d render error, will skip\n" % frame)
        return "cp /tmp/frame%05d.png /tmp/frame%05d.png" % (frame-1,frame)

def main():
    executor = ProcessPoolExecutor()
    duration = runGradint()
    numFrames = int(duration*theFPS)
    if debug_frame_limit: numFrames=min(numFrames,debug_frame_limit)
    # TODO: pickle all MovableParams so can do the rendering on a different machine than the one that makes the Gradint lesson?
    for c in list(executor.map(tryFrame,[(frame,numFrames) for frame in xrange(numFrames)]))+[
        "ffmpeg -nostdin -y -framerate "+repr(theFPS)+" -i /tmp/frame%05d.png -i "+gradint.outputFile+" -movflags faststart -pix_fmt yuv420p /tmp/gradint.mp4 && if test -d /Volumes; then open /tmp/gradint.mp4; fi" #  (could alternatively run with -vcodec huffyuv /tmp/gradint.avi for lossless, insead of --movflags etc, but will get over 6 gig and may get A/V desync problems in mplayer/VLC that -delay doesn't fix, however -b:v 1000k seems to look OK; for WeChat etc you need to recode to h.264, and for HTML 5 video need recode to WebM (but ffmpeg -c:v libvpx no good if not compiled with support for those libraries; may hv to convert on another machine i.e. ffmpeg -i gradint.mp4 -vf scale=320:240 -c:v libvpx -b:v 500k gradint.webm))
        ]:
        if c: # patch up skipped frames, then run ffmpeg
            print (c) ; os.system(c)
    for f in xrange(numFrames): os.remove("/tmp/frame%05d.png" % f) # wildcard from command line could get 'argument list too long' on BSD etc
if __name__=="__main__": main()
else: print (__name__)
