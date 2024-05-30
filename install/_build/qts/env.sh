#!/usr/bin/env bash
### Primary variables
srv_home="/share/CACHEDEV1_DATA/srv"
project="mantisanalyzer"
base_dir="/share/CACHEDEV1_DATA/runes/$project"

if ! [[ $USER == "stanley" || $USER == "admin" ]]; then
        exec > $srv_home/$project/env.log 2>&1
  echo "exec > $srv_home/$project/env.log 2>&1"
fi
whoami

echo '### Primary variables'
echo 'srv_home: ' $srv_home
echo 'project: ' $project
echo 'base_dir: ' $base_dir

### Environment variables directed from primary ones
export src=$base_dir/app
export config=$base_dir/base
export apphome=$srv_home/$project

echo '### Environment variables directed from primary ones'
echo 'src: ' $src
echo 'config: ' $config
echo 'apphome: ' $apphome

### Python3
if ! [[ ":$PATH:" == *":/opt/python3/bin/:"* ]]; then
  echo "export PATH=$PATH:/opt/python3/bin/"
        export PATH=$PATH:/opt/python3/bin/
fi

if ! [ -f /opt/python3/bin/pip ]; then
  echo "sudo ln /opt/python3/bin/pip3 /opt/python3/bin/pip"
        sudo ln /opt/python3/bin/pip3 /opt/python3/bin/pip
fi


### crontab
# if grep -q "$apphome/scripts/run.sh" "/etc/config/crontab"; then
#   echo ""
# else
#   echo "echo \"0 */1 * * * . $apphome/scripts/env.sh && $apphome/scripts/run.sh\" >> \"/etc/config/crontab\""
#         echo  "0 */1 * * * . $apphome/scripts/env.sh && $apphome/scripts/run.sh"  >>  "/etc/config/crontab"
#   echo "sudo crontab /etc/config/crontab && sudo /etc/init.d/crond.sh restart"
#         sudo crontab /etc/config/crontab && sudo /etc/init.d/crond.sh restart
#   echo "sudo crontab -l | grep $project"
#         sudo crontab -l | grep $project
# fi
