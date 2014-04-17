# create the database 'images.sqlite' and create a table 'image_store' inside
# of it.

import sqlite3

db = sqlite3.connect('images.sqlite')
create_str = 'CREATE TABLE image_store (' + \
             'i INTEGER PRIMARY KEY, ' + \
             'filename TEXT, ' + \
             'image BLOB' + \
             ')'
db.execute(create_str);
db.commit()
db.close()

# here, the database is images.sqlite; it contains one table, image_store;
# 'i' is a column that provides a unique key for retrieval (and is optimized
#   for that; 'image_store' is another column that contains large binary
#   objects (blobs).
