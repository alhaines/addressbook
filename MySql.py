# ~/py/MySql.py
#
# Copyright 2010 AL Haines (from original MyFunctions.php)
#
# v3.0: The definitive, stable version. Adds the 'charset' parameter to the
#       connection to ensure all data is correctly handled as UTF-8,
#       providing backward compatibility for older latin1 tables.

import pymysql
import pymysql.cursors
import sys

# --- This config loading is correct and does not need to change ---
try:
    import config
    DB_HOST = config.mysql_config.get('host')
    DB_USER = config.mysql_config.get('user')
    DB_PASSWORD = config.mysql_config.get('password')
    DB_NAME = config.mysql_config.get('database')
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Database credentials missing in config.py.")
except Exception as e:
    print(f"Error loading config: {e}", file=sys.stderr)
    sys.exit(1)


class MySQL:
    def __init__(self, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def _connect(self):
        if self.connection and self.connection.open:
            return self.connection
        try:
            # --- THE ONLY CHANGE IS HERE ---
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
                charset='utf8mb4' # This forces all results into clean UTF-8 strings
            )
            return self.connection
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}", file=sys.stderr)
            sys.exit(1)

    def _close(self):
        if self.connection and self.connection.open:
            self.connection.close()
            self.connection = None

    def get_data(self, query_string, params=None):
        data = []
        conn = None
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(query_string, params)
                data = cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error executing query: {e}", file=sys.stderr)
            return None
        finally:
            if conn:
                self._close()
        return data

    def put_data(self, query_string, params=None):
        success = False
        conn = None
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(query_string, params)
            conn.commit()
            success = True
        except pymysql.Error as e:
            print(f"Error executing update: {e}", file=sys.stderr)
            if conn:
                conn.rollback()
        finally:
            if conn:
                self._close()
        return success
    
    def get_field_names(self, table):
        field_names = []
        conn = None
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION")
                for row in cursor.fetchall():
                    field_names.append(row['COLUMN_NAME'])
        except pymysql.Error as e:
            print(f"Error getting field names for table '{table}': {e}", file=sys.stderr)
        finally:
            if conn:
                self._close()
        return field_names

    def get_num_fields(self, table):
        num_fields = -1
        conn = None
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                num_fields = cursor.rowcount
        except pymysql.Error as e:
            print(f"Error getting number of fields for table '{table}': {e}", file=sys.stderr)
        finally:
            if conn:
                self._close()
        return num_fields
