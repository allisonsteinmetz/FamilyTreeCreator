from treehouse import *

a = TreeSQL()

# IMPORTANT - must always call this function before you can interact with the database
a.connect()

# Create a new account
a.insert_account("admin", "admin")

# Insert a Treelist entry
# This also creates a Family table
a.insert_treehouse("admin", "admin_family")

# View all families associated with an account email
a.select_families_for_account("admin")

# Call at the end of use
a.disconnect()



