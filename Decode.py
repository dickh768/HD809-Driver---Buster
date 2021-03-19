# Simple program to convert raw samples of I2C bus into readable text
# Data is bit 0,  Clock is bit 1


XFALLING = 0
XRISING = 1
XSTEADY = 2

Xin_data = False
Xbyte = 0
Xbit = 0
XoldSCL = 1
XoldSDA = 1

Xtransact = ""
bytecnt = 0


def parse(bte):

    global XoldSCL
    global XoldSDA
    global Xtransact
    global Xin_data
    global Xbit
    global Xbyte
    global bytecnt

    # Get the last two bits into SDA/SCL
    bte = int.from_bytes(bte,"big") & 3
    SCL=(bte>>1)
    SDA=(bte & 1)



    if SCL != XoldSCL:
       XoldSCL = SCL
       if SCL:
        xSCL = XRISING
       else:
        xSCL = XFALLING
    else:
        xSCL = XSTEADY

    if SDA != XoldSDA:
       XoldSDA = SDA
       if SDA:
        xSDA = XRISING
       else:
        xSDA = XFALLING
    else:
        xSDA = XSTEADY

    if xSCL == XRISING:
       if Xin_data:
        if Xbit < 8:
           Xbyte = (Xbyte << 1) | SDA
           Xbit += 1
        else:
           if bytecnt ==0 :
                rw=Xbyte & 1    #pick out the read/write bit
                if rw:
                    Xtransact += 'R '
                else:
                    Xtransact += 'W '
               
                Xbyte = Xbyte >> 1 # shift right to get rid of the ack bit from an address....
                bytecnt += 1
           Xtransact += '{:02X}'.format(Xbyte)
           if SDA:
            Xtransact += '-'
           else:
            Xtransact += '+'
           Xbit = 0
           Xbyte = 0
    elif xSCL == XSTEADY:

       if xSDA == XRISING:
        if SCL:
           Xin_data = False
           Xbyte = 0
           Xbit = 0
           Xtransact += ']' # STOP
           print (Xtransact)
           Xtransact = "#"

       if xSDA == XFALLING:
        if SCL:
           Xin_data = True
           Xbyte = 0
           Xbit = 0
           if Xtransact == '#':
               Xtransact = "{:.5f}".format(x/3000000)
           bytecnt=0
           Xtransact += '  [' # START





with open("D:/signal.raw", "rb") as f:

    for x in range(500000000):
        byte = f.read(1)
       # print(byte.hex())
        parse(byte)
    f.close()



