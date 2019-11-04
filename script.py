#!/usr/bin/python

import json
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from sqlalchemy import create_engine
from config import DATABASE_URI, community_token, user_token
from models import Base, Posting
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import requests
import os


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

# url = 'https://pm1.narvii.com/6319/3d43ac7556aad6cf30e350ce100c10ce083fb7a8_hq.jpg'
# file_path = os.path.basename(url)
# f = open(file_path, 'wb')
# f.write(requests.get(url).content)
# f.close()
# os.remove(file_path)

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



# short_hair_tyan -117327305
# pixiv -41194531
# another_pixiv-32129915
# feeling_of_wonderful -88199789
# 2pic -82854181
# wise forest -84391992
# arts -30446096

monday = Posting(
    offset_counter=102,
    group=-117327305,
    day=0
)

tuesday = Posting(
    offset_counter=102,
    group=-41194531,
    day=1
)
wednesday = Posting(
    offset_counter=102,
    group=-32129915,
    day=2
)

thursday = Posting(
    offset_counter=102,
    group=-88199789,
    day=3
)

friday = Posting(
    offset_counter=102,
    group=-82854181,
    day=4
)

saturday = Posting(
    offset_counter=102,
    group=-84391992,
    day=5
)

sunday = Posting(
    offset_counter=102,
    group=-30446096,
    day=6
)


days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]



sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
def timed_job():
    params = (
        ('group_id', '152741251'),
        ('album_id', '268336398'),
        ('access_token', user_token),
        ('v', 5.103),
    )

    response = requests.get('https://api.vk.com/method/photos.getUploadServer', params=params)
    print(response)
    upload_server = json.loads(response.text)['response']['upload_url']
    with session_scope() as s:
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        if not s.query(Posting).first():
            for day in days:
                s.add(day)
        posting = s.query(Posting).filter(Posting.day == datetime.today().weekday()).first()
        # import calendar
        # print(calendar.day_name[posting.day])
        params = (
            ('owner_id', posting.group),
            ('album_id', '-7'),
            ('access_token', user_token),
            ('offset',posting.offset_counter),
            ('count',1),
            ('v', 5.103),
        )
        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        posting.offset_counter = posting.offset_counter + 1 #always increase the counter
        s.add(posting)
        sizes = response.json()['response']['items'][0]['sizes']
        url = sizes[len(sizes)-1]['url']
        # url = 'https://pm1.narvii.com/6319/3d43ac7556aad6cf30e350ce100c10ce083fb7a8_hq.jpg'
        file_path = os.path.basename(url)
        f = open(file_path, 'wb')
        f.write(requests.get(url).content)
        f.close()
    files = {'file1': open(file_path, 'rb')}
    response = requests.post(upload_server, files=files)
    os.remove(file_path)
    img_hash = json.loads(response.text)['hash']
    photos_list = json.loads(response.text)['photos_list']
    server = json.loads(response.text)['server']

    params = (
        ('group_id', '152741251'),
        ('album_id', '268336398'),
        ('hash', img_hash),
        ('photos_list', photos_list),
        ('server', server),
        ('access_token', user_token),
        ('v', 5.103),
    )

    response = requests.get('https://api.vk.com/method/photos.save', params=params)
    response_json = response.json()
    owner_id = response_json['response'][0]['owner_id']
    photo_id = response_json['response'][0]['id']
    photo_full_id = f'photo{owner_id}_{photo_id}'
    print(photo_full_id)

    params = (
        ('owner_id', '-152741251'),
        ('from_group', '1'),
        # ('message', 'another_one_bites_the_dust'),
        ('attachments', photo_full_id),
        ('access_token', user_token),
        ('v', 5.103),
    )

    response = requests.get('https://api.vk.com/method/wall.post', params=params)

    print(response.text)


@sched.scheduled_job('cron', day_of_week='wed', hour=13)
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
