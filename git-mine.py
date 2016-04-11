#!/usr/bin/python

import hashlib
import time
import signal
import sys
from subprocess import check_output, Popen, PIPE

print "Mining commit:"

def graceful_exit(signal, frame):
    print "\tdone";
    sys.exit(0);
# exit quietly on CTRL+C
signal.signal(signal.SIGINT, graceful_exit)

def git_hash(object_data):
    "Calculate the commit ID for the given commit data"
    hash = hashlib.sha1()
    hash.update('commit %d\0' % len(object_data))
    hash.update(object_data)
    return hash.hexdigest()

def git_update(object_data):
    "Write the commit data to the git object store, and return the hex ID"
    git_pipe = Popen(['git', 'hash-object', '-t', 'commit', '--stdin', '-w'], stdin=PIPE, stdout=PIPE);
    return git_pipe.communicate(input=object_data)[0].strip();

head_id = check_output(['git', 'rev-parse', 'HEAD']).strip()
object_data = check_output(['git', 'cat-file', '-p', head_id])

best_hash = head_id;
counter = 0;
start_time = time.time()
hash_limit = False
if len(sys.argv) > 1:
    hash_limit = sys.argv[1]

while not hash_limit or best_hash >= hash_limit:
    candidate = "%s (%d)\n" % (object_data.strip(), counter)
    candidate_hash = git_hash(candidate)
    if (not best_hash or candidate_hash < best_hash):
        best_hash = candidate_hash
        hash_limit_reached = (hash_limit and best_hash < hash_limit);
        if time.time() < start_time + 0.5 and not hash_limit_reached:
            continue
        saved_hash = git_update(candidate)
        if saved_hash != candidate_hash:
            print "Error saving object to git"
            exit(1)
        # Move our HEAD to the new commit
        print "\t%i\t (%s)" % (counter, candidate_hash)
        check_output(['git', 'reset', '--soft', saved_hash]);
    counter += 1