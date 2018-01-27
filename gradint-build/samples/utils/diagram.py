
# diagram.py: script to generate diagrams of gradint lessons
# (C) 2008 Silas S. Brown.  License: GPL

# Gradint is run normally (passing any command-line arguments on)
# and then a diagram of the lesson it made is written to diagram.svg

# you can get .ps by doing: inkscape -p '> diagram.ps' diagram.svg

pixelsPerSec = 1 # initially, can be adjusted by minWidth/maxWidth
rowHeight = 20 # initially, can be adjusted by minHeight/maxHeight
maxWidth = maxHeight = minWidth = minHeight = 0 # for no limit
# minWidth = 400 ; maxWidth = 600
minHeight = 200 ; maxHeight = 400

import gradint
import math,os

# map xrange to range if it doesn't exist (Python 3)
try: xrange
except: xrange = range

min_num_secs_before_row_reuse = 25 # to make the diagram clearer

#svg=os.popen("gzip -9 > diagram.svgz","w") # TODO does this still get broken pipes ?
svg=open("diagram.svg","w") # ** TODO choose either/or ?
# TODO: need to convert to PNG etc for IE

svg.write("""<?xml version="1.0"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n""")

def str2dp(f): return "%.2f" % float(f)

def moveTo(x,y):
    global svgCurPos
    svgCurPos=x,y
def lineTo(x,y):
    global svgCurPos
    svg.write('<line x1="'+str2dp(svgCurPos[0])+'" y1="'+str2dp(svgCurPos[1]))
    svgCurPos=x,y
    svg.write('" x2="'+str2dp(svgCurPos[0])+'" y2="'+str2dp(svgCurPos[1])+'" stroke-width="1" />\n')
def rectangle(x,y,width,height,colour="white"):
    if colour=="white": stroke="black"
    else: stroke=colour
    svg.write('<rect x="'+str2dp(x)+'" y="'+str2dp(y)+'" width="'+str2dp(width)+'" height="'+str2dp(height)+'" style="stroke:'+stroke+';stroke-width:1px; fill:'+colour+';" />\n')

def Event_draw(self,startTime,pixelsPerSec,topY,height): pass
gradint.Event.draw = Event_draw

def CompositeEvent_draw(self,startTime,pixelsPerSec,topY,height):
    if len(self.eventList) > 1:
        rectangle(startTime*pixelsPerSec,topY,self.length*pixelsPerSec,height)
        topY += height*0.1
        height *= 0.8
    for i in self.eventList:
      i.draw(startTime,pixelsPerSec,topY,height)
      startTime += i.length
gradint.CompositeEvent.draw=CompositeEvent_draw

def Event_colour(self,language):
    if self.makesSenseToLog():
      if language==gradint.firstLanguage: return "yellow" # TODO: 2nd to 3rd lang etc?
      else: return "green"
    else: return "grey" # prompts
gradint.Event.colour = Event_colour

def SampleEvent_draw(self,startTime,pixelsPerSec,topY,height):
    rectangle(startTime*pixelsPerSec,topY,self.length*pixelsPerSec,height,self.colour(gradint.languageof(self.file)))
gradint.SampleEvent.draw = SampleEvent_draw
def SynthEvent_draw(self,startTime,pixelsPerSec,topY,height):
    rectangle(startTime*pixelsPerSec,topY,self.length*pixelsPerSec,height,self.colour(self.language))
gradint.SynthEvent.draw = SynthEvent_draw

def drawCoils(leftX,topY,width,height,springLen):
  assert springLen >= width
  if springLen==width: deviation,nCoils=0,0
  else:
    t=math.sqrt(springLen*springLen-width*width)/4
    deviation=height/2.0 # maximum
    nCoils=int(math.ceil(t/deviation))
    deviation=t/nCoils
  midY=topY+height/2.0
  svg.write('<g stroke="purple">') # colour for coils
  moveTo(leftX,midY)
  for coil in xrange(nCoils):
    lineTo(leftX+(coil+.25)*width/nCoils,midY-deviation)
    lineTo(leftX+(coil+.75)*width/nCoils,midY+deviation)
  lineTo(leftX+width,midY)
  svg.write('</g>')

def drawGlue(glue,glueStart,pixelsPerSec,rowNo):
  rigidLen=max(0,glue.length-glue.plusMinus)
  springWidth=glue.length+glue.adjustment-rigidLen
  springLen=2*glue.plusMinus
  svg.write('<g stroke="blue">') # colour for the rigid part of the "spring"
  moveTo(glueStart*pixelsPerSec,(rowNo+0.5)*rowHeight)
  lineTo((glueStart+rigidLen)*pixelsPerSec,(rowNo+0.5)*rowHeight)
  svg.write('</g>')
  drawCoils((glueStart+rigidLen)*pixelsPerSec,rowNo*rowHeight+rowMargin,springWidth*pixelsPerSec,rowHeight-2*rowMargin,springLen*pixelsPerSec)

glueToDraw=[] ; eventsToDraw=[] ; rows=[]
ellipsesToDraw = []
def prepareDraw(gluedEventList):
  # rows stores max time currently shown in each row.  This function must be called in time order.
  glueStart = 0
  row = -1
  ellipseLeft = ellipseRight = -1
  for i in gluedEventList:
    startTime = i.getEventStart(glueStart)
    if row<0:
      for r in range(len(rows)):
        if (not rows[r]) or rows[r]<=startTime-min_num_secs_before_row_reuse:
          row=r ; break
    if row<0:
      row=len(rows) ; rows.append(0)
    i.event.row=row
    i.event.start = startTime
    if ellipseLeft<0: ellipseLeft = startTime
    eventsToDraw.append(i.event)
    if glueStart:
      i.glue.row=row
      i.glue.start = glueStart
      glueToDraw.append(i.glue)
    glueStart = i.getAdjustedEnd(glueStart)
    ellipseRight = glueStart
    rows[row] = glueStart
  if ellipseLeft>=0 and ellipseRight>=0: ellipsesToDraw.append((row,ellipseLeft,ellipseRight,hasattr(gluedEventList[0],"timesDone") and gluedEventList[0].timesDone))

def sgn(i):
    if i>0: return 1
    elif i<0: return -1
    else: return 0

def byFirstLen(e1,e2):
    r = e1[0].glue.length+e1[0].glue.adjustment-e2[0].glue.length-e2[0].glue.adjustment
    # but it must return int not float, so
    return sgn(r)
def byStart(e1,e2): return sgn(e1.start-e2.start)

gradint.gluedListTracker=[]
gradint.waitBeforeStart=0
gradint.main()
gradint.gluedListTracker.sort(byFirstLen)
for l in gradint.gluedListTracker: prepareDraw(l)

# Calculate height and width
num_rows = len(rows)
num_seconds = max(rows)
if maxWidth: pixelsPerSec=min(pixelsPerSec,maxWidth*1.0/num_seconds)
if minWidth: pixelsPerSec=max(pixelsPerSec,minWidth*1.0/num_seconds)
if maxHeight: rowHeight=min(rowHeight,maxHeight*1.0/num_rows)
if minHeight: rowHeight=max(rowHeight,minHeight*1.0/num_rows)
image_width = int(math.ceil(num_seconds*pixelsPerSec))
image_height = int(math.ceil(num_rows*rowHeight))
svg.write('<svg xmlns="http://www.w3.org/2000/svg"  width="'+str2dp(image_width)+'" height="'+str2dp(image_height)+'">')

rowMargin = rowHeight*0.15

for row,ellipseLeft,ellipseRight,timesDone in ellipsesToDraw:
    if timesDone: fill="#c0c0c0"
    else: fill="pink"
    svg.write('<ellipse cx="'+str2dp((ellipseLeft+ellipseRight)*pixelsPerSec/2)+'" cy="'+str2dp((row+0.5)*rowHeight)+'" rx="'+str2dp((ellipseRight-ellipseLeft)*pixelsPerSec/2)+'" ry="'+str2dp((rowHeight-rowMargin/2)/2)+'" fill="'+fill+'" stroke="#c0c0c0" />\n') # ellipse behind whole sequence might make things clearer (although it does take a little longer to draw)

for g in glueToDraw: drawGlue(g,g.start,pixelsPerSec,g.row) # before events, so the reading line goes over the top of it

eventsToDraw.sort(byStart)
x=y=None
for e in eventsToDraw:
  if not x==None:
    svg.write('<g stroke="red">') # (lines between events to show reading order, at 0.25 and 0.75 so as not to clash with glue at 0.5)
    for yOff in [-0.25*rowHeight,0.25*rowHeight]:
      moveTo(x,y+yOff)
      lineTo(e.start*pixelsPerSec,(e.row+0.5)*rowHeight+yOff)
    svg.write('</g>')
  e.draw(e.start,pixelsPerSec,e.row*rowHeight+rowMargin,rowHeight-2*rowMargin)
  x=(e.start+e.length)*pixelsPerSec
  y=(e.row+0.5)*rowHeight

svg.write("</svg>")
