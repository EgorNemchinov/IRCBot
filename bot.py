import socket
import argparse

HOST = "chat.freenode.net"
PORT = 6667

class IRCBot:

    BYTES_TO_READ = 2048

    def __init__(self, channel='channel', nick='Mcconaughey'):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.connect((HOST, PORT))

        self.nickname = nick
        self.channel = '#' + channel.replace('#', '')
        self.running = False
        self.buffer = ''

        self.send_msg(f'USER {NICK} {NICK} {NICK}: {NICK}')
        self.send_msg(f'NICK {NICK}')
        self.priv_msg(NICK, 'nickserv')
        for line in self.read_lines():
            self.check_ping(line)
        self.send_msg(f'JOIN #{channel}')
        self.priv_msg('Alright, alright, alright')
        self.read_lines()
        self.run()
        pass

    def send_msg(self, msg):
        self.irc_socket.send(bytes('%s\r\n' % msg, 'UTF-8'))

    def priv_msg(self, msg, receiver='#channel'):
        return self.send_msg('PRIVMSG %s : %s' % (receiver, msg))

    def read_lines(self):
        buffer = self.irc_socket.recv(self.BYTES_TO_READ).decode('UTF-8')
        self.log(buffer)
        return str.split('\n')

    def check_ping(self, line):
        if 'PING' in line:
            self.send_msg('PONG %s' % line.split()[1])
            return True
        return False

    def run(self):
        print('Running in a loop')
        self.running = True
        try:
            while self.running:
                lines = self.read_lines()
                for line in lines:
                    self.check_ping(line)

                    words = str.rstrip(line).split()
        except:
            self.stop()

    def stop(self):
        self.running = False
        self.priv_msg('Was nice meeting ya. Bye, fellas!')
        self.send_msg('QUIT : Bye y\'all')

    def log(self, line):
        print(line)
    
