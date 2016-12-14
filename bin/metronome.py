#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    metronome bot
'''

__author__ = 'Matt Joyce'
__email__ = 'matt.joyce@symphony.com'
__copyright__ = 'Copyright 2016, Symphony'

import argparse
import datetime
import json
import logging
import symphony
import sys
import time
import uuid


def get_counter():
    ''' get current count '''
    cachefile = open('/var/cache/metronome/counter', 'r')
    count = cachefile.read().rstrip()
    count = int(count)
    cachefile.close()
    return count


def inc_counter():
    ''' increment the counter '''
    cachefile = open('/var/cache/metronome/counter', 'r+')
    count = get_counter()
    count += 1
    cachefile.seek(0)
    count = str(count)
    cachefile.write(count)
    cachefile.close()
    return count


def main():
    ''' main program loop '''
    # CLI flag parsing
    parser = argparse.ArgumentParser(description='metronome bot')
    # specify config file
    parser.add_argument(
        '-c', '--config', nargs='?',
        help='specify path to config file',
        default='/etc/metronome/metronome.cfg'
    )
    # specify logging file
    parser.add_argument(
        '-l', '--log', nargs='?',
        help='specify path to log file',
        default='/var/log/metronome/metronome.log'
    )
    # specify debug logging
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='debug logging'
    )
    # specify cache counter file
    parser.add_argument(
        '--counter', nargs='?',
        help='specify path to cache counter',
        default='/var/cache/metronome/counter'
    )
    # parse
    try:
        args = parser.parse_args()
    except Exception as err:
        print('failed to parse arguments: %s' % (err))
        sys.exit(1)
    # silence INFO alerts from requests module
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    # toggle on debug flag
    if args.debug is False:
        logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s %(message)s')
    else:
        logging.basicConfig(filename=args.log, level=logging.DEBUG, format='%(asctime)s %(message)s')

    # run configuration
    conn = symphony.Config(str(args.config))
    # connect to pod
    try:
        agent, pod, symphony_sid = conn.connect()
    except Exception as err:
        print('failed to connect to symphony: %s' % (err))
        sys.exit(1)
    # get datafeed
    try:
        datafeed_id = agent.create_datafeed()
        print(datafeed_id)
    except Exception as err:
        print('failed to allocate datafeed id: %s' % (err))
        sys.exit(1)
    # main loop
    while True:
        # this polls and returns a list of alert ids
        try:
            # increment counter and initiate sleep cycle
            inc_counter()
            time.sleep(5)
            # accept pending connection requests
            connection_resp = pod.list_connections()
            for request in connection_resp:
                if request['status'] == 'PENDING_INCOMING':
                    pod.accept_connection(request['userId'])
            # perform user search globally
            search_filter = {"company": "Symphony Corporate"}
            local = 'false'
            search_resp, search_ret = pod.search_user('maximilian', search_filter, local)
            search_data = json.loads(search_ret)
            searched_count = search_data['count']
            searched_id = search_data['users'][0]['id']
            searched_email = search_data['users'][0]['emailAddress']
            searched_name = search_data['users'][0]['displayName']
            search_stats = '%s results found, showing first : (%s) %s - %s'\
                           % (searched_count, searched_id, searched_name, searched_email)
            # check counter
            count = get_counter()
            # build polling message
            msgFormat = 'MESSAGEML'
            message = '<messageML><b>%s ( %s )</b> <i>%s</i> \
                       %s - search maximilian - <b> %s </b> : <i> %s </i> </messageML>'\
                      % ('tick',
                         str(count),
                         datetime.datetime.now(),
                         uuid.uuid4(),
                         str(search_resp),
                         search_stats)
            # send message
            retstring = agent.send_message(symphony_sid, msgFormat, message)
            print(retstring)
        # if main loop fails... try to reconnect
        except Exception as err:
            try:
                datafeed_id = agent.create_datafeed()
            except:
                agent, pod, symphony_sid = conn.connect()
            logging.error("failed to run main loop: %s" % err)


if __name__ == "__main__":
    main()
