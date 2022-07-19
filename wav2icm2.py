import audioop
import wave
import aifc
import sys
import io
import os
import wavio
import numpy
    
'''
Project Luminous
wav2icm(CHISATO) Ver 2
2021/03/24
'''

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def icmmaker(dir):
    loadwav=wave.open(dir, mode='rb')
    wavch=loadwav.getnchannels()
    wavwt=loadwav.getsampwidth()
    #print(wavwt)
    wavfr=loadwav.getframerate()
    wavfra=loadwav.getnframes()
    wavdata=loadwav.readframes(wavfra) 
    if wavch == 2:
        print('Stereo WAV')
        loadswav=wavio.read(dir)
        wavdataL = loadswav.data[:, 0].tobytes()
        wavdataR = loadswav.data[:, 1].tobytes()
        leftadpcm = audioop.lin2adpcm(wavdataL, wavwt, None)[0]
        rightadpcm = audioop.lin2adpcm(wavdataR, wavwt, None)[0]
        '''
        www=open('lmart.adraw', 'wb')
        www.write(leftadpcm)
        www.close()
        lol=open('rmart.adraw', 'wb')
        lol.write(rightadpcm)
        lol.close()
        
        print(len(leftadpcm))
        print(len(rightadpcm))
        '''
        supertemp=''
        speedsrt=io.StringIO(supertemp)
        for i in range(0, len(leftadpcm)):
            aint = leftadpcm[i]
            bint = rightadpcm[i]
            a1bin=bin(aint)[2:].zfill(8)[:4]
            b1bin=bin(bint)[2:].zfill(8)[:4]
            a2bin=bin(aint)[2:].zfill(8)[4:]
            b2bin=bin(bint)[2:].zfill(8)[4:]
            speedsrt.write(a1bin+b1bin+a2bin+b2bin)
        speedsrt.seek(0)
        sbin = speedsrt.read()
        test123 = bitstring_to_bytes(sbin)
        #print('load OK')
        
    elif wavch == 1 :
        test123 = audioop.lin2adpcm(wavdata, wavwt, None)[0]
    '''
    www=open('3mart.raw', 'wb')
    www.write(wavdata)
    www.close()
    '''
    fakeaiff=aifc.open(dir+'.aiff', mode='wb')
    fakeaiff.setnchannels(wavch)
    fakeaiff.setsampwidth(wavwt)
    fakeaiff.setframerate(wavfr)
    fakeaiff.setnframes(wavfra)
    fakeaiff.close()
    loadfakeaiff=open(dir+'.aiff', mode='rb')
    makefakeICM=open(dir+'.ICM', mode='wb')
    makefakeICM.write(b'FORM')
    if wavch == 1:
        bigsiseint=28+len(test123)+18
    elif wavch == 2:
        bigsiseint=28+len(test123)+18
    #print(bigsiseint)
    bigsise=bigsiseint.to_bytes(4, byteorder="big")
    #print(bigsise)
    makefakeICM.write(bigsise)
    loadfakeaiff.seek(8)
    aiffpart1=loadfakeaiff.read(14)
    makefakeICM.write(aiffpart1)
    
    if wavch == 1:
        supersiseint=(bigsiseint-46)*2
    elif wavch == 2:
        supersiseint=bigsiseint-46
    
    supersise=supersiseint.to_bytes(4, byteorder="big")
    makefakeICM.write(supersise)
    makefakeICM.write(b'\x00\x04')
    loadfakeaiff.seek(28)
    aiffpart2=loadfakeaiff.read(8)
    makefakeICM.write(aiffpart2)
    if wavch == 1:
        makefakeICM.write(b'\x00\x00\x41\x50\x43\x4D')
        makefakeICM.write(supersise)
        makefakeICM.write(b'\x00'*8)
        makefakeICM.write(test123)
    elif wavch == 2:   
        makefakeICM.write(b'\x00\x00\x41\x50\x43\x4D')
        makefakeICM.write(supersise)
        makefakeICM.write(b'\x00'*8)
        makefakeICM.write(test123)
    loadfakeaiff.close
    makefakeICM.close
    #os.remove(dir+'.aiff')
    
    
dir=sys.argv[1]    
icmmaker(dir)  