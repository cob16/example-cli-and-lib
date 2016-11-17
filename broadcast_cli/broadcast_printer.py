from clint.textui import colored, indent, puts, columns
from datetime import datetime


def broadcast_printer(b):
    puts(columns([user_id(b), 10], [created_at(b), 25], [feed(b), None]))
    puts(colored.yellow('Content: ▼'))
    # with indent(10):
    puts(b['content'])
    puts()



def user_id(broadcast):
    return colored.blue('User: {}').format(broadcast['user_id'])


def feed(broadcast):
    feeds = sorted(broadcast['feed_list'], key=str.lower) #case insensitive sort
    return colored.magenta("Feeds: {0}").format(' - '.join(feeds))


def created_at(b):
    return colored.cyan(
        datetime.strptime(b['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("Date: %y/%m/%d %H:%M UTC")
    )
