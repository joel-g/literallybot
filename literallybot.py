from urllib.parse import urlparse
from bs4 import BeautifulSoup

import re
import requests
import bs4
import praw
import time


history = 'commented.txt'

reply = 'Did you really mean to say literally?\nConsider reading http://writingexplained.org/literally-vs-figuratively-difference to learn when to use the word "literally".'

def authenticate():

    print('Authenticating...\n')
    reddit = praw.Reddit('literallybot', user_agent = '/u/LiterallyLiteralBot')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def literallybot(reddit):

    print("Getting 100 comments...\n")

    for comment in reddit.subreddit('test').comments(limit = 100):
        match = re.findall("literally", comment.body)
        if match:
            print("'Literally' found in comment with comment ID: " + comment.id)

            file_obj_r = open(history,'r')
            if comment.id not in file_obj_r.read().splitlines():
                print('Literally a new post. Commenting on:')
                print(comment.body)
                comment.reply(reply)

                file_obj_r.close()

                file_obj_w = open(history,'a+')
                file_obj_w.write(comment.id + '\n')
                file_obj_w.close()
                time.sleep(600)
            else:
                print('Already commented on this!\n')

            time.sleep(10)

    print('Waiting 30 seconds...\n')
    time.sleep(30)


def main():
    reddit = authenticate()
    while True:
        literallybot(reddit)


if __name__ == '__main__':
    main()
