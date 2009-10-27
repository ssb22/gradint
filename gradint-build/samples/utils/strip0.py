#!/usr/bin/env python

# Program to strip any silence from the beginning/end of a
# sound file (must be real 0-bytes not background noise)

# (This is useful as a "splitter" post-processor when
# getting samples from CD-ROMs e.g. "Colloquial Chinese" -
# don't use audacity here because some versions of audacity
# distort 8-bit audio files)

# Needs 'sox' + splitter

from splitter import *

for wavFile in sys.argv[1:]:
    # Figure out sox parameters
    header = sndhdr.what(wavFile)
    if not header: raise IOError("Problem opening %s" % (wavFile,))
    (wtype,rate,channels,wframes,bits) = header
    if bits==8: soxBits="-b -u" # unsigned
    elif bits==16: soxBits="-w -s" # signed
    elif bits==32: soxBits="-l -s" # signed
    else: raise Exception("Unsupported bits per sample")
    soxParams = "-t raw %s -r %d -c %d" % (soxBits,rate,channels)
    rawFile = wavFile + ".raw"
    # Now ready to convert to raw, and read it in
    convertToRaw(soxParams,wavFile,rawFile)
    o=open(rawFile,"rb")
    allData=o.read()
    o.close()
    # Now figure out how many samples we can take out
    bytesPerSample = channels*int(bits/8)
    if bytesPerSample==1: silenceVal=chr(128)
    else: silenceVal=chr(0)
    startIdx = 0
    while startIdx < len(allData):
        if not allData[startIdx]==silenceVal: break
        startIdx = startIdx + 1
    startIdx = int(startIdx/bytesPerSample) * bytesPerSample
    endIdx = len(allData)
    while endIdx:
        if not allData[endIdx-1]==silenceVal: break
        endIdx = endIdx - 1
    endIdx = endIdx - len(allData) # put it into -ve notatn
    endIdx = int(endIdx/bytesPerSample) * bytesPerSample
    endIdx = endIdx + len(allData) # avoid 0
    sys.stderr.write("Debugger: Clipping %s to %d:%d\n" % (wavFile,startIdx,endIdx))
    allData = allData[startIdx:endIdx]
    # Write back the file, and convert it back to wav
    o=open(rawFile,"wb")
    o.write(allData)
    o.close()
    convertToWav(soxParams,rawFile,wavFile)
    # Clean up
    os.unlink(rawFile)
