import fire
from ftplib import FTP


class FTPUtil(object):
    """A simple calculator class..

    Extended description of class

    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """

    def __init__(self, attr1: str, attr2: str) -> None:
        """コンストラクタ

        Extended description of function.

        Args:
            attr1 (str): パス付きでファイル名を与えてください。
            attr2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """

        super().__init__()
        self.attr1 = attr1
        self.attr2 = attr2

    def fileDownload(self, downloadFile: str):
        """ファイルのダウンロードを行います。

        Extended description of function.

        Args:
            downloadFile (str): パス付きでファイル名を与えてください。
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """

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
