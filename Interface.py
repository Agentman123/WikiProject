import random
from revscoring.features import wikitext, revision_oriented, temporal
from revscoring.languages import english
from revscoring.extractors import api
from revscoring.utilities.util import read_observations
import mwapi
import json
import sys, traceback
import mwreverts.api

revid = random.randint(60000000, 90000000)
url = 'https://en.wikipedia.org/?diff={0}'.format(revid)
session = mwapi.Session('https://en.wikipedia.org')
rev_reverteds = []

try:
    _, reverted, reverted_to = mwreverts.api.check(
        session, revid, radius=5,  # most reverts within 5 edits
        window=48 * 60 * 60,  # 2 days
        rvprop={'user', 'ids'})  # Some properties we'll make use of
except (RuntimeError, KeyError) as e:
    sys.stderr.write(str(e))

if reverted is not None:
    reverted_doc = [r for r in reverted.reverteds if r['revid'] == revid][0]

    if 'user' not in reverted_doc or 'user' not in reverted.reverting:

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
    revData = list(api_extractor.extract(url, features))
    revObserv = {"rev_id": revid, "cache": revData}
except:
    print('Revision Data Not Found')

revObserv = json.dumps(revObserv)
print(revObserv)