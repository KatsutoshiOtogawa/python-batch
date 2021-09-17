import fire
from ftplib import FTP


class FTPUtil(object):
    """A simple calculator class."""

    # ファイルのダウンロードを行う。
    def fileDownload(self, downloadFile):
        with FTP(host='192.168.0.1', user='admin', passwd='admin') as ftp:
            ftp.cwd('/G/')
            with open("local.txt", "w") as f:
                ftp.retrlines("RETR remote.txt", f.write)

    # ファイルのアップロードを行うバイナリファイルでもこれを使う。
    def fileUpload(self):
        with FTP(host='192.168.0.1', user='admin', passwd='admin') as ftp:
            ftp.cwd('/G/')

            # テキストファイルでもバイナリモードで開く必要あり。
            with open("local.txt", "rb") as f:
                ftp.storlines("STOR remote.txt", f)


def main():
    ftpUtil = FTPUtil()
    fire.Fire(ftpUtil)


if __name__ == '__main__':
    main()
