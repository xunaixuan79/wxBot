#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import re
import MySQLdb


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        print 'INFO receive message ', msg['content']
        if msg['content']['type'] == 0:
            # 如果收到文字消息
            process_fraud_msg(msg['content']['data'])


def process_fraud_msg(msg):
    m = re.search('(\d{17})([0-9]|X)', msg.upper())
    if m is not None:
        id = m.group(0)
        print 'INFO got a relative message: ', id
        save_msg(id, msg.encode('utf-8'))
    pass


db = MySQLdb.connect("localhost", "test", "test", "wx")
insert_applicant = "insert into applicant(`idcard_number`,`desc`) values (%s, %s)"


def save_msg(id, msg):
    cursor = db.cursor()
    try:
        cursor.execute(insert_applicant, (id, msg))
        db.commit()
    except Exception as e:
        db.rollback()
        print str(e)


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    # cnx = MySQLdb.connect("localhost", "test", "test", "wx")
    # save_msg("331022244", 'sdfsdfsdfsdf')
    main()
