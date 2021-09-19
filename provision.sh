
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

# aptのpipenvだと不具合があるので、python3-pip経由でpipenvをインストールすること。
apt install -y python3-pip \
    && pip3 install pipenv


# postgresql クライアント用のやつを使う
apt install -y postgresql \
    libpq-dev \
    python3-dev

# vscodeが/usr/local/bin/pythonのpythonを見ているのでそちらにインストール
# 
ln -s /usr/bin/python3 /usr/local/bin/python

# vscodeのextensionはグローバルにインストールしたもののみ対応なので、
# グローバルにインストールする。
pip3 install \
    flake8 \
    autopep8 \
    pytest \

ln -s /usr/bin/flake8 /usr/local/bin/flake8
ln -s /usr/bin/autopep8 /usr/local/bin/autopep8
ln -s /usr/bin/pytest /usr/local/bin/pytest

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

# python仮想環境を使わないので~/.local/binへのパスが必要になる。
su - vagrant -c 'echo PATH=$PATH:$HOME/.local/bin >> ~/.bashrc'

# 仮想環境内なのでpipenvによるpython仮想環境を使わない。
su - vagrant -c 'echo export PIPENV_IGNORE_VIRTUALENVS=1 >> ~/.bashrc' 

su - vagrant -s /bin/bash << END
cd /vagrant/
pipenv lock --requirements --dev > requirements.txt
pip3 install -r requirements.txt
END
