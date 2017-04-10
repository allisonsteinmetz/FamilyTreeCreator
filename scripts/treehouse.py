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
        self.cnx = None
        self.cursor = None

    # Destructor
    def __del__(self):
        if (self.cnx != None):
            self.disconnect()

    # Create a connection to the database
    # IMPORTANT: must be called before any other method here
    def connect(self):
        if (self.cnx != None):
            self.disconnect()

        try:
            self.cnx = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.db)
            self.cursor = self.cnx.cursor(buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    # End the connection to the database
    def disconnect(self):
        self.cnx.close()
        self.cursor.close()

    # Execute any statement that changes the database
    def exec_change(self, statement):
        self.cursor.execute(statement)
        self.cnx.commit()

    # Drop a table
    def drop(self, table_name):
        sql_string = "DROP TABLE IF EXISTS %s" % table_name
        self.exec_change(sql_string)

    ### Account table methods

    # Select all entries in account
    def select_account(self):
        self.cursor.execute("SELECT * FROM Account")
        for (email, username, password) in self.cursor:
            print "%s, %s, %s" % (email, username, password)

    ### Treelist table methods


    ### Family table methods

    # Create a family table
    def create_family(self, family_name, family_id):
        table_name = str(family_name) + str(family_id)
        sql_string = (
            "CREATE TABLE %s("
            "personID INT NOT NULL AUTOINCREMENT,"
            "motherID INT,"
            "fatherID INT,"
            "name VARCHAR(50) NOT NULL,"
            "gender CHAR(1) NOT NULL,"
            "PRIMARY KEY(personID)"
            ") ENGINE=InnoDB"
        ) % table_name.lower()
        self.exec_change(sql_string)

    # Drop a family table
    def drop_family(self, family_name, family_id):
        table_name = str(family_name) + str(family_id)
        self.drop(table_name)
    #
