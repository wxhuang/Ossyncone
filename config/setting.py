# -*- coding: utf-8 -*-

# Copyright (c) 2012 Wu Tangsheng(lanbaba) <wuts73@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import os
import sys
import shutil
import ast


# OSS 连接参数
####################
# OSS              #
####################
def get_conf(path):
  if not os.path.isdir(path):
    raise Exception("invalid var path")
  config_path = os.path.join(path, 'conf') 
  if not os.path.exists(config_path):
    raise Exception("config file not found")
  s = open(config_path, 'r').read()
  return ast.literal_eval(s)
config_path = os.path.split(__file__)[0]
default_path = os.path.join(config_path, '../')
default_conf = get_conf(config_path)

if len(sys.argv) < 2:
  path = default_path
  g_conf = default_conf
else:
  path = sys.argv[1]
  g_conf = get_conf(path)

HOST = g_conf.has_key('HOST') and g_conf['HOST'] or default_conf['HOST']
ACCESS_ID = g_conf.has_key('ACCESS_ID') and g_conf['ACCESS_ID'] or default_conf['ACCESS_ID']
SECRET_ACCESS_KEY = g_conf.has_key('SECRET_ACCESS_KEY') and g_conf['SECRET_ACCESS_KEY'] or default_conf['SECRET_ACCESS_KEY']

# OSS Bucket和本地目录同步映射关系，一个Bucket对应一个或多个本地目录(local_folder)。
# 可以定义多个bucket。示例：
# oss_mappers = [{'bucket': 'dzdata', 'local_folders': ['/root/testdata/audios', '/root/testdata/docs']},
# {'bucket': 'privdata', 'local_folders': ['/root/testdata/images', '/root/testdata/pdfs']}]
####################
# OSS MAP          #
####################
oss_mappers = g_conf.has_key('OSS_MAPPERS') and g_conf['OSS_MAPPERS'] or default_conf['OSS_MAPPERS']
# 日志选项
####################
# LOGGING SETTING  #
####################
MAX_LOGFILE_SIZE = g_conf.has_key('MAX_LOGFILE_SIZE') and g_conf['MAX_LOGFILE_SIZE'] or default_conf['MAX_LOGFILE_SIZE']
# 默认日志文件大小为100M，每次达大小限制时，会自动加后缀生成备份文件
MAX_BACKUP_COUNT = g_conf.has_key('MAX_BACKUP_COUNT') and g_conf['MAX_BACKUP_COUNT'] or default_conf['MAX_BACKUP_COUNT']
# 默认备份文件为5个

# 上传文件或者删除object的最大重试次数
####################
# MAX_RETRIES      #
####################
MAX_RETRIES = g_conf.has_key('MAX_RETRIES') and g_conf['MAX_RETRIES'] or default_conf['MAX_RETRIES']

# 上传文件线程数
####################
# MAX_RETRIES      #
####################
NTHREADS = g_conf.has_key('NTHREADS') and g_conf['NTHREADS'] or default_conf['NTHREADS']

LOGFILE_PATH = os.path.join(path, "logs/app.log")
DB_PATH = os.path.join(path, "db/ossync.db")

LOG_DIR = os.path.split(LOGFILE_PATH)[0]
if not os.path.exists(LOG_DIR):
  os.mkdir(LOG_DIR)
  shutil.copyfile(os.path.join(config_path, "app.log.bak"), os.path.join(LOG_DIR, "app.log"))
DB_DIR = os.path.split(DB_PATH)[0]
if not os.path.exists(DB_DIR):
  os.mkdir(DB_DIR)
  shutil.copyfile(os.path.join(config_path, "ossync.db.bak"), os.path.join(DB_DIR, "ossync.db"))

