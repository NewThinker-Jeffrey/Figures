#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import string
import time
import hashlib
import shutil
from datetime import datetime

url_prefix = "https://github.com/NewThinker-Jeffrey/Figures/raw/main/figures/"

def get_date_str(seconds_from_1970=-1, format='%Y-%m-%d__%H-%M-%S__%f'):
  if seconds_from_1970 < 0:
    seconds_from_1970 = time.time()
  date_time = datetime.utcfromtimestamp(seconds_from_1970)
  return datetime.strftime(date_time, format)

def random_str(len=16):
  return ''.join(random.choice(string.ascii_lowercase + string.digits)
                 for _ in range(len))

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check_figure_file(file_name):
  if not os.path.isfile(file_name):
    print("!!!! No such file: {}".format(file_name))
    return False
  if "." not in os.path.basename(file_name):
    print("!!!! No file suffix: {}".format(file_name))
    return False
  return True

def register_file(file_name):
  suffix = os.path.basename(file_name).split(".")[-1]
  md5sum = md5(file_name)
  registered_file_basename = md5sum + "." + suffix
  registered_file = os.path.join("figures", registered_file_basename)
  registered_url = url_prefix + registered_file_basename
  # shutil.copy2(file_name, registered_file)
  shutil.copyfile(file_name, registered_file)
  assert(md5(registered_file) == md5sum)
  return registered_file, registered_url

def main():
  if len(sys.argv) < 2:
    print("Usage: python {} <pic1.jpg> [<pic2.jpg>] ... ".format(sys.argv[0], ))
    sys.exit(1)
  my_dir = os.path.abspath(os.path.dirname(__file__))
  files = sys.argv[1:]
  for file_name in files:
    if not check_figure_file(file_name):
      sys.exit(2)
  abs_files = [ os.path.abspath(file_name) for file_name in files ]

  os.chdir(my_dir)
  registered_files = []
  registered_urls = []
  for file_name in abs_files:
    registered_file, registered_url = register_file(file_name)
    registered_files.append(registered_file)
    registered_urls.append(registered_url)
  
  strlines = []
  strlines.append("============  {}".format(get_date_str()))
  for file_name, url in zip(abs_files, registered_urls):
    strlines.append("+++ {}".format(file_name))
    strlines.append("> ![]({})".format(url))
  print("\n".join(strlines))

  for registered_file in registered_files:
    assert(0 == os.system("git add {}".format(registered_file)))
  assert(0 == os.system("git commit -m \"add {}\"".format(", ".join(registered_files))))
  assert(0 == os.system("git push"))

  logfile = os.path.join(my_dir, "log.txt")
  with open(logfile, "a") as stream:
    stream.write("\n")
    stream.write("\n".join(strlines))
    stream.write("\n")

  print("\n\n\n")
  print("\n".join(strlines))

if __name__ == "__main__":
  main()