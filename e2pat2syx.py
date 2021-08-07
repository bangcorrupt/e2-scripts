# Converts .e2pat to .syx
import argparse
from bitstring import BitArray

def main():	
	
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", dest='patNum', help="destination pattern number")
    parser.add_argument("file", metavar="filepath", type=str, help="path/to/file.e2pat")

    args = parser.parse_args()

    with open(args.file, 'rb') as f:	
        data =  bytearray(f.read())	
    data = data[0x100:]

    syxHead = bytearray([0xf0, 0x42, 0x30, 0x00, 0x01, 0x23, 0x40])		#	dump to current pattern

    if args.patNum:
        patNum = int(args.patNum)-1
        msb = 0
        lsb = patNum % 128
        if patNum > 127:
            msb = 1
        syxHead = bytearray([0xf0, 0x42, 0x30, 0x00, 0x01, 0x23, 0x4c, lsb, msb])	#	dump to patNum
        

    syxdata = syxHead + syx_enc(data) + b'\xf7'

    outfile = args.file[:-5] + 'syx'											# change filename extension

    with open(outfile, 'wb') as f:
        f.write(syxdata)

    if args.patNum:
        print(args.file + ' converted to ' + outfile + ', pattern number ' + args.patNum)
    else:
        print(args.file + ' converted to ' + outfile)



def syx_enc(byt):
    
    lng = len(byt)
    lst = []
    tmp = []
    b = 0
    cnt = 7
    lim = 0
    for i,e in enumerate(byt):

        if lng < 7:
            lim = 7 - lng

        a = e & ~0b10000000
        b |= ((e & 0b10000000)>>cnt)
        
        tmp.append(a)
        
        cnt -= 1
        if cnt == lim:
            lst.append([b])
            lst.append(tmp)
            tmp = []
            b = 0
            cnt = 7

            if (lng - i) < 7:
                lim = 7 - (lng - i) + 1

    syx = [item for sublist in lst for item in sublist]

    return bytes(syx)



if __name__ == '__main__':
    main()
