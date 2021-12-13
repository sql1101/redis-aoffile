### redis-aoffile
这个小工具能直接解析aof 文件，主要用于redis的操作审计，故障恢复（如数据误删除操作）

### 安装
环境要求：
1. python 3+
2. hiredis 2+

### redis 版本
* redis 3 - redis 6

### 使用
```
usage: redis_aof.py [-h] --aof-file AOF_FILE [--key KEY_NAME] [--command-type COMMAND_TYPE]

Parse redis aof file to command you want

optional arguments:
  -h, --help            show this help message and exit
  --aof-file AOF_FILE   redis aof file to be parsed
  --key KEY_NAME        redis key name
  --command-type COMMAND_TYPE
                        Parse redis aof file to redis shell command
```
1. 全量解析aof 文件
```
python3 redis_aof.py  --aof-file /var/lib/redis/appendonly.aof
['SELECT', '0']
['set', 'a', '1;']
['set', 'a2', '1;']
['set', 'a3', '1;']
['set', 'a4', '1;']
['SELECT', '0']
['del', 'a']
['SELECT', '0']
['set', 'a3', '1000;']
['del', 'a3']
['SELECT', '10']
['set', 'b', '100']
['SELECT', '0']
['set', 'a4', '999']
['SELECT', '10']
['del', 'b']
['HSET', 'h1', 'a', '1']
['HSET', 'h1', 'b', '2']
['HSET', 'h1', 'c', '3']
```

2. 检索指定的key
```
python3 redis_aof.py  --aof-file /var/lib/redis/appendonly.aof --key a4
['set', 'a4', '1;']
['set', 'a4', '999']
```

3. 输出redis shell 命令格式
```
python3 redis_aof.py  --aof-file /var/lib/redis/appendonly.aof --key a4  --command-type shell
set a4 1;
set a4 999
```

#### 感谢
1. 感谢阿里云专家的支持
2. 感谢hiredis 开发者
* 本人代码能力有限，如果有代码有BUG和建议请与我联系，谢谢


