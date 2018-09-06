set -e
cd /RLProject
git clone -b docker https://github.com/ermekaitygulov/gym-crumb/
. /opt/conda/etc/profile.d/conda.sh
conda activate base
cd gym-crumb/gym-crumb && pip install -e .
cd /
Xvfb :1 -screen 0 1600x1200x16  &
export DISPLAY=:1.0
jupyter notebook --ip 0.0.0.0 --port 8800 --no-browser --allow-root &
exec "$@"
