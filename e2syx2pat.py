# Converts .syx to .e2pat
import argparse
from e2_syx_codec import syx_dec


def main():	

    parser = argparse.ArgumentParser()
    parser.add_argument("file", metavar="filepath", type=str, help="path/to/file.syx")

    args = parser.parse_args()

    with open(args.file, 'rb') as f:	
        data =  bytearray(f.read())

    if data[6] == 0x40:						# remove syx header from 'current pattern dump'
        data = data[7:-1]		
    elif data[6] == 0x4c:					# remove syx header from 'pattern dump'
        data = data[9:-1]


    pat_data = syx_to_pat(data)

    outfile = args.file[:-3] + 'e2pat'			# change filename extension
    with open(outfile, 'wb') as f:
        f.write(pat_data)

    print(args.file + ' converted to ' + outfile)



def syx_to_pat(syx_data):
    
    pat_head = bytearray(b'\x4b\x4f\x52\x47' + b'\x00' * 12 + 
                    b'\x65\x6c\x65\x63\x74\x72\x69\x62\x65' +
                    b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00' + 
                    b'\xff' * 220)
                    
    pat_data = pat_head + syx_dec(syx_data)
    
    return pat_data

if __name__ == '__main__':
    main()
