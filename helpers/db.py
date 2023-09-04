import sqlite3
from datetime import datetime
import os

class db:

    conn=None

    def __init__(self):
        
        #if DB doesn't exist
        if not os.path.isfile('posts.db'):
            print("DB doesn't exist, will create one now")
            self.create_db()
        else:
            self.conn = sqlite3.connect('posts.db')


    def create_db(self):
        self.conn = sqlite3.connect('posts.db')
        cursor = self.conn.cursor()

        cursor.execute('''CREATE TABLE posts
                (postid INT PRIMARY KEY     NOT NULL,
                savedon TEXT    NOT NULL);''')
        print("Table created successfully")

        self.conn.commit()
        
     
    def insertpost(self,postid):
        cursor = self.conn.cursor()
        now = datetime.now()
        cursor.execute("INSERT INTO posts (postid, savedon) VALUES (?, ?)", (postid, now))

        self.conn.commit()

    def postexists(self,postid):
       
        cursor = self.conn.cursor()
        cursor.execute("SELECT postid from posts WHERE postid = ?", (postid,))
        data = cursor.fetchall()

        if data:
            return True
        else:
            return False
    
    def close(self):
        self.conn.close()