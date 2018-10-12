from revscoring.features import wikitext, revision_oriented, temporal
#from revscoring.languages import english
from revscoring.extractors import api
import revscoring
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
#    english.badwords.revision.diff.match_prop_delta_sum,
  # Measures the proportional change in "informals"
#    english.informals.revision.diff.match_prop_delta_sum,
  # Measures the proportional change meaningful words
#    english.stopwords.revision.diff.non_stopword_prop_delta_sum,
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
        
for revid in sample:
    revid = int(revid)
    print("https://en.wikipedia.org/wiki/?diff={0}".format(revid))
    print(list(api_extractor.extract(revid, features)))
"""
training = fileopen('datatraining.csv')
test = fileopen('datatest.csv')

for i in range(len(training)):
    trainingRevId.append(training[i])
#print(trainingRevId)
for j in range(len(test)):
    testRevId.append(test[j])
#print(testRevId)
for revTrainId in trainingRevId:
    revTrainId = int(revTrainId)
    try:
        print("https://en.wikipedia.org/wiki/?diff={0}".format(revTrainId))
        print(list(api_extractor.extract(revTrainId, features)))
    except:
        print('Revision Not Found')
        continue
"""for revTestId in testRevId:
    revTestId = int(revTestId)
    print("https://en.wikipedia.org/wiki/?diff={0}".format(revTestId))
    print(list(api_extractor.extract(revTestId, features)))"""
