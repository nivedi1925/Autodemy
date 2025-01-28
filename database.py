import sqlite3
import json


def create_database_and_tables(channel_chat_ids):
    """This to be executed for the first time only then should be commented
    Creates database in the project folder"""
    conn = sqlite3.connect("Courses.db")
    conn.execute("CREATE TABLE course_list(title text PRIMARYKEY NOT NULL);")
    conn.execute("CREATE TABLE message_ids(chat_id INT PRIMARYKEY NOT NULL,last_message_id INT);")
    query = "INSERT INTO message_ids(chat_id,last_message_id) VALUES({0},{1});"
    for id in channel_chat_ids:
        conn.execute(query.format(id,0))
    conn.commit()
    conn.close()
    # dictionary to be dumped
    d = {
        'last_deleted_message_id':0
    }

    with open('last_deleted.json', 'w', encoding='utf8') as json_file:
        json.dump(d,json_file)



def check_new_course(title,conn):
    """Return true if it is new course else false
    Make an entry in the database if its new course before returning true"""
    # conn = sqlite3.connect(("Courses.db"))
    select_query = "SELECT COUNT(title) FROM course_list WHERE title='{0}';"
    cursor = conn.execute(select_query.format(title))
    for row in cursor:
        count = row[0]

    if count > 0:
        return False
    else:
        insert_query = "INSERT INTO course_list(title) VALUES('{0}');"
        conn.execute(insert_query.format(title))
        conn.commit()
        return True


def delete_entry(title,conn):
    """Delete an entry from dat database which is equal to given title"""
    print("deleted -- ", title)
    delete_query = "DELETE FROM course_list WHERE title LIKE '%{0}%';".format(title)
    print(delete_query)
    conn.execute(delete_query)
    conn.commit()
    print("deleted -- ",title)


def last_time_checked_message_ids():
    message_ids = {}
    conn = sqlite3.connect("Courses.db")
    select_message_id = "SELECT * FROM message_ids;"
    cursor = conn.execute(select_message_id)
    for row in cursor:
        message_ids[row[0]] = row[1]
    return message_ids
    conn.close()

def update_last_check_message_ids(message_id_dict,conn):
    query = "UPDATE message_ids SET last_message_id={0} WHERE chat_id={1}"
    for chat_id in message_id_dict:
        conn.execute(query.format(message_id_dict[chat_id],chat_id))


