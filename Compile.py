import csv
import random

training = []
test = []
data = []
dataFlag = []

for i in range(1, 11):
    with open('data' + str(i) + '.csv') as csv_file:
        data_csv_reader = csv.reader(csv_file, delimiter=',')
        for row in data_csv_reader:
            if row != []:
                data.append(row)
                dataFlag.append('False')

while len(training) != int(len(data) * .75):
    indexNum = random.randint(0, len(data) - 1)
    if dataFlag[indexNum] == 'True':
        continue
    else:
        training.append(data[indexNum])
        dataFlag[indexNum] = 'True'

for x in range(len(data)):
    if dataFlag[x] == 'False':
        dataFlag[x] = 'True'
        test.append(data[x])

print(len(data))
print(len(training))
print(len(test))
training_revert = 0
training_no_revert = 0
test_revert = 0
test_no_revert = 0

for train in range(len(training)):
    if training[train][3] == 'False':
        training_no_revert += 1
    elif training[train][3] == 'True':
        training_revert += 1

for t in range(len(test)):
    if test[t][3] == 'False':
        test_no_revert += 1
    elif test[t][3] == 'True':
        test_revert += 1

print(training_revert)
print(training_no_revert)
print(round(((training_revert / len(training)) * 100), 2))
print(round(((training_no_revert / len(training)) * 100), 2))
print(test_revert)
print(test_no_revert)
print(round(((test_revert / len(test)) * 100), 2))
print(round(((test_no_revert / len(test)) * 100), 2))
print(len(training))
print(len(test))

"""
with open('datatotal.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(data)):
        writer.writerow(data[i])

with open('datatraining.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for j in range(len(training)):
        writer.writerow(training[j])

with open('datatest.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for k in range(len(test)):
        writer.writerow(test[k])
"""
