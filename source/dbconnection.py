import sqlite3
#Leftover code, could be used to remove code clutter but not used


def DB_Write(table_name, column_names, values):
    conn = sqlite3.connect("databases/testgpt.db")
    cursor = conn.cursor()
    sql_command = f"INSERT INTO {table_name} ({column_names}) VALUES ({values})"
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

def DB_Delete(sql_command):
      conn = sqlite3.connect("databases/testgpt.db")
      cursor = conn.cursor()
      cursor.execute(sql_command)
      conn.commit()
      conn.close()
