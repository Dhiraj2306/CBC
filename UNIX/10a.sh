# a) Shell script to display system information.

#!/bin/bash
echo "System Information"
echo "Hostname: $(hostname)"
echo "Operating System: $(uname -o)"
echo "Kernel Version: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Current User: $(whoami)"
echo "IP Address: $(ip -4 addr show | grep inet)”