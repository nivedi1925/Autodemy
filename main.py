from pyexpat.errors import messages
import database
from config import api_id, api_hash, fresh_course_chat_id,delete_channel_chat_id
from telethon import TelegramClient
import sqlite3
import json
import datetime





messages_for_db_scan = {}
error_messages = []
channel_chat_ids = [-1001101378903, -1001279165634, -1001494678304,
                    -1001261561054, -1001502099529, -1001351249451,
                    -1001434355232, -1001929303378,]




#TODO: Write function to forwad message
def forward_message(message,chat_id):
    with TelegramClient('mySession', api_id, api_hash) as client:
        client.loop.run_until_complete(client.forward_messages(fresh_course_chat_id, message.id, chat_id))
        # client.loop.run_until_complete(client.send_message(fresh_course_chat_id,"\n-------This is footer-------\n"))



#TODO: Write a function to get message from each channel
def get_messages(chat_id):
    client = TelegramClient('mySession', api_id, api_hash)
    async def main():
        async for message in client.iter_messages(chat_id, limit=5):
            #check already checked message or not
            course_title = get_title(chat_id,message)
            messages_for_db_scan[course_title] = [message,chat_id]
            #await client.forward_messages(fresh_course_chat_id,message,UDEMYFREE_chat_id)

    with client:
        client.loop.run_until_complete(main())

#TODO: Write function to get the title from message
def get_title(chat_id,message):
    message.text = message.text.replace("#New\n", "")
    message.text = message.text.replace("#Bestseller\n", "")
    message.text = message.text.replace("#Highest_Rated\n", "")
    message.text = message.text.replace("[NEW]", "")
    message.text = message.text.replace("#Hot_&_New\n", "")
    # message.text = message.text.replace("#Highest_Rated\n", "")

    try:
        if chat_id == -1001101378903:
            if message.text.startswith("**"):
                return message.text.split('**')[1].strip().lower()
            else:
                return message.text.split("\n")[0].strip().lower()

        elif chat_id == -1001279165634:
            return message.text.split('**')[1].strip().lower()

        elif chat_id == -1001494678304:
            return message.text[30:].split('\n')[0].strip().lower()

        elif chat_id == -1001261561054:
            return message.text.split('/')[4].replace("-"," ").strip().lower()

        elif chat_id == -1001502099529:
            return message.text.split('**')[1].strip().lower()

        elif chat_id == -1001351249451:
            return message.text.split('**')[3].strip().lower()

        elif chat_id == -1001434355232:
            return message.text.split('**')[1].strip().lower()

        elif chat_id == -1001929303378:
            return message.text.split('**')[1].strip().lower()

    except Exception as e:
        error_messages.append([message,chat_id])



#TODO: Write function to iterate through dictionary object and check database and forward message
def check_and_forwad_messages():
    last_checked_message_ids = database.last_time_checked_message_ids()# to check
    checked_ids = last_checked_message_ids.copy() # message ids which are currenty being checked
    conn = sqlite3.connect("Courses.db")
    for title in messages_for_db_scan:
        message = messages_for_db_scan[title][0]
        chat_id = messages_for_db_scan[title][1]
        if message.id <= last_checked_message_ids[chat_id]:
            continue
        else:
            if message.id > checked_ids[chat_id]:
                checked_ids[chat_id] = message.id
            try:
                if database.check_new_course(title,conn):
                    forward_message(message,chat_id)

            except:
                error_messages.append([message, chat_id])
    database.update_last_check_message_ids(checked_ids,conn)
    conn.commit()
    conn.close()

def forward_erorr_messages():
    last_checked_message_ids = database.last_time_checked_message_ids()  # to check
    checked_ids = last_checked_message_ids.copy() # message ids which are currenty being checked
    conn = sqlite3.connect("Courses.db")
    for element in error_messages:
        message = element[0]
        chat_id = element[1]
        message_id = message.id
        if message.id <= last_checked_message_ids[chat_id]:
            continue
        else:
            print("error message id ",message_id,chat_id,checked_ids[chat_id])
            if message.id > checked_ids[chat_id]:
                checked_ids[chat_id] = message.id
            forward_message(message=message,chat_id=chat_id)
    database.update_last_check_message_ids(checked_ids, conn)
    conn.commit()
    conn.close()



def delete_message_title_from_channel():
    client = TelegramClient('mySession', api_id, api_hash)
    titles_to_be_deleted = []
    #read all 10 messages
    async def main():
        async for message in client.iter_messages(delete_channel_chat_id, limit=10):
            titles_to_be_deleted.append(message)
    with client:
        client.loop.run_until_complete(main())

    with open('last_deleted.json', 'r') as file:
        last_deleted_id = json.load(file)

    conn = sqlite3.connect("Courses.db")
    for message in titles_to_be_deleted:
        if message.id <= last_deleted_id['last_deleted_message_id']:
            continue
        else:
            last_deleted_id['last_deleted_message_id'] = message.id

            database.delete_entry(message.text.strip().lower(),conn)
    conn.commit()
    conn.close()
    with open('last_deleted.json', 'w', encoding='utf8') as json_file:
        json.dump(last_deleted_id,json_file)

def send_heart_beat():
    x = datetime.datetime.now().strftime('%H:%M')

    with TelegramClient('mySession', api_id, api_hash) as client:
        client.loop.run_until_complete(client.send_message(fresh_course_chat_id, '🐒🐒**Time:{0}**🐒🐒'.format(x)))


def main():
    send_heart_beat()
    delete_message_title_from_channel()
    for i in channel_chat_ids:
        get_messages(i)
    check_and_forwad_messages()
    forward_erorr_messages()


#database.create_database_and_tables(channel_chat_ids) # for first time only
main()

