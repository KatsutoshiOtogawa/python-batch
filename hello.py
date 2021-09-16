import fire
from ftplib import FTP


def hello(name="World"):
    return "Hello %s!" % name


class Calculator(object):
    """A simple calculator class."""
    def double(self, number):
        return 2 * number


def fileDownload():
    with FTP(host='192.168.0.1', user='admin', passwd='admin') as ftp:
        # ftp.dir('/G/')
        ftp.cwd('/G/')
        with open("local.txt", "w") as f:
            ftp.retrlines("RETR /remote.txt", f.write)

# ftp = FTP('192.168.0.1')
# ftp.login('admin','admin')
# ftp.dir('/G/')


# ftp.nlst("/dir")
# アップロード
# テキストファイルでもバイナリモードで開く
# with open("local.txt", "rb") as f:
    # ftp.storlines("STOR /remote.txt", f)

if __name__ == '__main__':
    fire.Fire(hello)
    fire.Fire(Calculator)
