import mysql.connector
from mysql.connector import errorcode
import json

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
                print "Something is wrong with your user name or password."
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist."
            else:
                print err

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


    ##### Account table methods

    # Create new Account
    def insert_account(self, *args):
        sql_string = ""
        if len(args) == 2:
            sql_string = "INSERT INTO Account (email, password) VALUES ('%s','%s')" % (args[0], args[1])
        elif len(args)== 3:
            sql_string = "INSERT INTO Account (email, username, password) VALUES ('%s','%s', '%s')" % (args[0], args[1], args[2])

        try:      
            self.exec_change(sql_string)
        except mysql.connector.Error as err:
            print err

    # Select all entries in Account
    def select_account(self):
        self.cursor.execute("SELECT * FROM Account")
        for (email, username, password) in self.cursor:
            print "%s, %s, %s" % (email, username, password)


    ##### Treelist table methods

    # Insert an entry in Treelist
    def insert_treehouse(self, email, treeName):
        try:
            sql_string = "INSERT INTO Treelist (email, treeName) VALUES ('%s', '%s')" % (email, treeName)
            self.exec_change(sql_string)

            sql_string = "SELECT treeID FROM Treelist WHERE email = '%s' AND treeName = '%s'" % (email, treeName)
            for treeID in self.cursor:
                create_family(treeName, treeID)

        except mysql.connector.Error as err:
            print err

    # Select family table names
    def select_families_for_account(self, email):
        sql_string = "SELECT treeName FROM Treelist WHERE email = '%s'" % email
        self.cursor.execute(sql_string);

        families = []
        for (treeName) in self.cursor:
            families.append(treeName)

        return families


    ##### Family table methods

    # Drop a family table
    def drop_family(self, family_name, family_id):
        table_name = str(family_name) + str(family_id)
        self.drop(table_name)

    # Select all from family
    def select_family(self, familyName):
        self.cursor.execute("SELECT * FROM %s" % familyName)
        for (personID, motherID, fatherID, name, gender) in self.cursor:
            print "%s, %s, %s, %s, %s" % (personID, motherID, fatherID, name, gender)

    # Create a family table
    def create_family(self, family_name, family_id):
        table_name = str(family_name) + str(family_id)
        sql_string = (
            "CREATE TABLE %s("
            "personID INT NOT NULL AUTO_INCREMENT,"
            "motherID INT,"
            "fatherID INT,"
            "name VARCHAR(50) NOT NULL,"
            "gender CHAR(1) NOT NULL,"
            "PRIMARY KEY(personID)"
            ") ENGINE=InnoDB"
        ) % table_name.lower()
        self.exec_change(sql_string)

    # Insert into
    #def insert_node(self, family_name, pid, mid, fid, )
    #    sql_string = "INSERT INTO "
