# env

python3 -m venv .venv
. .venv/bin/activate

# install package

pip3 install -r requirements.txt

# update package

pip3 freeze > requirements.txt

# alert TWII

python3 twii_alert.py

# docker build

docker build -t twii_alert .

# docker run

docker run -it --rm twii_alert
