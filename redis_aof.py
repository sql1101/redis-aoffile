#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：xushaohui time:2021/12/31


from redis import Redis
from rediscluster import RedisCluster
import argparse
import sys
def parse_args():
    parser = argparse.ArgumentParser(description='example: python3 RedisOpsKey.py --match "a*"')
    parser.add_argument('--match', dest='match', type=str,default='*',required=False, help='scan match parse default:*')
    parser.add_argument('--host', dest='host', type=str,default='127.0.0.1',required=False, help='redis host ip default:127.0.0.1')
    parser.add_argument('--port', dest='port', type=str,default='6379',required=False, help='redis host port default:6379')
    parser.add_argument('--password', dest='password', type=str,default=None,required=False, help='redis host password default:None')
    parser.add_argument('--mode', dest='mode', type=str,default='standalone',required=False, help='redis mode, option:standalone(default) or cluster')
    parser.add_argument('--delete', dest='delete', type=str,default=None,required=False, help='redis key delete, option:yes or None(default) ')
    parser.add_argument('--db', dest='db', type=str,default=None,required=False, help='redis databases')

    return parser


def RedisOpsKey(host,port,match_args,password=None,mode='standalone',del_mode=None,db=None):
    redis_mode = mode
    if redis_mode =='standalone':
        if db is None:
            client = Redis(host=host, port=port, password=password, db=0)
            database_number = client.config_get('databases').get('databases')
            client.close()

            for db in range(int(database_number)):
                cursor, counts = 0, 0
                client = Redis(host=host, port=port, password=password, db=db)
                while True:
                    cursor, keys = client.scan(cursor, match=match_args, count=100)
                    counts += len(keys)
                    for key in keys:
                        print(key.decode("utf-8"))
                        if del_mode == 'yes':
                            client.delete(key)
                            print("del key:%s success" % (key.decode("utf-8")))
                    if cursor == 0:
                        break
                if counts != 0:
                    print("database:%s Total Key Number:%s" % (db, counts))
                    print('\n')
                client.close()
        else:
            cursor, counts = 0, 0
            client = Redis(host=host, port=port, password=password, db=db)
            while True:
                cursor, keys = client.scan(cursor, match=match_args, count=100)
                counts += len(keys)
                for key in keys:
                    print(key.decode("utf-8"))
                    if del_mode == 'yes':
                        client.delete(key)
                        print("del key:%s success" % (key.decode("utf-8")))
                if cursor == 0:
                    break
            if counts != 0:
                print("database:%s Total Key Number:%s" % (db, counts))
                print('\n')
            client.close()



    else:
        cursor, counts = 0, 0
        client = RedisCluster(host=host, port=port,password=password,decode_responses=True)
        keys = client.scan_iter(match_args)
        for key in keys:
            print(key)
            if del_mode == 'yes':
                client.delete(key)
                print("del key:%s success" % (key))
            counts += 1
        if counts != 0:
            print('\n')
            print("Total Key Number:%s" % ( counts))
        client.close()



if __name__ == '__main__':
    parse = parse_args()
    if len(sys.argv) < 2:
        parse.print_help()
        sys.exit(1)
    else:
        args = parse_args().parse_args()
        RedisOpsKey(host=args.host,port=args.port,match_args=args.match,password=args.password,mode=args.mode,del_mode=args.delete,db=args.db)


