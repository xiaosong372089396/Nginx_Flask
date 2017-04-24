import csv
csvfile = open('南昌.csv','r')
reader = csv.reader(csvfile)
for line in reader:
    print (line)
csvfile.close()