#!/bin/bash
#set -e

uid=$1 #${1:-1000}
nbRuns=$2
configName=$3
evalFile=$4
shift; shift; shift; shift;

useradd -d /home/user -Ms /bin/bash -u $uid user
chown -R $uid /home/user

echo running as $uid

if [ -n "$evalFile" ]; then
	evalFile="-e $evalFile"
fi

# Launch illumination.
exec bash -c "cd /home/user/daccadevo; PYTHONPATH=$PYTHONPATH:/home/user/daccadevo python3 -m daccadevo.DACCADRun -c $configName -r $nbRuns $evalFile"


