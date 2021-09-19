# Imports the Cloud Logging client library
# import google.cloud.logging

# # Instantiates a client
# client = google.cloud.logging.Client()

# # Retrieves a Cloud Logging handler based on the environment
# # you're running in and integrates the handler with the
# # Python logging module. By default this captures all logs
# # at INFO level and higher
# client.get_default_handler()
# client.setup_logging()
# python標準のloggerと全然作り違うので、工夫する必要あり。

# Imports Python standard library logging
import logging
import os
import fire
import copy
from datetime import datetime

app_env = os.environ.get("APP_ENV")
log_dir = os.environ['LOG_DIR']

LOGGER = logging.getLogger('myLogger')

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# create console handler and set level to debug
stream = logging.StreamHandler()

# add formatter to stream
stream.setFormatter(copy.deepcopy(formatter))

# ファイルへの出力
filestream = logging.FileHandler(
    filename=os.path.join(log_dir, '{:%Y-%m-%d}.log'.format(datetime.now())),
    encoding='utf-8'
)
filestream.setFormatter(copy.deepcopy(formatter))

if app_env == 'production':

    LOGGER.setLevel(logging.INFO)

else:

    LOGGER.setLevel(logging.DEBUG)

# add steam to logger
LOGGER.addHandler(stream)

# add filestream to logger
LOGGER.addHandler(filestream)


def checkOutput(errorLevel: str, message='should print out such string.'):
    """エラーレベルにより出力をチェックしたいときに使ってください。

    Extended description of function.

    Args:
        errorLevel (str): 出力を見たいエラーレベルを書いてください。ERROR,WARN,INFO,DEBUGなど
        message (str): 出力したい文字列を入力してください。

    Examples:
        >>> checkOuput('ERROR')
        or
        >>> checkOutput('INFO','you want to check strings.')

    Note:
        setLevelで出力されない設定にされているエラーレベルは出力されません。
    """

    if errorLevel == 'ERROR':
        LOGGER.error('message="{}"'.format(message))
    elif errorLevel == 'WARNING':
        LOGGER.warning('message="{}"'.format(message))
    elif errorLevel == 'INFO':
        LOGGER.info('message="{}"'.format(message))
    elif errorLevel == 'DEBUG':
        LOGGER.debug('message="{}"'.format(message))
    else:
        LOGGER.error('message="not found such error level."')


def main():
    """シェルからのエントリーポイントです。

    Extended description of function.

    Examples:
        $ python3 logger.py ERROR
        $ python3 logger.py INFO 'you want to write message'

    Note:
        エラー処理はやっていないので、落ちたらダメになったタイミングで変更しましょう。
    """

    # 環境変数よりクラスの初期化パラメーター取得
    # ftp_host = os.environ['FTP_HOST']
    # ftp_user = os.environ['FTP_USER']
    # ftp_password = os.environ['FTP_PASSWORD']

    # インスタンス作成 and シェルから実行
    # ftpUtil = FTPUtil(host=ftp_host, user=ftp_user, passwd=ftp_password)
    # fire.Fire(ftpUtil)
    fire.Fire(checkOutput)


if __name__ == '__main__':
    main()
