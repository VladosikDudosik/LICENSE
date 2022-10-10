import csv
from itertools import count

result = {}
with open("data.csv",'r') as file:
    spamreader = csv.reader(file, delimiter=' ', quotechar='|')
    for row in spamreader:
        temp = row[0].split(',')
        if temp[0] in result:
            result[temp[0]]['people'].append(temp[1])
            result[temp[0]]['count'] +=1
        else:
            result[temp[0]] = {'people':[temp[1]],'count':1}
        

print(result)