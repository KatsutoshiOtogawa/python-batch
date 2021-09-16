
# cant use interactive settings in vagrant provision.
export DEBIAN_FRONTEND=noninteractive

# 環境変数読み込み
cat /vagrant/.env | sed 's/# .*$//' | xargs -I {} echo export {} >> /home/vagrant/.bashrc
cat /vagrant/.env | sed 's/# .*$//' | xargs -I {} echo export {} >> ~/.bashrc
source ~/.bashrc

apt update && apt upgrade -y 

# fix for mojibake
apt install -y nkf

# set Asia/Tokyo
timedatectl set-timezone Asia/Tokyo

apt install -y python3-pip \
    && pip3 install pipenv

# vscodeが/usr/local/bin/pythonのpythonを見ているのでそちらにインストール
ln -s /usr/bin/python  /usr/local/bin/python

# vscodeのextensionはグローバルにインストールしたもののみ対応なので、
# グローバルにインストールする。
pip3 install flake8 \
    && pip3 install flake8 \
    && pip3 install autopep8 \
    && pip3 install pytest

# chromeで使うamd64bitに依存するパッケージをインストールするためにamd64bitを有効化
dpkg --add-architecture amd64 \
    && dpkg --print-foreign-architectures \
    && apt-get update

# RUN apt install -y libappindicator1 fonts-liberation libasound2 libnspr4 libnss3 libxss1 lsb-release xdg-utils
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm ./google-chrome-stable_current_amd64.deb

# 日本語のフォントを入れるために必要。入れないとchromeが文字化けする
apt install -y task-japanese \
    && locale-gen ja_JP.UTF-8 \
    && localedef -f UTF-8 -i ja_JP ja_JP

apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# set bash function
su - vagrant -c 'cat < /vagrant/function.sh >> ~/.bashrc'

su - vagrant -c 'pipenv lock --requirements > requirements.txt && pip3 install -r requirements.txt'
