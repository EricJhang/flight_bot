
from models.User import LineUser
import pymongo

uri = 'mongodb://heroku_g4mqlp4n:b2fuh42r8dvlnaofkcrv97sv93@ds225010.mlab.com:25010/heroku_g4mqlp4n'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
PROVIDER = 'LINE'
VENDOR = ['雄獅', '可樂', '山富']
def is_first_Login(event):
    # 先把method開出來，到時候去搜尋FlightGo會員資料庫，確認會員是不是第一次使用
    isfirst = True
    return isfirst
def save_memberInfo_data(user_id, phoneNumber, email, gender,profile):
    # 將會員資料傳到後端，讓後端進行儲存
    name = profile.display_name
    picture = profile.picture_url
    user = LineUser(user_id, name, email, gender, phoneNumber, picture)

    # collection; it is created automatically when we insert.

    # Note that the insert method can take either an array or a single dict.
    #json_str = json.dumps(user.__dict__, ensure_ascii=False).encode('utf8')
    #data = {'user': user.__dict__}
    session_collection = db['members']
    inserted_id = session_collection.insert_one(user.__dict__).inserted_id
    if inserted_id:
        return True
    else:
        return False
def save_favorite_questionnaire(user_key,favorite_list):
    # 將每位user 做的喜好旅遊類型問卷答案往後端儲存
    print(favorite_list[0])

def save_message(event, message):
    print('#save_message')
    print (message)
    
    data = {
        'user_id': event.source.user_id,
        'ask': {
            'replyToken': event.reply_token,
            'type': event.type,
            'timestamp': event.timestamp,
            'source_type': event.source.type,
            'source_user_id': event.source.user_id,
            'message_id': event.message.id,
            'mesage_type': event.message.type,
            'message_text': event.message.text,
            'vendor': VENDOR[2]  # e.g 山富
        },
        'reply': {
            'from': 'flightgo', # it may from flightgo OR vendor name
            'type': message[0].type,
            'text': message[0].text
        }
    },
    # collection; it is created automatically when we insert.
    session_collection = db['sessions']
    # Note that the insert method can take either an array or a single dict.
    session_collection.insert_many(data)