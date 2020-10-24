import argparse
import sqlite3
import os


def main(args):
    sqliteConnection = sqlite3.connect(args.database)
    cursor = sqliteConnection.cursor()
    process_dir(args.path, cursor)
    sqliteConnection.commit()


def process_dir(dir, cursor):
    for _, subdirs, files in os.walk(dir):
        for d in subdirs:
            aux = os.path.abspath(os.path.join(dir, d))
            process_dir(aux, cursor)
        for f in files:
            aux = os.path.abspath(os.path.join(dir, f))
            process_file(aux, f, cursor)


def process_file(full_path, fname, cursor):
    sqlite_select_query = """SELECT * from image where path = %s"""
    cursor.execute(sqlite_select_query, full_path)
    records = cursor.fetchall()
    if not records:
        sqlite_insert_query = """INSERT INTO image (name, path, tags) VALUES (?,?,?)"""
        cursor.execute(sqlite_insert_query, (fname, full_path, ''))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="www")
    parser.add_argument("-db", "--database", default='sqlite:///ImageServer.db')

    main(parser.parse_args())
