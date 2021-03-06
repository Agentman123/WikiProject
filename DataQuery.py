import requests
import sys, traceback
import mwreverts.api
import mwapi
import csv
import types

urllink = 'https://quarry.wmflabs.org/run/293187/output/0/csv'
revids_f = requests.get(urllink)
x = 8
y = 17
revids = []
for i in range(20000):
    revids.append(int(revids_f.text[x:y]))
    x += 11
    y += 11
session = mwapi.Session("https://en.wikipedia.org")
rev_reverteds = []

for rev_id in revids[18000:20000]:  # NOTE: Limiting to sets of 2000
    try:
        _, reverted, reverted_to = mwreverts.api.check(
            session, rev_id, radius=5,  # most reverts within 5 edits
            window=48 * 60 * 60,  # 2 days
            rvprop={'user', 'ids'})  # Some properties we'll make use of
    except (RuntimeError, KeyError) as e:
        sys.stderr.write(str(e))
        continue

    if reverted is not None:
        reverted_doc = [r for r in reverted.reverteds
                        if r['revid'] == rev_id][0]
        #print(rev_id)
        #print(reverted)
        #print(reverted.reverting['user'])
        #print(reverted.reverteds[0]['user'])
        #print(reverted.reverted_to['user'])

        if 'user' not in reverted_doc or 'user' not in reverted.reverting:
            continue
        self_revert = \
            reverted_doc['user'] == reverted.reverting['user']

        # revisions that are reverted back to by others
        reverted_back_to = \
            reverted_to is not None and \
            'user' in reverted_to.reverting and \
            reverted_doc['user'] != \
            reverted_to.reverting['user']

        # If we are reverted, not by self or reverted back to by someone else,
        # then, let's assume it was damaging.
        damaging_reverted = not (self_revert or reverted_back_to)
    else:
        damaging_reverted = False

    if reverted is None:
        rev_reverteds.append(('N/A', rev_id, 'N/A', damaging_reverted)) #Before Rev, Current Rev, After Rev
    elif reverted is not None:

        rev_reverteds.append((reverted.reverteds[0]['parentid'], reverted.reverting['revid'], reverted.reverting['revid'], damaging_reverted))
            #Before Rev, Before User, Current Rev, Current User, After Rev, After User
    sys.stderr.write("r" if damaging_reverted else ".")

with open('data10.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(rev_reverteds)):
        writer.writerow(rev_reverteds[i])