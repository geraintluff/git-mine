#!/usr/bin/python

import hashlib
import time
from subprocess import check_output, Popen, PIPE

def git_hash(object_data):
    hash = hashlib.sha1()
    hash.update('commit %d\0' % len(object_data))
    hash.update(object_data)
    return hash.hexdigest()

def git_update(object_data):
    git_pipe = Popen(['git', 'hash-object', '-t', 'commit', '--stdin', '-w'], stdin=PIPE, stdout=PIPE);
    return git_pipe.communicate(input=object_data)[0];

head_id = check_output(['git', 'rev-parse', 'HEAD']).strip()
object_data = check_output(['git', 'cat-file', '-p', head_id])

best_hash = head_id;
counter = 0;
start_time = time.time()

while True:
    candidate = object_data + str(counter) + '\n'
    candidate_hash = git_hash(candidate)
    if (not best_hash or candidate_hash < best_hash):
        best_hash = candidate_hash
        print "%i\t (%s)" % (counter, candidate_hash)
        # Save the new hash into git's object store
        saved_hash = git_update(candidate).strip()
        if saved_hash != candidate_hash and time.time() > start_time + 2:
            print "Error saving object to git"
            exit(1)
        # Move our HEAD to the new commit
        check_output(['git', 'reset', '--soft', saved_hash]);
    counter += 1
