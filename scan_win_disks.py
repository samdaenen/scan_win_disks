import re
import subprocess
import json

hostlist = raw_input("Location of the hostlist: ")
output = raw_input("Where should i place the export file?")
host_array = []
host_disks = {}
listing = {}

with open(hostlist, 'r') as f:
        host = f.read().splitlines()
        host_array = host

for i in host_array:
        result = subprocess.Popen(["/opt/plugins/check_nrpe", "-H", i, "-c", "check_drivesize", "-a", "drive=all-drives", "filter=type in ('fixed', 'remote')", "show-all" ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        stdout, stderr = result.communicate()
        regex = re.compile(r'([A-Z]):\\ used\'=(\d+\.?\d*\w*;?){5}')
        host_disks[i] = [ d[0] for d in  regex.findall(stdout.strip())]
        with open(output, 'w') as json_file:
                json_file.write(json.dumps([host_disks]))
