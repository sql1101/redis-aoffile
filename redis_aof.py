#! /usr/bin/env python3
#coding=utf-8
"""
Redis appendonly file parser
"""
import hiredis
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Parse redis aof file to command you want')
    parser.add_argument('--aof-file', dest='aof_file', type=str,required=True, help='redis aof file to be parsed')
    parser.add_argument('--key', dest='key_name', default=False, help='redis key name')
    parser.add_argument('--command-type', dest='command_type', default=False, help='Parse redis aof file to redis shell command')
    args = parser.parse_args()
    return args

def redis_command(command,key,command_shell):

    if key:
        if command[1] == key:
            if command_shell == 'shell':
                print(" ".join(command))
            else:
                print(command)
    else:
        if command_shell == 'shell':
            print(" ".join(command))
        else:
            print(command)


def parser_aoffile(aoffile,key=False,command_shell=False):
    file = open(aoffile, 'rb')
    line = file.readline()
    request_command = line

    while line:
        try:
            reader = hiredis.Reader()
            reader.setmaxbuf(0)
            reader.feed(request_command)
            command = reader.gets()
            if command is not False:
                if isinstance(command,list):
                    command = [c.decode('utf-8') for c in command]
                    redis_command(command,key,command_shell)
                request_command = b''
        except hiredis.ProtocolError as e:
            print('protocol error :%s' % (e))
        line = file.readline()
        request_command += line
    file.close

if __name__ == '__main__':

    args = parse_args()
    parser_aoffile(args.aof_file,args.key_name,args.command_type)
