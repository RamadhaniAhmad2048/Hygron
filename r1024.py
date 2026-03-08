def system(INPUT_TEXT):
	print("[*] %s%s%s" % ('\033[1;37m', INPUT_TEXT, '\033[0m'))

def info(INPUT_TEXT):
	print("[I] %s%s%s" % ('\033[1;36m', INPUT_TEXT, '\033[0m'))

def success(INPUT_TEXT):
	print("[S] %s%s%s" % ('\033[1;32m', INPUT_TEXT, '\033[0m'))

def warning(INPUT_TEXT):
	print("[W] %s%s%s" % ('\033[1;33m', INPUT_TEXT, '\033[0m'))

def alert(INPUT_TEXT):
	print("[A] %s%s%s" % ('\033[1;31m', INPUT_TEXT, '\033[0m'))