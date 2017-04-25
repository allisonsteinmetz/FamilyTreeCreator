import mysql.connector
from mysql.connector import errorcode


class FamilyMember:
    def __init__(self):
        self.name = ""
        self.spouseName = "None"
        self.children = []
        self.motherName = "None"
        self.fatherName = "None"
        self.gender = ""

    def copy_family(self, obj):
        self.name = obj.name
        self.spouseName = obj.spouseName
        self.children = obj.children[:]
        self.motherName = obj.motherName
        self.fatherName = obj.fatherName
        self.gender = obj.gender


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
        self.disconnect()

    # Create a connection to the database
    # IMPORTANT: must be called before any other method here
    def connect(self):
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
        if (self.cnx != None):
            if (self.cursor != None):
                self.cursor.close()
                self.cursor  = None
            self.cnx.close()
            self.cnx = None

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
    def select_account(self, enteredEmail, enteredPassword):
        self.cursor.execute("SELECT * FROM Account")
        for (email, username, password) in self.cursor:
            if(enteredEmail == email and enteredPassword == password):
                return username
        return False

    # Select a username from an email
    def select_username(self, email):
        sql_string = "SELECT userName FROM Account WHERE email = '%s'" % email
        self.cursor.execute(sql_string)
        for user in self.cursor:
            return user[0]
        return False


    ##### Treelist table methods

    # Insert an entry in Treelist
    def insert_treehouse(self, email, treeName):
        if (self.test_family(treeName) == False):
            return
        try:
            sql_string = "INSERT INTO Treelist (email, treeName) VALUES ('%s', '%s')" % (email, treeName)
            self.exec_change(sql_string)
            self.create_family(self.get_family_name(email, treeName))

        except mysql.connector.Error as err:
            print err


    # Remove an entry from Treelist
    def delete_treehouse(self, email, treeName):
        sql_string = "DELETE FROM Treelist WHERE email = '%s' AND treeName = '%s'" % (email, treeName)
        self.drop(self.get_family_name(email, treeName))
        self.exec_change(sql_string)


    def get_family_name(self, email, treeName):
        if (self.select_username != False):
            return self.select_username(email) + "_" +  treeName
        else:
            return ""


    # Select family table names
    def select_families_for_account(self, email):
        sql_string = "SELECT treeName FROM Treelist WHERE email = '%s'" % email
        self.cursor.execute(sql_string)

        families = []
        for (treeName) in self.cursor:
            treeName = treeName[0]
            families.append(treeName)
        return families


    ##### Family table methods

    # Create a family table
    # DO NOT USE outside of insert_treehouse()
    def create_family(self, family_name):
        sql_string = (
            "CREATE TABLE %s("
            "name VARCHAR(50) NOT NULL,"
            "spouseName VARCHAR(50),"
            "motherName VARCHAR(50),"
            "fatherName VARCHAR(50),"
            "gender CHAR(1) NOT NULL,"
            "PRIMARY KEY(name),"
            "FOREIGN KEY(spouseName) REFERENCES %s(name),"
            "FOREIGN KEY(motherName) REFERENCES %s(name)"
            ") ENGINE=InnoDB"
        ) % (family_name, family_name, family_name)
        try:
            self.exec_change(sql_string)
        except mysql.connector.Error as err:
            print err
            return False
        return True


    # Drop a family table
    # DO NOT USE outside of delete_treehouse()
    def drop_family(self, family_name):
        sql_string = "UPDATE %s SET spouseName = NULL, motherName = NULL, fatherName = NULL"
        self.exec_change(sql_string)
        self.drop(family_name)


    # See if syntax is correct for family
    def test_family(self, family_name):
        if (self.create_family(family_name) == True):
            self.drop_family(family_name)
            return True
        return False


    # Select all from family
    def select_family(self, familyName):
        sql_string = "SELECT name, spouseName, motherName, fatherName, gender FROM %s" % familyName
        self.cursor.execute(sql_string)

        members = []
        for name, spouseName, motherName, fatherName, gender in self.cursor:
            row = FamilyMember()
            row.name = name

            if (spouseName is None):
                row.spouseName = u"None"
            else:
                row.spouseName = spouseName

            if (motherName is None):
                row.motherName = u"None"
            else:
                row.motherName = motherName

            if (fatherName is None):
                row.fatherName = u"None"
            else:
                row.fatherName = fatherName

            row.gender = gender
            members.append(row)

        for member in members:
            member.children = self.get_children(familyName, member)

        return members


    # Get the gender of a person
    def get_gender(self, familyName, personName):
        sql_string = "SELECT gender FROM %s WHERE name = '%s'" % (familyName, personName)
        self.exec_change(sql_string)
        for gender in self.cursor:
            return gender[0]


    # Find the children of a family_name
    def get_children(self, familyName, parentName):
        sql_string = "SELECT name FROM %s WHERE (fatherName = '%s' OR motherName = '%s')" % (familyName, parentName, parentName)
        self.cursor.execute(sql_string)
        children = []
        for child in self.cursor:
            children.append(child)
        return children


    # Insert a new person into the family
    def insert_person(self, family_name, name, gender):
        sql_string = "INSERT INTO %s(name, gender) VALUES ('%s', '%s')" % (family_name, name, gender)
        self.exec_change(sql_string)


    # Delete a person from the family
    def delete_person(self, family_name, name):
        family = self.select_family(family_name)

        # Only allow deletion of leaf nodes
        for member in family:
            connections = 0
            if member.name == name:
                if (len(member.children) != 0):
                    return False

                if (member.motherName != "None" or member.fatherName != "None"):
                    connections += 1
                if (member.spouseName != "None"):
                    connections += 1

            if (connections > 1):
                return False

        sql_string = "UPDATE %s SET spouseName = NULL WHERE spouseName = '%s' " % (family_name, name)
        self.exec_change(sql_string)
        sql_string = "UPDATE %s SET spouseName = NULL WHERE name = '%s' " % (family_name, name)
        self.exec_change(sql_string)
        sql_string = "DELETE FROM %s WHERE name = '%s'" % (family_name, name)
        self.exec_change(sql_string)


    # Update the spouse for a person in a family
    def update_spouse(self, family_name, name, spouse_name):
        sql_string = "UPDATE %s SET spouseName = '%s' WHERE name = '%s'" % (family_name, spouse_name, name)
        self.exec_change(sql_string)
        sql_string = "UPDATE %s SET spouseName = '%s' WHERE name = '%s'" % (family_name, name, spouse_name)
        self.exec_change(sql_string)


    # Update the mother for a person in a family
    def update_mother(self, family_name, name, mother_name):
        sql_string = "UPDATE %s SET motherName = '%s' WHERE name = '%s'" % (family_name, mother_name, name)
        self.exec_change(sql_string)


    # Update the father for a person in the family
    def update_father(self, family_name, name, father_name):
        sql_string = "UPDATE %s SET fatherName = '%s' WHERE name = '%s'" % (family_name, father_name, name)
        self.exec_change(sql_string)





# JSON generating class
class TreeJSON:
    def __init__(self, familyName):
        self.familyTreeString = ""
        self.found_root = False
        self.globalRootNode = FamilyMember()
        self.db = TreeSQL()
        self.db.connect()
        self.entries = self.db.select_family(familyName)
        self.db.disconnect()

    # Find and construct a family member object
    def find_family_member(self, name):
        member = FamilyMember()
        for row in self.entries:
            if row.name == name:
                member = row
                return member
        return False

    # Find the root of the tree
    # DO NOT CALL unless necessary
    def find_root(self):
        # No root if there is no tree
        if (len(self.entries) == 0):
            return False
        # Single entry is root by definition
        elif (len(self.entries) == 1):
            self.globalRootNode = self.entries[0]
            self.found_root = True
        # If a parent was added, they are the new root node
        # Otherwise, do nothing
        elif (len(self.entries) == 2):
            mother = find_family_member(self.globalRootNode.motherName)
            father = find_family_member(self.globalRootNode.fatherName)
            if (mother != "None"):
                self.globalRootNode = mother
            elif (father != "None"):
                self.globalRootNode = father
        # Just find the first topmost node in all other cases
        else:
            for row in self.entries:
                if row.spouseName == "None" and row.motherName == "None" and row.fatherName == "None":
                    self.globalRootNode = row
                    self.found_root = True
                elif row.spouseName != "None":
                    spouse = self.find_family_member(row.spouseName)
                    if (spouse.fatherName == "None" and spouse.motherName == "None"):
                        self.globalRootNode = row
                        self.found_root = True


    # Build the tree string recursively
    def constructTree(self, node, spouse_added):
        unclosedMarriage = False

        if (node == self.globalRootNode):
            self.familyTreeString += "[{'name': '" + node.name + "', 'class':"
            if (self.globalRootNode.gender == 'M'):
                self.familyTreeString += "'man',"
            else:
                self.familyTreeString += "'woman',"
            self.familyTreeString += "'textClass':'rootText'"

        if (node.spouseName != "None"):
            if spouse_added == False:
                if node.gender == 'M':
                    self.familyTreeString += ", 'marriages': [{'spouse': { 'name': '" + node.spouseName + "','class': 'woman'}"
                    unclosedMarriage = True
                elif node.gender == 'F':
                    self.familyTreeString += ", 'marriages': [{'spouse': { 'name': '" + node.spouseName + "','class': 'man'}"
                    unclosedMarriage = True
            if node.gender == self.globalRootNode.gender:
                self.constructTree(self.find_family_member(node.spouseName), True)

        if (len(node.children) != 0 and node.gender == self.globalRootNode.gender):
            self.familyTreeString += ", 'children': ["
            for child in node.children:
                childObj = self.find_family_member(child[0])

                if childObj.gender == 'M':
                    self.familyTreeString += "{ 'name': '" + childObj.name + "', 'class': 'man'"
                else:
                    self.familyTreeString += "{ 'name': '" + childObj.name + "', 'class': 'woman'"

                self.constructTree(childObj, False)
                self.familyTreeString += "}, "

            self.familyTreeString += "]"

        if (unclosedMarriage):
            self.familyTreeString += "}]"

        finalString = ""
        if (node == self.globalRootNode):
            self.familyTreeString += "}]"
            finalString = self.familyTreeString
            self.familyTreeString = ""
            self.globalRootNode = FamilyMember()

        return finalString

    # Return a JSON string from the treehouse
    # CALL THIS ONE
    def get_JSON(self):
        self.find_root()
        if self.found_root:
            return self.constructTree(self.globalRootNode, False)
        else:
            return "[]"
