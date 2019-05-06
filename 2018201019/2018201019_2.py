from collections import OrderedDict
import sys

def print_dict(mydict):
	s = str()
	for key, value in mydict.items():
		if value != None:
			s += key
			s += ' ' + str(value) + ' '
	return s[0:-1]

def process_log(lines, disk, com_trans, flag):
	keyword = ["START CKPT", "END CKPT", "COMMIT", "START"]
	for line in reversed(lines):
		start_index = line.find("<") + 1
		end_index = line.find(">")
		temp = line[start_index : end_index]
		if flag and (keyword[0] in line):
			break
		elif(keyword[1] in line):
			flag = True
		elif(keyword[2] in line):
			garbage,trans=temp.split(' ')
			com_trans.append(trans.strip())
		elif(keyword[3] not in line):
			trans, var, val=temp.split(',')
			val, var, trans = int(val.strip()), var.strip(), trans.strip()
			if(trans not in com_trans):
				disk[var] = val

def main():
	file = None
	with open(sys.argv[1],'r') as f:
		file = f.read().splitlines()

	initial_val, disk = file[0].split(), OrderedDict()
	index = 0
	for val in initial_val:
		if val.isdigit():
			disk[initial_val[index - 1]] = int(val)
		index += 1

	process_log(list(file[2:]), disk, [], False)

	file = open("2018201019_2.txt",'w')
	distdict = print_dict(disk)
	file.write(distdict + '\n')
	file.close()

if __name__ == "__main__":
	main()