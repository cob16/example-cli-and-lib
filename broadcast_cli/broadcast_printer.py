from clint.textui import colored, indent, puts
from datetime import datetime


def broadcast_printer(b):
    puts(user_id(b))
    puts(created_at(b))
    puts(feed(b))

    puts(colored.yellow('Content: ▼'))
    with indent(4):
        puts(b['content'])
    puts()


def user_id(broadcast):
    return colored.blue('User: {}').format(broadcast['user_id'])


def feed(broadcast):
    return colored.magenta("Feeds: {0}").format(' - '.join(broadcast['feeds']))


def created_at(b):
    return colored.cyan(
        datetime.strptime(b['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("Date: %y/%m/%d %H:%M UTC")
    )
