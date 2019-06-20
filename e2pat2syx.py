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
	data = data[256:]

	syxHead = bytearray([0xf0, 0x42, 0x30, 0x00, 0x01, 0x23, 0x40])		#	dump to current pattern
	
	if args.patNum:
		patNum = int(args.patNum)-1
		msb = 0
		lsb = patNum % 128
		if patNum > 127:
			msb = 1
		syxHead = bytearray([0xf0, 0x42, 0x30, 0x00, 0x01, 0x23, 0x4c, lsb, msb])	#	dump to patNum
		
	bits = BitArray(bytes=data).bin		# convert to bitstring
	byt = []
	b = []
	for i in range(len(bits)):			# group into bytes
		b.append(bits[i])
		if len(b) == 8:
			byt.append(b)
			b = []
	
	sets = []
	s = []
	for i in range(len(byt)):			# group into 7 byte sets
		s.append(byt[i])
		if len(s) == 7:
			sets.append(s)			
			s = []

	nubyte = ['0']
	for i in range(len(sets)):
		for j in range(len(sets[i])):		
			nubyte.insert(1,sets[i][j][0])	# add bit to new byte
			sets[i][j][0] = '0'				# set bit to zero
			if len(nubyte) == 8:		
				sets[i].insert(0,nubyte)	# add new byte
				nubyte = ['0']
	
	nudata = []
	for s in sets:
		for b in s:
			nudata.append(int(''.join(b), 2))	# flatten list and convert bitstrings to int

	nudata = bytearray(nudata)					# convert to bytes

	syxdata = syxHead + nudata +  bytearray([0x00,0x00,0x00,0x00,0x00,0xf7])	# Add sysex header and tail bytes
	
	outfile = args.file[:-5] + 'syx'											# change filename extension
	with open(outfile, 'wb') as f:
		f.write(syxdata)

	if args.patNum:
		print(args.file + ' converted to ' + outfile + ', pattern number ' + args.patNum)
	else:
		print(args.file + ' converted to ' + outfile)


if __name__ == '__main__':
    main()
