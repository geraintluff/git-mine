#!/usr/bin/python

import hashlib
import time
import signal
import sys
import re
from subprocess import check_output, Popen, PIPE

print "Mining commit:"

DEFAULT_LIMIT = '0001'
DEFAULT_LOWER_LIMIT = '0'

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
object_data_parts = object_data.split('\n\n', 1)
object_data_prefix = re.sub('\nnonce [^\n]+', '', object_data_parts[0]);
object_data_suffix = object_data_parts[1]

best_hash = head_id;
counter = 0;
start_time = time.time()
hash_limit = DEFAULT_LIMIT
hash_lower_limit = DEFAULT_LOWER_LIMIT
if len(sys.argv) > 1:
    hash_limit = sys.argv[1]
if len(sys.argv) > 2:
    hash_lower_limit = sys.argv[2]
if best_hash < hash_lower_limit:
    best_hash = 'f'*40;
    
while not hash_limit or best_hash >= hash_limit:
    candidate = "%s\nnonce %d\n\n%s" % (object_data_prefix, counter, object_data_suffix)
    candidate_hash = git_hash(candidate)
    if candidate_hash >= hash_lower_limit and (not best_hash or candidate_hash < best_hash):
        best_hash = candidate_hash
        hash_limit_reached = (hash_limit and best_hash < hash_limit);

        # Don't bother with initial discoveries unless we've reached the limit
        if time.time() < start_time + 0.5 and not hash_limit_reached:
            continue

        saved_hash = git_update(candidate)
        if saved_hash != candidate_hash:
            print "Error saving object to git"
            exit(1)
        # Move our HEAD to the new commit
        print "\t%d\t (%s)" % (counter, candidate_hash)
        check_output(['git', 'reset', '--soft', saved_hash]);
    counter += 1
