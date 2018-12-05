import argparse

from bot import IRCBot

NAME = 'Mcconaughey'
INIT_MESSAGE = 'Alright, alright, alright, I''m here'
QUIT_MESSAGE = 'Bye, y\'all, was nice meeting ya'

class McconaugheyBot(IRCBot):
    def __init__(self, channel):
        super().__init__(channel, NAME, init_message=INIT_MESSAGE, quit_message=QUIT_MESSAGE)

    def _process_line(self, line):
        words = str.rstrip(line).split()

        if ' PRIVMSG ' in line:
            index = words.index('PRIVMSG')
            sender = words[0][1:words[0].find('!')]
            rest = ' '.join(words[index + 2 :])
            self.priv_msg(f'And I\'d say to {sender}: Alright, alright, alright')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg('channel', type=str)
    args = parser.parse_args()

    bot = McconaugheyBot(args.channel)
    bot.run()
