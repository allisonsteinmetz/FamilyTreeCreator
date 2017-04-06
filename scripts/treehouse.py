import mysql.connector
from mysql.connector import errorcode

# MySQL database connection class
class TreeSQL:
    # Constructor
    def __init__(self, user = 'asantana048', password = 'Team2login!',
        host = 'test.cxyuwmmq4ydn.us-west-2.rds.amazonaws.com',
        db = 'testdb'):
        self.user = user
        self.password = password
        self.host = host
        self.db = db

    # Destructor
    def __del__(self):
        self.cnx.close()
        self.cursor.close()

    def connect(self):
        self.cnx = mysql.connector.connect(
            user = self.user,
            password = self.password,
            host = self.host,
            database = self.db)
        self.cursor = self.cnx.cursor(buffered=True)cc

    def make_change(self, statement):
        self.cursor.execute(statement)
        self.cnx.commit()

    def select_account(self, statement):
        self.cursor.execute(statement)
        for (email, username, password) in self.cursor:
            print "%s, %s, %s" % (email, username, password)
