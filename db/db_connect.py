import psycopg2
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cred  import db_user, db_host, db_port,db_database

class Database:
    """PostgreSQL Database class."""

    def __init__(
            self,
            DATABASE_HOST = db_host,
            DATABASE_USERNAME = db_user,
            DATABASE_PASSWORD = None,
            DATABASE_PORT = db_port,
            DATABASE_NAME = db_database
        ):
        self.host = DATABASE_HOST
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.port = DATABASE_PORT
        self.dbname = DATABASE_NAME
        self.conn = None
        # self.cur = None

    def connect(self):
      if self.conn is None:
        try:
          self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )

          cursor = self.conn.cursor()
          # Print PostgreSQL Connection properties
          print ( self.conn.get_dsn_parameters(),"\n")

          # Print PostgreSQL version
          cursor.execute("SELECT version();")
          record = cursor.fetchone()
          print("You are connected to - ", record,"\n")
          
          create_table_query = '''CREATE TABLE IF NOT EXISTS mobile
                (ID INT PRIMARY KEY     NOT NULL,
                MODEL           TEXT    NOT NULL,
                PRICE         REAL); '''
          
          cursor.execute(create_table_query)
          self.conn.commit()
          print("Table created successfully")

        except (Exception, psycopg2.Error) as error:
          print ("Error while connecting to PostgreSQL", error)
        finally:
          #closing database connection.
          if(self.conn):
              cursor.close()
              self.conn.close()
              print("PostgreSQL connection is closed")

    def select_rows(self):
      self.open_connection()
      with self.conn.cursor() as cur:
        cur.execute(query)
        records = [row for row in cur.fetchall()]
        cur.close()
        return records
      

if __name__ == '__main__': 
  db = Database()
  db.connect()