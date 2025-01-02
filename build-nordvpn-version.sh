#!/bin/bash

rm -rf nordvpn-version
git clone https://github.com/egandro/nordvpn-proxy.git nordvpn-version
cd nordvpn-version
git checkout develop
rm -rf .git
rm -rf app/privoxy
mkdir -p app/scraper
cp ../requirements.txt app/scraper
cp ../main.py app/scraper
sed -i 's/8118/5000/g' Dockerfile
sed -i 's/8118/5000/g' docker-compose.yml
sed -i 's/PROXY_PORT/PORT/g' docker-compose.yml
sed -i 's/8118/5000/g' env.txt
sed -i 's/PROXY_PORT/PORT/g' env.txt
sed -i 's/unzip/unzip python3 py3-pip/g' Dockerfile

cat <<EOF > app/scraper/run
#!/bin/bash
python3 -m pip config set global.break-system-packages true
pip install --no-cache-dir -r requirements.txt
python3 main.py
EOF
