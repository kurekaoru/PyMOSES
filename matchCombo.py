import sys, re

def getAllMatches(string, pattern):
	indeces = [(m.start(0), m.end(0)) for m in re.finditer(pattern, string.strip())]
	return [string[x[0]:x[1]] for x in indeces]

if __name__ == '__main__':
	R = [x.strip() for x in open(sys.argv[1]).readlines()]
	print getAllMatches(R[-1], '\$\d{6}(_.{1,2})?_at')

