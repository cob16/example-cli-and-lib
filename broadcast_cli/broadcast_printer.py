from clint.textui import colored
from clint.textui import puts


def feed(broadcast):
    for feed in broadcast.feeds:
        puts(colored.red(feed))


def content(broadcast):
    puts(colored.yellow(broadcast.content))


def created_at(broadcast):
    puts(colored.red('TODO')) #todo
