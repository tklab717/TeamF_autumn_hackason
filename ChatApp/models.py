import pymysql
from util.DB import DB

class dbConnect:
    #チームリスト情報の取得
    def getteamList(uid, year, season, team, github):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM teamLists WHERE uid=%s and year=%s and season=%s and team=%s and github=%s;"
            cur.execute(sql,(uid, year, season, team, github))
            teamList = cur.fetchone()
            return teamList
        except Exception as e:
            print(e+'が発生しています')
            abort(500)
        finally:
            cur.close()


    #マイページ登録情報のDB連携
    def selectTeam(uid, year, season, team, github):
        try:
            #teamListsからチャットルームへ進むを押した人のgithubリンクを入手
            conn = DB.getConnection()
            cur = conn.cursor()
            #channelsからgithubリンクが同じ（同じチーム）の人のルームを入手
            sql = "SELECT github FROM teamLists WHERE uid=%s AND year=%s AND season=%s AND team=%s AND github=%s;"
            cur.execute(sql, (uid, year, season, team, github))
            github = cur.fetchone()

            #githubでフィルタをかける
            sql = "SELECT uid FROM teamLists WHERE github =%s";
            #githubは辞書型のためkey指定する
            cur.execute(sql,(github['github']))
            #条件に合う全てのuidsを入手する
            uids = cur.fetchall()
            #uidsは辞書型のリストのため、keyを指定してタプル変換
            #（タプルに変換するのはSQLに変数として与えるため）
            uids_list = tuple(set([uids[idx]['uid'] for idx in range(len(uids))]))

            ##プレースホルダを動的作成
            #SQLへ記載する複数の%sを作成する
            stmt_formats = ','.join(['%s'] * len(uids_list))
            #channelsからuidを指定してchannelデータを入手する
            sql = "SELECT * FROM channels WHERE uid in (%s);"

            ##プリペアードステートメントを実行
            cur.execute(
                sql % stmt_formats,
                uids_list
            )
            #条件に合うすべてのチャネルを入手する
            channels = cur.fetchall()
            return channels

        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close() 

    #マイページ登録機能
    def createteamLists(uid, year, season, team, github):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO teamLists (uid, year, season, team, github) VALUES (%s, %s, %s, %s, %s);" 
            cur.execute(sql, (uid, year, season, team, github))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


#追加機能（集まれボタンを押した人のチーム員のメールアドレス入手）
    def getEmailGather(uid, year, season, team, github):
        try:
            #teamListsから集まれボタンが押した人のgithubリンクを入手
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT github FROM teamLists WHERE uid=%s AND year=%s AND season=%s AND team=%s AND github=%s;"
            cur.execute(sql, (uid,year,season,team,github))
            github = cur.fetchone()
            #teamListsからgithubリンクが同じ（同じチーム）の人のuidを入手
            sql = "SELECT uid FROM teamLists WHERE github=%s;"
            cur.execute(sql, (github['github']))
            uids = cur.fetchall()
            uids_list =  tuple(set([uids[idx]['uid'] for idx in range(len(uids))]))
            ## プレースホルダを動的作成
            stmt_formats = ','.join(['%s'] * len(uids_list))
            #usersからuidを指定してメールアドレスを入手。
            sql = "SELECT email FROM users WHERE uid in (%s);"
            ## プリペアードステートメント実行
            cur.execute(
                sql % stmt_formats, 
                uids_list)
            emails = cur.fetchall()
            email_list =  [emails[idx]['email'] for idx in range(len(emails))]
            return email_list
        
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)

        finally:
            cur.close()

    def createUser(uid, name, email, password):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (uid, name, email, password))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

#uidを指定して該当する名前を返す
    def getUserName(uid):
            try:
                conn = DB.getConnection()
                cur = conn.cursor()
                sql = "SELECT user_name FROM users WHERE uid=%s;"
                cur.execute(sql, (uid))
                name = cur.fetchone()
                return name
            except Exception as e:
                print(e + 'が発生しています')
                abort(500)
            finally:
                cur.close()

    def getUser(email):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    def getChannelAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels;"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    def getChannelById(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    def getChannelByName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    def addChannel(uid, newChannelName, newChannelDescription):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (uid, name, abstract) VALUES (%s, %s, %s);"
            cur.execute(sql, (uid, newChannelName, newChannelDescription))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    def getChannelByName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
        except Exception as e:
            print(e + 'が発生しました')
            abort(500)
        finally:
            cur.close()
            return channel

    def updateChannel(uid, newChannelName, newChannelDescription, cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
            cur.execute(sql, (uid, newChannelName, newChannelDescription, cid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しました')
            abort(500)
        finally:
            cur.close()


    #deleteチャンネル関数
    def deleteChannel(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id,u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    def createMessage(uid, cid, message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
            cur.execute(sql, (uid, cid, message))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    def deleteMessage(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM messages WHERE id=%s;"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()
