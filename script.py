#!/usr/bin/python

import json
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from sqlalchemy import create_engine
from config import DATABASE_URI, community_token, user_token
from models import Base, Counter
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

sched = BlockingScheduler()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# @sched.scheduled_job('cron', hour='10-22/2,0')
# def timed_job():
#     params = (
#         ('group_id', '152741251'),
#         ('album_id', '268336398'),
#         ('access_token', user_token),
#         ('v', 5.103),
#     )


#     response = requests.get('https://api.vk.com/method/photos.getUploadServer', params=params)
#     print(response.text)
#     upload_server = json.loads(response.text)['response']['upload_url']

#     with session_scope() as s:
#             # Base.metadata.drop_all(engine)
#             Base.metadata.create_all(engine)
#             if not s.query(Counter).first():
#                 counter = Counter()
#                 s.add(counter)
#             counter = s.query(Counter).first()
#             index = counter.index
#             page_index = (index + 1) // 24 + 1
#             image_index = index % 24
#             try:
#                 response = requests.get(f'https://wallhaven.cc/api/v1/search?categories=110&purity=100&sorting=favorites&order=desc&page={page_index}')
#             except Exception as e:
#                 print(e.message)
#                 raise e
#             image_url = json.loads(response.text)['data'][image_index]['path']
#             file_path = os.path.basename(image_url)
#             f = open(file_path, 'wb')
#             f.write(requests.get(image_url).content)
#             f.close()

#             try:
#                 files = {'file1': open(file_path, 'rb')}
#                 response = requests.post(upload_server, files=files)
#             except Exception as e:
#                 print(e.message)
#                 raise e
#             counter.index = counter.index + 1
#             os.remove(file_path)
#             img_hash = json.loads(response.text)['hash']
#             photos_list = json.loads(response.text)['photos_list']
#             server = json.loads(response.text)['server']

#             try:
#                 params = (
#                     ('group_id', '152741251'),
#                     ('album_id', '268336398'),
#                     ('hash', img_hash),
#                     ('photos_list', photos_list),
#                     ('server', server),
#                     ('access_token', user_token),
#                     ('v', 5.103),
#                 )

#                 response = requests.get('https://api.vk.com/method/photos.save', params=params)
#             except Exception as e:
#                 print(e.message)
#                 raise e
#             owner_id = json.loads(response.text)['response'][0]['owner_id']
#             photo_id = json.loads(response.text)['response'][0]['id']
#             photo_full_id = f'photo{owner_id}_{photo_id}'

#             try:
#                 params = (
#                     ('owner_id', '-152741251'),
#                     ('from_group', '1'),
#                     # ('message', 'another_one_bites_the_dust'),
#                     ('attachments', photo_full_id),
#                     ('access_token', user_token),
#                     ('v', 5.103),
#                 )

#                 response = requests.get('https://api.vk.com/method/wall.post', params=params)
#             except Exception as e:
#                 print(e.message)
#                 raise e





@sched.scheduled_job('cron', day_of_week='fri', hour=13, minute=23)
def scheduled_job():
    params = (
        ('owner_id', '-152741251'),
        ('from_group', '1'),
        ('attachments', 'photo-176795646_457239122'),
        ('access_token', user_token),
        ('v', 5.103),
    )

    response = requests.get('https://api.vk.com/method/wall.post', params=params)

    print(response.text)


@sched.scheduled_job('cron', day_of_week='wed', hour=13, minute=42)
def scheduled_job():
    params = (
        ('owner_id', '-152741251'),
        ('from_group', '1'),
        ('attachments', 'photo343976380_456242282'),
        ('access_token', user_token),
        ('v', 5.103),
    )

    response = requests.get('https://api.vk.com/method/wall.post', params=params)

    print(response.text)


sched.start()
