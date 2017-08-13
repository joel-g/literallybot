import re
import praw
import time
from pygame import mixer

mixer.init()
alert=mixer.Sound('bell.wav')
BLACKLIST = {'literally'}
history = 'commented.txt'

reply = "Did you really 'literally'?\nConsider reading [this](http://writingexplained.org/literally-vs-figuratively-difference) to make sure you're using 'literally' correctly."

def authenticate():

    print('Authenticating...\n')
    reddit = praw.Reddit('literallybot', user_agent = '/u/LiteralLiterallyBot')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def literallybot(reddit):

    print("Getting 500 comments...\n")
    for comment in reddit.subreddit('all').comments(limit = 500):
        match = re.findall("literally", comment.body)
        if match:
            print("'Literally' found in comment with comment ID: " + comment.id)

            file_obj_r = open(history,'r')
            if comment.id not in file_obj_r.read().splitlines():
                if comment.author.name == reddit.user.me():
                    print('     Skipping my own comment...\n')
                else:
                    print('     Found new comment by ' + comment.author.name + '\n')
                    comment.reply(reply)
                    alert.play()

                    file_obj_r.close()
                    file_obj_w = open(history,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                    print('Waiting 10 minutes before commenting again')
                    time.sleep(600)
            else:
                print('     Already commented on this!\n')

            time.sleep(10)

    print('Waiting 30 seconds before pulling more comments...\n')
    time.sleep(30)


def main():
    reddit = authenticate()
    while True:
        literallybot(reddit)


if __name__ == '__main__':
    main()
