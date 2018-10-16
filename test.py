from revscoring.features import wikitext, revision_oriented, temporal
from revscoring.languages import english
from revscoring.extractors import api
from revscoring.utilities.util import read_observations
import mwapi
import csv

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

sample = []
with open('datasample.csv') as csv_file:
    data_csv_reader = csv.reader(csv_file, delimiter=',')
    for row in data_csv_reader:
        if row != []:
            sample.append(row[1])

sampleData = []
for revid in sample:
    revid = int(revid)
    try:
        #print("https://en.wikipedia.org/wiki/?diff={0}".format(revid))
        sampleRevData = list(api_extractor.extract(revid, features))
        sampleObserv = {"rev_id": revid, "cashe": sampleRevData}
        sampleData.append(sampleObserv)
    except:
        print('Revision Data Not Found')
        continue
sampleFeatures = read_observations(sampleData)
print(sampleFeatures)

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
for revTrainId in trainingRevId:
    revTrainId = int(revTrainId)
    try:
        #print("https://en.wikipedia.org/wiki/?diff={0}".format(revTrainId))
        trainingRevData = list(api_extractor.extract(revTrainId, features))
        trainingObserv = {"rev_id": revTrainId, "cache": trainingRevData}
        trainingData.append(trainingObserv)
    except:
        print('Revision Data Not Found')
        continue
trainingFeatures = read_observations(trainingData)
print(trainingFeatures)

testData = []
for revTestId in testRevId:
    revTestId = int(revTestId)
    try:
        #print("https://en.wikipedia.org/wiki/?diff={0}".format(revTestId))
        testRevData = list(api_extractor.extract(revTestId, features))
        testObserv = {"rev_id": revTestId, "cache": testRevData}
        testData.append(testObserv)
    except:
        print('Revision Data Not Found')
        continue
testFeatures = read_observations(testData)
print(testFeatures)
"""
print(sampleData)
#print(trainingData)
#print(testData)