f = open("pairs_input", "r")

dic = {}
# got it by typing in debugger
# x/29wx 0x404060 (address of correct_pass)
correct_pass = [0xa4a69f3d, 0xf83bc3a8, 0xef910d0d, 0xdf671b52, 
				0x119e53f0, 0xd999b520, 0xea6a8210, 0x101a5985, 
				0xea6a8210, 0xbf945420, 0x7ecefaf8, 0x101a5985,
				0x792a531c, 0x3c15d9d6, 0x792a531c, 0x78cfd480, 
				0xdd97f41c, 0x101a5985, 0x408db164, 0x792a531c, 
				0x8158d281, 0x101a5985, 0xd999b520, 0xabc7ba0d, 
				0x101a5985, 0xea6a8210, 0xfa67b835, 0x42bb6661,
				0x0e0a33cf]

for line in f:
	line = line[:len(line) - 1]
	values = line.split(" ")
	formatted_val1 = hex(int(values[1]))
	if formatted_val1[-1] == 'L':
		formatted_val1 = formatted_val1[:-1]
	formatted_val1 = int('0x' + formatted_val1[-8:], 16)
	dic[formatted_val1] = int(values[0])

f.close()

solution = ''
for num in correct_pass:
	gen_num = dic[num]
	solution += chr(int(hex(gen_num)[-3:], 16))

print solution

