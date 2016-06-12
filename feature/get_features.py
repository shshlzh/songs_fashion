#!/usr/bin/env python
# encoding=utf8

import time
from collections import defaultdict
from ConfigParser import SafeConfigParser

conf = SafeConfigParser()
conf.read('conf/main.cfg')


songs_file = conf.get('data', 'song')
fp_songs = open(songs_file)
target_artist_id = '0c80008b0a28d356026f4b1097041689'


def get_target_artist_songs(target_artist_id):
    '''songs'''
    all_songs_info_dict = {}
    for line in fp_songs:
        items = line.strip().split(',')
        song_id = items[0]
        artist_id = items[1]
        if artist_id != target_artist_id:
            continue
        publish_time = items[2]
        song_init_plays = items[3]
        language = items[4]
        gender = items[5]

        song_info = (publish_time, song_init_plays, language, gender)
        all_songs_info_dict[song_id] = song_info

    return all_songs_info_dict


def get_time_bucket(data_time):
    '''bucket'''

    bucket_items = conf.items('time_bucket')
    create_date, hour, week = data_time.strip().partition(' ')

    tb_hour = -1
    for tag, tb_key in bucket_items:
        tb_str, _, tb_value = tb_key.strip().partition(':')
        tb_list = tb_str.split(',')
        if len(tb_list) == 2 and tb_list[0] <= hour < tb_list[1]:
            tb_hour = int(tb_value)
            break
        if len(tb_list) == 1 and hour >= tb_list[0]:
            tb_hour = int(tb_value)
            break
    return (create_date, tb_hour, int(week))


def get_target_artist_user(target_songs_info_dict):
    '''user'''

    users_file = conf.get('data', 'user')
    fp_user = open(users_file)

    user_info_dict = defaultdict(list)
    format = '%Y-%m-%d %H %u'

    for line in fp_user:
        items = line.strip().split(',')
        song_id = items[1]
        gmt_create = float(items[2])
        if song_id not in target_songs_info_dict:
            continue
        song_info = target_songs_info_dict[song_id]

        gmt_day = time.gmtime(gmt_create)
        dt = time.strftime(format, gmt_day)

        time_key = get_time_bucket(dt)

        user_info_dict[time_key].append(song_info)

    for time_key in user_info_dict:
        user_songs = user_info_dict[time_key]
        user_cnt = len(user_songs)

        create_time, week, tb_hour = time_key



if __name__ == "__main__":
    get_time_bucket('')
    target_songs_info_dict = get_target_artist_songs(target_artist_id)
    get_target_artist_user(target_songs_info_dict)
