#!/usr/bin/env python

import os, struct, sndhdr, sys
try: import winsound
except: winsound=None
macsound = (sys.platform.find("mac")>=0 or sys.platform.find("darwin")>=0)

# python 3+:
try: input
except: input=lambda x:eval(raw_input(x))

startCount = 0   # or however many WAVs already exist (should be even)

threshold = 10 # 3 is too low for recorded sound, but if using speech synth you might want to set it to 1
shortestSilence = 0.3
shortestSound = 0.4

if len(sys.argv)>1: exec(" ".join(sys.argv[1:])) # so you can override the above on the command line

sox_8bit, sox_16bit, sox_32bit, sox_signed, sox_unsigned = "-b", "-w", "-l", "-s", "-u"
if not winsound: # adapted from gradint (see comments there)
  sox_formats=os.popen("sox --help 2>&1").read()
  sf2 = ' '.join(sox_formats.lower().split())
  if sf2.startswith("sox: sox v"):
    if sf2[10]==' ': soxMaj=15
    else: soxMaj = int(sf2[10:sf2.index('.')])
  else: soxMaj=0
  if soxMaj>=14:
    if soxMaj==14 and sf2[13]<'4': sox_8bit, sox_16bit, sox_32bit = "-1", "-2", "-4"
    else: sox_8bit, sox_16bit, sox_32bit, sox_signed, sox_unsigned = "-b 8", "-b 16", "-b 32", "-e signed-integer", "-e unsigned-integer" # TODO: check the last one

def autosplit(filename,lang1,lang2,threshold):
    (wtype,rate,channels,wframes,bits) = sndhdr.what(filename)
    if bits==8:
        soxBits=sox_8bit+" "+sox_unsigned
        structBits="B"
    elif bits==16:
        soxBits=sox_16bit+" "+sox_signed
        structBits="h"
        threshold *= 256
    elif bits==32:
        soxBits=sox_32bit+" "+sox_signed
        structBits="i"
        threshold *= (256 * 256 * 256)
    else: raise Exception("Unsupported bits per sample")
    bytesPerSample = int(bits/8)
    soxParams = "-t raw %s -r %d -c 1" % (soxBits,rate)
    datapipe = os.popen("sox %s %s -" % (filename,soxParams))
    def nextSample():
        bytes = datapipe.read(bytesPerSample)
        if bytes:
            isSounding = abs(struct.unpack("1"+structBits,bytes)[0])>=threshold
            return isSounding, bytes
        else: return (False,None)
    dataToWriteout = [] ; numSilences = 0 ; inSilence = 0
    sampleNo = startCount ; bytes=True
    while bytes:
        (sounding, bytes) = nextSample()
        if inSilence and not sounding and bytes: continue
        elif bytes:
            if dataToWriteout or sounding:
                dataToWriteout.append(bytes)
            if sounding: numSilences = inSilence = 0
            else: numSilences += 1
        if numSilences >= int(shortestSilence*rate) or not bytes:
            inSilence = 1
            # dataToWriteout = dataToWriteout[:-numSilences] # DON'T do this - allow for the envelope's 'release' below the threshold.  However, have changed the 0.1 on the next line to 0.4 (= 0.1+0.3).
            if len(dataToWriteout) >= int(shortestSound*rate):
                # We can go ahead and write a sample
                if sampleNo%2: lang=lang2
                else: lang=lang1
                if lang1==lang2: c=sampleNo
                else: c=int(sampleNo/2)
                sampleNo += 1
                fname = "%04d_%s" % (c,lang)
                open(fname, "wb").write(''.join(dataToWriteout))
                os.system("sox %s \"%s\" \"%s.wav\"" % (soxParams,fname,fname))
                os.unlink(fname)
                print fname+".wav"
                if winsound: winsound.PlaySound(fname+".wav",winsound.SND_FILENAME)
                elif macsound: os.system("afplay "+fname+".wav")
                else: os.system("play "+fname+".wav")
            # Anyway, clear the output buffer
            dataToWriteout = []

sys.stdout.write("DO NOT RUN THIS SCRIPT unless recording is IDEAL\n(VERY little background noise, and good signal)\n")

filename = raw_input("Enter filename of main recording: ")
lang1=lang2=None
while not lang1: lang1=raw_input("Enter first language on recording (e.g. zh): ")
interleaved=input("Are two languages interleaved? (1/0): ")
if interleaved:
    while not lang2: lang2=raw_input("Enter second language on recording (e.g. en): ")
else: lang2=lang1

autosplit(filename,lang1,lang2,threshold)
