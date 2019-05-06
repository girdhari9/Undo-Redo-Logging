import sys

def get_variable_between_brackets(transaction):
	start_index = transaction.find("(")+1
	end_index = transaction.find(")")
	var = transaction[start_index : end_index]
	if not var.find(',') == -1:
		var1, var2 = var.split(',')
		var2 = var2.strip()
		var1 = var1.strip()
		return var1, var2
	return var.strip()

def print_dict(mydict):
	s = str()
	for key, value in mydict.items():
		if value != None:
			s += key
			s += ' ' + str(value) + ' '
	return s[0:-1]

def is_empty(mydict):
	flag = True
	for key, value in mydict.items():
		if len(value):
			flag = False
			break
	if flag:
		return True
	else:
		return False

def operation(op, var2, var3):
	if op == '+':
		return var2 + var3
	elif op == '-':
		return var2 - var3
	elif op == '*':
		return var2 * var3
	elif op == '/':
		return var2 / var3

def helper(transaction):
	if transaction.find('+') != -1:
		return '+'
	elif transaction.find('-') != -1:
		return '-'
	elif transaction.find('*') != -1:
		return '*'
	elif transaction.find('/') != -1:
		return '/'
	else:
		print("Invalid operator")
		exit(0)

def execute_x_lines(lines, main_memory, disk, extra_var, key):
	temp_output = list()
	for transaction in lines:
		if transaction.find('READ') != -1:
			var1, var2 = get_variable_between_brackets(transaction)
			if var1 not in disk:
				print("Not found: ",var1)
				exit(0)
			if main_memory[var1] == None:
				main_memory[var1] = disk[var1]
			extra_var[var2] = main_memory[var1]

		elif not transaction.find('WRITE') == -1:
			var1, var2 = get_variable_between_brackets(transaction)
			if var1 not in disk:
				print("Not found: ",var1)
				exit(0)
			val = '<'+key+', '+var1+', '+str(main_memory[var1])+'>'
			temp_output.append(val)
			main_memory[var1] = extra_var[var2]
			mmdict = print_dict(main_memory)
			temp_output.append(mmdict)
			diskdict = print_dict(disk)
			temp_output.append(diskdict)

		elif not transaction.find('OUTPUT') == -1:
			var1 = get_variable_between_brackets(transaction)
			disk[var1] = main_memory[var1]

		elif not transaction.find('=') == -1:
			end_index = transaction.find(":")
			var1 = transaction[0 : end_index].strip()
			op = helper(transaction)
			start_index = transaction.find("=") + 1
			end_index = transaction.find(op)
			var2 = transaction[start_index : end_index].strip()
			var3 = transaction[end_index + 1:].strip()
			if var2 not in extra_var:
				var2 = int(var2)
			else:
				var2 = extra_var[var2]
			if var3 not in extra_var:
				var3 = int(var3)
			else:
				var3 = extra_var[var3]
			extra_var[var1] = operation(op, var2, var3)
		else:
			print("Invalid Transactions Input")
			exit(0)
	return temp_output

#run python3 2018201019_1.py Part_1/input.txt 3
def main():
	x, filename = int(sys.argv[2]), sys.argv[1]
	file = None
	with open(filename, 'r') as f:
		file = f.read().splitlines()

	initial_val, disk, main_memory = file[0].split(), {}, {}
	index = 0
	for val in initial_val:
		if val.isdigit():
			disk[initial_val[index-1]] = int(val)
			main_memory[initial_val[index-1]] = None
		index += 1
	
	i, flag_start, transactions = 1, {}, {}
	while i < len(file):
		if not file[i] ==  '':
			trans_name, no_of_lines = file[i].split()
			transactions[trans_name], flag_start[trans_name] = file[i+1:i+int(no_of_lines)+1], False
			i += int(no_of_lines) + 1
		i += 1

	extra_var, final_output = {}, []
	while not is_empty(transactions):
		for key, value in transactions.items():
			if not flag_start[key]:
				flag_start[key] = True
				final_output.append('<START '+key+'>')
				mmdict = print_dict(main_memory)
				final_output.append(mmdict)
				diskdict = print_dict(disk)
				final_output.append(diskdict)
			if len(value) <= x:
				transactions[key] = []
				temp_output = execute_x_lines(value[0:],main_memory,disk,extra_var,key)
				final_output.extend(temp_output)
				mmdict = print_dict(main_memory)
				final_output.append('<COMMIT '+key+'>')
				final_output.append(mmdict)
				diskdict = print_dict(disk)
				final_output.append(diskdict)
			else:
				temp_output = execute_x_lines(value[0:x],main_memory,disk,extra_var,key)
				final_output.extend(temp_output)
				value = value[x:]
				transactions[key] = value

	with open("2018201019_1.txt",'w') as file:
		for x in final_output:
			file.write(x + '\n')	
		file.close()

if __name__ == "__main__":
	main()