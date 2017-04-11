from treehouse import *

treedb = TreeSQL()
treedb.connect()

Tables = {}

Tables['Account'] = (
    "CREATE TABLE Account("
    " email VARCHAR(50) NOT NULL,"
    " username VARCHAR(50),"
    " password VARCHAR(50) NOT NULL,"
    "  PRIMARY KEY (email)"
    ") ENGINE=InnoDB"
)

Tables['Treelist'] = (
    "CREATE TABLE Treelist("
    "treeID INT NOT NULL AUTO_INCREMENT"
    "email VARCHAR(100) NOT NULL,"
    "treeName VARCHAR(100) NOT NULL,"
    "URL VARCHAR(100),"
    "PRIMARY KEY(email, treeName),"
    "FOREIGN KEY(email) REFERENCES Account(email)"
    ") ENGINE=InnoDB"
)

for key, value in Tables.iteritems():
    try:
        print "Creating table %s: " % key
        treedb.exec_change(value)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print "It already exists."
        else:
            print(err.msg)
    else:
        print "Success!"
