#!/usr/bin/env python
# encoding=utf8

from ConfigParser import SafeConfigParser

conf = SafeConfigParser()
conf.read('conf/main.cfg')

song_file = conf.get('data', 'song')

user_file = conf.get('data', 'user')
print song_file, user_file


import datetime
import random

def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d%02d%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result

predict_date_list = datelist((2015,9,1), (2015, 10, 30)) 



song_artist_dict = {}
for line in open(song_file):
    items = line.strip().split(',')
    song_id = items[0]
    artist_id = items[1]
    song_artist_dict[song_id] = artist_id

from collections import Counter, defaultdict
import time



artist_cnt_dict = defaultdict(list)
for line in open(user_file):
    items = line.strip().split(',')
    song_id = items[1]
    ds = items[4]


    artist_id = song_artist_dict[song_id]
    artist_cnt_dict[artist_id].append(ds)

for artist_id in artist_cnt_dict:

    actions_date_list = artist_cnt_dict[artist_id]

    actions_date_cnt_dict = Counter(actions_date_list)

    for data_date in actions_date_cnt_dict:
        print '%s,%s,%s' % (artist_id, data_date, actions_date_cnt_dict[data_date])



