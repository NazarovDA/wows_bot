import sqlite3


class SQLiter:
    def __init__(self):
        self.__connection = sqlite3.connect('mailing.db')
        self.__cursor = self.__connection.cursor()

        try:
            self.__cursor.execute("""
            CREATE TABLE players (
            inGameNickname STRING PRIMARY KEY UNIQUE NOT NULL,
            discordNickname STRING UNIQUE NOT NULL,
            player_id STRING NOT NULL UNIQUE,
            is_subcribed BOOLEAN NOT NULL)
            """)
            self.__connection.commit()
        except sqlite3.OperationalError:
            pass

    def add(self, inGameNickname, discordNickname, playerId):
        sql = f"INSERT INTO players VALUES({inGameNickname}, {str(discordNickname)}, {playerId}, TRUE)"
        print(sql)
        print(str(discordNickname))
        print(type(str(discordNickname)))
        self.__cursor.execute(sql)
        self.__connection.commit()

    def findAllSubscribed(self):
        self.__cursor.execute("""SELECT inGameNickName, player_id FROM players WHERE is_subcribed=TRUE""")
        result = self.__cursor.fetchall()
        return result

    def unSubscribe(self, discordNickname):
        self.__cursor.execute(f"""UPDATE players SET is_subscribed = FALSE WHERE discordNickname={discordNickname}""")
        self.__connection.commit()

    def subscribe(self, discordNickname):
        self.__cursor.execute(f"""UPDATE players SET is_subscribed = TRUE WHERE discordNickname={discordNickname}""")
        self.__connection.commit()
