import csv
import random
import requests
import mwreverts
import mwapi
from lxml import html

training = []
test = []
data = []
dataFlag = []
#print("hello world")
with open('datatotal.csv') as csv_file:
    data_csv_reader = csv.reader(csv_file, delimiter=',')
    dataLine = 0
    for row in data_csv_reader:
        if dataLine % 2 == 0:
            data.append(row)
            dataFlag.append('False')
        dataLine += 1
        print(dataLine)

while 'False' in dataFlag:
    indexNum = random.randint(0, len(data) - 1)
    print(indexNum)
    if dataFlag[indexNum] == 'True':
        continue
    elif dataFlag[indexNum] == 'False':
        dataFlag[indexNum] = 'True'
        currentRevid = data[indexNum][1]
        beforeRevid = data[indexNum][0]
        afterRevid = data[indexNum][2]
        currentWiki = requests.get('https://en.wikipedia.org/wiki/?diff=' + str(currentRevid))
        beforeWiki = requests.get('https://en.wikipedia.org/wiki/?diff=' + str(beforeRevid))
        afterWiki = requests.get('https://en.wikipedia.org/wiki/?diff=' + str(afterRevid))
        current = []
        for line in currentWiki:
            current.append(line)
        print(current[0])
        print(current[1])
        #print(beforeWiki.text)
        #print(currentWiki.text)
        #print(afterWiki.text)
