# Scan Windows disks

This script is used to scan a list of hosts to know how many disks are available.
The script should be copied to a poller system where the check_nrpe plugin is available.

The host file should list all the target ip's and only the ip's like:
```bash
10.0.0.1
10.0.0.48
10.0.0.64
```

## Usage:
```bash
python scan_win_disks -s [path to host list] -o [path where the output file should be stored]
```

The output is formatted as JSON.