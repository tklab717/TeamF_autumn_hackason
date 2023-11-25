import pymysql
from util.SSM import SSM

REGION = 'ap-northeast-1'

class DB:
    def getConnection():
        try:
            try:
                REGION_now = SSM.get_parameters('RDS-REGION')
                conn = pymysql.connect(
                host=SSM.get_parameters('RDS-HOST'),
                db="chatapp",
                user=SSM.get_parameters('RDS-USER'),
                password=SSM.get_parameters('RDS-PASS'),
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
                )
                return conn
            except:
                print("Localコンディション")
                conn = pymysql.connect(
                host="db",
                db="chatapp",
                user="testuser",
                password="testuser",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
                )
                return conn
        except (ConnectionError):
            print("コネクションエラーです")
            conn.close()