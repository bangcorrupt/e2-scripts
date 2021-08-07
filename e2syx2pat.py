# Converts .syx to .e2pat
import argparse
from bitstring import BitArray

def main():	

    patHead = bytearray(b'\x4b\x4f\x52\x47' + b'\x00' * 12 + 
                        b'\x65\x6c\x65\x63\x74\x72\x69\x62\x65' +
                        b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00' + 
                        b'\xff' * 220)

    
    parser = argparse.ArgumentParser()
    parser.add_argument("file", metavar="filepath", type=str, help="path/to/file.syx")

    args = parser.parse_args()

    with open(args.file, 'rb') as f:	
        data =  bytearray(f.read())[:-1]

    if data[6] == 0x40:						# remove syx header from 'current pattern dump'
        data = data[7:]		
    elif data[6] == 0x4c:					# remove syx header from 'pattern dump'
        data = data[9:]


    patData = patHead + syx_dec(data)

    outfile = args.file[:-3] + 'e2pat'			# change filename extension
    with open(outfile, 'wb') as f:
        f.write(patData)

    print(args.file + ' converted to ' + outfile)



def syx_dec(syx):

    chk = [syx[i:i + 8] for i in range(0, len(syx), 8)]

    lst = []
    tmp = []
    a = 0
    
    for l in chk:
        for i in range(len(l)-1):
            a = l[i+1]
            a |= ((l[0] & (1<<i))>>i)<<7
            
            tmp.append(a)

        lst.append(tmp)
        tmp = []
    
    byt = [item for sublist in lst for item in sublist]
    
    return bytes(byt)


if __name__ == '__main__':
    main()
