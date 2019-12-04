# Read the Wolfram|Alpha API key from keys.txt
f = open('keys.txt', 'r')
line = f.readline()
f.close()
WFAkey = line[11:(len(line) - 2)]
