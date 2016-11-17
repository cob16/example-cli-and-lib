from clint.textui import colored, indent, puts, columns
from datetime import datetime


def broadcast_printer(b):
    puts(columns([user_id(b), 7], [broadcast_id(b), 10], [created_at(b), 25], [feed(b), None]))
    puts(colored.yellow('Content: ▼'))
    # with indent(10):
    puts(b.content)
    puts()


def broadcast_id(broadcast):
    return colored.blue('User_ID: {}').format(broadcast.id)


def user_id(broadcast):
    id = broadcast.user_id
    if broadcast.user_id is None:
        id = 'N/A'
    return colored.cyan('ID: {}').format(id)


def feed(broadcast):
    feeds = sorted(broadcast.feeds, key=str.lower) #case insensitive sort
    return colored.magenta("Feeds: {0}").format(' - '.join(feeds))


def created_at(broadcast):
    return colored.cyan(
        datetime.strptime(broadcast.created_at, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("Date: %y/%m/%d %H:%M UTC")
    )
