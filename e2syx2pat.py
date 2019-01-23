# Converts .syx to .e2pat
import argparse
from bitstring import BitArray

def main():	
	patHead = bytearray(b'\x4b\x4f\x52\x47\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x65\x6c\x65\x63\x74\x72\x69\x62\x65'
							b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xff\xff\xff\xff\xff'
								b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
									b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
										b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
											b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
												b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
													b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
														b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
															b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
																b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
																	b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
																		b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
																			b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
																				b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
																					b'\xff\xff\xff\xff\xff\xff\xff')
	parser = argparse.ArgumentParser()
	parser.add_argument("file", metavar="filepath", type=str, help="path/to/file.syx")
	
	args = parser.parse_args()

	with open(args.file, 'rb') as f:	
		data =  bytearray(f.read())	

	if data[6] == 0x40:						# remove syx header from 'current pattern dump'
		data = data[7:]		
	elif data[6] == 0x4c:					# remove syx header from 'pattern dump'
		data = data[9:]
	
	bits = BitArray(bytes=data).bin			# convert to bitstring
	byt = []
	b = []
	for i in range(len(bits)):				# group into bytes
		b.append(bits[i])
		if len(b) == 8:
			byt.append(b)
			b = []
	
	sets = []
	s = []
	for i in range(len(byt)):
		s.append(byt[i])
		if len(s) == 8: 					# group into 8 byte sets
			sets.append(s)
			s = []

	for i in range(len(sets)):
		syxbyte = sets[i][0][1:]			# get added byte
		sets[i] = sets[i][1:]				# remove added byte from set
		for j in range(len(sets[i])):
			sets[i][j][0] = syxbyte[6-j]	# replace start bit

	nudata = []								
	for s in sets:
		for b in s:
			nudata.append(int(''.join(b), 2))	# flatten list and convert bitstrings to int

	nudata = bytearray(nudata)					# convert to bytes

	patData = patHead + nudata + bytearray([0x00,0x00,0x00,0x00])		# Add Korg file header and tail bytes

	outfile = args.file[:-3] + 'e2pat'			# change filename extension
	with open(outfile, 'wb') as f:
		f.write(patData)
	
	print(args.file + ' converted to ' + outfile)

if __name__ == '__main__':
    main()
