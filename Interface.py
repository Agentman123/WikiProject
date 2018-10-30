import random
from revscoring.features import wikitext, revision_oriented, temporal
from revscoring.languages import english
from revscoring.extractors import api
from revscoring.utilities.util import read_observations
import mwapi
import json
import sys, traceback
import mwreverts.api

session = mwapi.Session('https://en.wikipedia.org')
rev_reverteds = []
flag = True
while flag == True:
    revid = random.randint(700000000, 900000000)
    try:
        _, reverted, reverted_to = mwreverts.api.check(
            session, revid, radius=5,  # most reverts within 5 edits
            window=48 * 60 * 60,  # 2 days
            rvprop={'user', 'ids'})  # Some properties we'll make use of
        flag = False
    except (RuntimeError, KeyError) as e:
        sys.stderr.write(str(e))
        print('Revision ID ' + str(revid) + ' does not exist')
    
if reverted is not None:
    reverted_doc = [r for r in reverted.reverteds if r['revid'] == revid][0]
    if 'user' not in reverted_doc or 'user' not in reverted.reverting:
        None
    self_revert = reverted_doc['user'] == reverted.reverting['user']
    # revisions that are reverted back to by others
    reverted_back_to = reverted_to is not None and 'user' in reverted_to.reverting and reverted_doc['user'] != reverted_to.reverting['user']
    # If we are reverted, not by self or reverted back to by someone else,
    # then, let's assume it was damaging.
    damaging_reverted = not (self_revert or reverted_back_to)
else:
    damaging_reverted = False
    
if reverted is None:
    rev_reverteds.append(('N/A', revid, 'N/A', damaging_reverted))  # Before Rev, Current Rev, After Rev
elif reverted is not None:

    rev_reverteds.append((reverted.reverteds[0]['parentid'], reverted.reverting['revid'], reverted.reverting['revid'],
                          damaging_reverted))
    # Before Rev, Before User, Current Rev, Current User, After Rev, After User
sys.stderr.write("r" if damaging_reverted else ".")

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

api_extractor = api.Extractor(session)
try:
    revData = list(api_extractor.extract(revid, features))
    revObserv = {"rev_id": revid, "cache": revData}
except:
    print('Revision Data Not Found')

#revObserv = json.dumps(revObserv)
#print(type(revObserv))
print('Revision Id: ' + str(revObserv['rev_id']))
print('Repeated Characters Added: ' + str(revObserv['cache'][0]))
print('Added Characters: ' + str(revObserv['cache'][1]))
print('Removed Characters: ' + str(revObserv['cache'][2]))
print('Proportional Number of Bad Words: ' + str(revObserv['cache'][3]))
print('Proportional Number of Informal Words: ' + str(revObserv['cache'][4]))
print('Change of Meaningful Words: ' + str(revObserv['cache'][5]))
print('User Anonymity: ' + str(revObserv['cache'][6]))
print('User Group: ' + str(revObserv['cache'][7]))
print('Registration Time: ' + str(revObserv['cache'][8]))