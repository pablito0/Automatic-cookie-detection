import os


file = open(r'C:\Dev\TFG\Github\Automatic-cookie-detection\1MillionPages.txt', 'r')
Lines = file.readlines()
count = 100
writeFile = open (r'C:\Dev\TFG\Github\Automatic-cookie-detection\PaginasEspana.txt', 'w')
cleanLines = []
for line in Lines:
    if (".es\n" in line[len(line)-4:]):
        cleanLines.append(line)
writeFile.writelines(cleanLines)
writeFile.close
file.close