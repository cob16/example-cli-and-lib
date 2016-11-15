# Broadcast cli
This is a educational test package that was used for learning purposes by the author
 
It is cli python application that allows human communication with the a rails API.
The idea being that a user can send a 'broadcast' (i.e a text message) that will 
be sent to a number of social medea, email, blogs ect at the same time by the server.

 
### To install
- `pip install .`
- `broadcast -h`

##Usage
```bash
usage: broadcast [-h] {list,send,show} ...

Sends and receives broadcasts (multi social network posts) from a server. Use
[subcommand] -h to get information of a command

optional arguments:
  -h, --help        show this help message and exit

Available subcommands:
  {list,send,show}
    list            Gets a list of all broadcasts made by the current user
    send            Sends a new broadcast
    show            Show all detail of a broadcast

```

### Running tests
- `pip install .[test]`
- `nosetests`

## With help from 
- https://github.com/kennethreitz/clint/tree/master/examples