import os, sys

if len(sys.argv) < 2:
    print('Usage: prepare.py <prefix> <new>')
    exit()

prefix = sys.argv[1]
new = sys.argv[2]
files = os.listdir()

for f in files:
  if f.startswith(prefix):
    name = f.replace(prefix,new)
    try:
      os.rename(f, name)
    except Exception:
      print('Failed to rename file: ' + f + ' to ' + name)
