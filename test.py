from revscoring.features import wikitext, revision_oriented, temporal
from revscoring.languages import english
from revscoring.extractors import api
from revscoring.utilities.util import read_observations
import mwapi
import csv
import json

def fileopen(file):
    filelist = []
    with open(str(file)) as csv_file:
        data_csv_reader = csv.reader(csv_file, delimiter=',')
        for row in data_csv_reader:
            if row != []:
                filelist.append(row[1])
    return filelist

session = mwapi.Session("https://en.wikipedia.org")
features = [
  # Catches long key mashes like kkkkkkkkkkkk
    wikitext.revision.diff.longest_repeated_char_added,
  # Measures the size of the change in added words
    wikitext.revision.diff.words_added,
  # Measures the size of the change in removed words
    wikitext.revision.diff.words_removed,
  # Measures the proportional change in "badwords"
    english.badwords.revision.diff.match_prop_delta_sum,
  # Measures the proportional change in "informals"
    english.informals.revision.diff.match_prop_delta_sum,
  # Measures the proportional change meaningful words
    english.stopwords.revision.diff.non_stopword_prop_delta_sum,
  # Is the user anonymous
    revision_oriented.revision.user.is_anon,
  # Is the user a bot or a sysop
    revision_oriented.revision.user.in_group({'bot', 'sysop'}),
  # How long ago did the user register?
    temporal.revision.user.seconds_since_registration
]

trainingRevId = []
testRevId = []
api_extractor = api.Extractor(session)
"""
sample = []
with open('datasample.csv') as csv_file:
    data_csv_reader = csv.reader(csv_file, delimiter=',')
    for row in data_csv_reader:
        if row != []:
            sample.append(row[1])

sampleData = []
sampleInfo = []
for revid in sample:
    revid = int(revid)
    try:
        #print("https://en.wikipedia.org/wiki/?diff={0}".format(revid))
        sampleRevData = list(api_extractor.extract(revid, features))
        sampleObserv = {"rev_id": revid, "cashe": sampleRevData}
    except:
        print('Revision Data Not Found')
        continue
    sampleObserv = json.dumps(sampleObserv)
    sampleData.append(sampleObserv)

for samples in read_observations(sampleData):
    sampleInfo.append(samples)

"""
training = fileopen('datatraining.csv')
test = fileopen('datatest.csv')

for i in range(len(training)):
    trainingRevId.append(training[i])
#print(trainingRevId)

for j in range(len(test)):
    testRevId.append(test[j])
#print(testRevId)

trainingData = []
trainingInfo = []
for revTrainId in trainingRevId:
    revTrainId = int(revTrainId)
    try:
        #print("https://en.wikipedia.org/wiki/?diff={0}".format(revTrainId))
        trainingRevData = list(api_extractor.extract(revTrainId, features))
        trainingObserv = {"rev_id": revTrainId, "cache": trainingRevData}
    except:
        print('Revision Data Not Found')
        continue
    trainingObserv = json.dumps(trainingObserv)
    trainingData.append(trainingObserv)

for trainings in read_observations(trainingData):
    trainingInfo.append(trainings)

testData = []
testInfo = []
for revTestId in testRevId:
    revTestId = int(revTestId)
    try:
        #print("https://en.wikipedia.org/wiki/?diff={0}".format(revTestId))
        testRevData = list(api_extractor.extract(revTestId, features))
        testObserv = {"rev_id": revTestId, "cache": testRevData}
    except:
        print('Revision Data Not Found')
        continue
    testObserv = json.dumps(testObserv)
    testData.append(testObserv)

for tests in read_observations(testData):
    testInfo.append(tests)

with open('TrainingInfo.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(trainingInfo)):
        writer.writerow(trainingInfo[i])

with open('TestInfo.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(testInfo)):
        writer.writerow(testInfo[i])
#"""

#print(sampleInfo)
print(trainingInfo)
print(testInfo)
