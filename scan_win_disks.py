#!/usr/bin/env python
import re
import subprocess
import json
import argparse
import sys

parser = argparse.ArgumentParser(description='Scan Windows host for existing disks')
parser.add_argument('-s','--source',
                    help="Source file",
                    default=None,
                    dest="source"
                    )
parser.add_argument('-o','--output',
                    help="Destination file",
                    default=None,
                    dest="output"
                    )
args = parser.parse_args()

host_array = []
host_disks = {}
lines = 0
prog = 0

for line in open(args.source).xreadlines( ): lines += 1

def progress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total), 1))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()

with open(args.source, 'r') as f:
        host = f.read().splitlines()
        host_array = host

for i in host_array:
        result = subprocess.Popen(["/opt/plugins/check_nrpe", "-H", i, "-c", "check_drivesize", "-a", "drive=all-drives", "filter=type in ('fixed', 'remote')", "show-all" ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        stdout, stderr = result.communicate()
        regex = re.compile(r'([A-Z]):\\ used\'=(\d+\.?\d*\w*;?){5}')
        host_disks[i] = [ d[0] for d in  regex.findall(stdout.strip())]
        prog += 1
        progress(prog, lines, status='status')

with open(args.output, 'w') as json_file:
        json_file.write(json.dumps([host_disks]))
