import os
import fire
from ftplib import FTP
from .logger import LOGGER


class FTPUtil(object):
    """ FTPサーバーとのやりとりを表すclass

    Extended description of class

    Attributes:
        host (str): ログインするFTPサーバーのホスト名
        user (str): ログインするFTPサーバーのユーザー名
        passwd (str): ログインするFTPサーバーのパスワード
    """

    def __init__(self, host: str, user: str, passwd: str) -> None:
        """コンストラクタ

        Extended description of function.

        Args:
            host (str): ログインするFTPサーバーのホスト名
            user (str): ログインするFTPサーバーのユーザー名
            passwd (str): ログインするFTPサーバーのパスワード

        Returns:
            bool: Description of return value

        """

        super().__init__()
        self.host = host
        self.user = user
        self.passwd = passwd

    def fileDownload(self, downloadFile: str, destinationFile: str):
        """ファイルのダウンロードを行います。

        Extended description of function.

        Args:
            downloadFile (str): パス付きでファイル名を与えてください。
            destinationFile (str): 保存先をパス付きでファイル名を与えてください。

        Returns:
            bool: Description of return value

        Examples:
            >>> ftpUtil = FTPUtil(ftp_host, ftp_user, ftp_password)
            >>> ftpUtil.fileDownload('/G/remote.txt', 'docs/local.txt')

        Note:
            エラー処理はやっていないので、落ちたらダメになったタイミングで変更しましょう。
        """

        LOGGER.debug(downloadFile, destinationFile)
        # ファイル名とそのパスを取得
        basename = os.path.basename(downloadFile)
        dirname = os.path.dirname(downloadFile)
        with FTP(host=self.host, user=self.user, passwd=self.passwd) as ftp:
            ftp.cwd(dirname)
            with open(destinationFile, "w") as f:
                ftp.retrlines("RETR {}".format(basename), f.write)

    # ファイルのアップロードを行うバイナリファイルでもこれを使う。
    def fileUpload(self, uploadFile: str, destinationFile: str):
        """ファイルのダウンロードを行います。

        Extended description of function.

        Args:
            uploadFile (str): パス付きでアップロードするファイル名を与えてください。
            destinationFile (str): 保存先をパス付きでファイル名を与えてください。

        Returns:
            bool: Description of return value

        Examples:
            >>> ftpUtil = FTPUtil(ftp_host, ftp_user, ftp_password)
            >>> ftpUtil.fileUpload('docs/local.txt', '/G/remote.txt')

        Note:
            エラー処理はやっていないので、落ちたらダメになったタイミングで変更しましょう。
        """

        # ファイル名とそのパスを取得
        basename = os.path.basename(destinationFile)
        dirname = os.path.dirname(destinationFile)
        with FTP(host=self.host, user=self.user, passwd=self.passwd) as ftp:
            ftp.cwd(dirname)

            # テキストファイルでもバイナリモードで開く必要あり。
            with open(uploadFile, "rb") as f:
                ftp.storlines("STOR {}".format(basename), f)


def main():
    """シェルからのエントリーポイントです。

    Extended description of function.

    Examples:
        $ python3 ftputil.py fileDownload /G/remote.txt docs/local.txt
        $ python3 ftputil.py fileUpload docs/local.txt /G/remote.txt

    Note:
        エラー処理はやっていないので、落ちたらダメになったタイミングで変更しましょう。
    """

    # 環境変数よりクラスの初期化パラメーター取得
    ftp_host = os.environ['FTP_HOST']
    ftp_user = os.environ['FTP_USER']
    ftp_password = os.environ['FTP_PASSWORD']

    # インスタンス作成 and シェルから実行
    ftpUtil = FTPUtil(host=ftp_host, user=ftp_user, passwd=ftp_password)
    fire.Fire(ftpUtil)


if __name__ == '__main__':
    main()
