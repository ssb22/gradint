#!/usr/bin/env python

# Program to support splitting a long sound file into
# several little ones.

# Needs 'sox' - if Windows, download from
# sox.sourceforge.net
# (e.g. http://prdownloads.sourceforge.net/sox/sox12172.zip
# - note gives a "select a mirror" dialogue) and put sox.exe
# in the same directory or on the path

# -----------------------

# lowpri: 2nd sort key by length ? (only matters if adding a lot of new words & phrases at same time)

import time,os,sndhdr,sys
try: import winsound
except: winsound=None
macsound = (sys.platform.find("mac")>=0 or sys.platform.find("darwin")>=0)
if macsound: sys.stderr.write("Warning: You need to have qtplay (from gradint or wherever) in your PATH for this to work\n")

def rawcut(allData,fromSecs,toSecs,rate=22050,bits=16,channels=1):
    return allData[secbyte(fromSecs,rate,channels,bits):secbyte(toSecs,rate,channels,bits)]
def secbyte(sec,rate,channels,bits):
    # Convert a time in seconds to a byte offset in the raw
    # data
    # Note: Result MUST be a multiple of bytesPerSample
    # 'sec' is not necessarily an integer
    sampleNo = int(0.5+sec*rate) # nearest integer sample no
    bytesPerSample = channels*int(bits/8)
    return sampleNo * bytesPerSample

def readTimings(langs):
    if macsound: time.sleep(1) # OS X hack due to qtplay delay (1sec on an Intel 2GHz Core Duo running OSX 10.5)
    sys.stdout.write("Starting clock\n")
    # Now using time.time() rather than time.clock()
    # due to clock units confusion
    # Just have to hope the system is accurate enough
    offset = time.time()
    ret = [] ; ip=''
    start = offset
    while not ip=='q':
        ip = raw_input(langs[len(ret)%len(langs)]+": ")
        t = time.time()
        if ip=="c" and ret: ret[-1]=(ret[-1][0],t-offset)
        elif not ip: ret.append((start-offset,t-offset))
        start = t
    sys.stdout.write("Finishing at %f seconds\n" % (t-offset,))
    return ret

def instructions():
    sys.stdout.write("Press Return between samples\n")
    sys.stdout.write("Enter 'c' to change the time of the last Return to this one\n")
    sys.stdout.write("Enter 'x' to omit this bit (e.g. silence)\n")
    sys.stdout.write("Enter 'q' when done (AFTER stopping last sample)\n")
    sys.stdout.write("PRESS RETURN TO START\n")
    raw_input()

def getParams():
    wavFile=raw_input("Enter filename of main recording: ")
    header = sndhdr.what(wavFile)
    if not header:
        sys.stdout.write("Problem opening that file\n")
        return None
    (wtype,rate,channels,wframes,bits) = header
    sys.stdout.write("WAV file is %d-bit\n" % (bits,))
    if bits==8: soxBits="-b -u" # unsigned
    elif bits==16: soxBits="-w -s" # signed
    elif bits==32: soxBits="-l -s" # signed
    else:
        sys.stdout.write("Unsupported bits per sample '%s'\n" % (bits,))
        return None
    soxParams = "-t raw %s -r %d -c %d" % (soxBits,rate,channels)
    rawFile = wavFile + ".raw"
    convertToRaw(soxParams,wavFile,rawFile)
    lang1=lang2=None
    while not lang1: lang1=raw_input("Enter first language on recording (e.g. zh): ")
    interleaved=input("Are two languages interleaved? (1/0): ") # (horrible hack)
    if interleaved:
        while not lang2: lang2=raw_input("Enter second language on recording (e.g. en): ")
    else:
        lang2=lang1
        sys.stdout.write("OK - should run this program again for other language's recording\n")
    return soxParams,wavFile,rawFile,lang1,lang2,rate,bits,channels

def convertToWav(soxParams,rawFile,wavFile):
    os.system("sox %s \"%s\" \"%s\"" % (soxParams,rawFile,wavFile))
def convertToRaw(soxParams,wavFile,rawFile):
    os.system("sox \"%s\" %s \"%s\"" % (wavFile,soxParams,rawFile))

def main():
    tuple=None
    while not tuple: tuple=getParams()
    soxParams,wavFile,rawFile,lang1,lang2,rate,bits,channels = tuple
    mainLoop(soxParams,wavFile,rawFile,lang1,lang2,rate,bits,channels)
    os.unlink(rawFile)

# Set lang1 & lang2 equal if not interleaving
def mainLoop(soxParams,wavFile,rawFile,lang1="zh",lang2="en",rate=22050,bits=16,channels=1):
    allData=open(rawFile,"rb").read()
    open(wavFile,"rb").read() # to cache before starting clock and 'play' (especailly because just loaded the separate raw data) (could also play from raw data if got sox)
    instructions()
    # Start sound asynchronously - hope for the best that
    # the first clock reading is near enough to the actual
    # start of the sound
    if winsound: winsound.PlaySound(wavFile,winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif macsound: os.spawnlp(os.P_NOWAIT,"qtplay","qtplay",wavFile)
    # else: os.spawnlp(os.P_NOWAIT,"play","play",wavFile)
    # Problem: What if 'play' o/p's at slightly less than the correct rate - will think the cuts are further on in the file than they really are.  (e.g. 16000Hz on a z61p Cygwin, "time play" shows it takes slightly longer than sox thinks the file is)
    # Better convert to 44100 just to make sure.
    else: os.system("sox \"%s\" -r 44100 -t wav - | play -t wav - &" % wavFile)
    # Read timings, cut up, and write out the samples
    samples = [ rawcut(allData,s,f,rate,bits,channels) for s,f in readTimings([lang1,lang2]) ]
    formatString = "%0"+str(len(str(int(len(samples)/(2-(lang2==lang1))-1))))+"d_%s"
    # (pad with 0s as necessary so it's in order)
    # (len(samples)-1 gives highest number, so len(str(l..))
    # gives number of digits in it)
    for i in range(len(samples)):
        if i%2: lang=lang2
        else: lang=lang1
        if lang1==lang2: c=i
        else: c=int(i/2)
        fname = formatString % (c,lang)
        f=open(fname, "wb")
        f.write(samples[i])
        f.close()
        convertToWav(soxParams,fname,fname+".wav")
        os.unlink(fname)
        sys.stdout.write("Written %s.wav\n" % (fname,))

if __name__=="__main__":
    main()
