import argparse
import urllib3
from bot import IRCBot

NAME = 'JonathanSunny'
INIT_MESSAGE = 'Hello! If you would like to find out weather in certain town, write "weather <city>"'
QUIT_MESSAGE = 'Thank you for using our service.'

class WeatherBot(IRCBot):
    def __init__(self, channel):
        super().__init__(channel, NAME, init_message=INIT_MESSAGE, quit_message=QUIT_MESSAGE)

    def _process_line(self, line):
        words = str.rstrip(line).split()

        if ' PRIVMSG ' in line:
            index = words.index('PRIVMSG')
            sender = words[0][1:words[0].find('!')]
            receiver = words[index + 1]
            rest = ' '.join(words[index + 2 :])
            if 'weather' in line:
                print(words[index + 2])
                city = '-'.join(words[index + 3:])
                self.log(f'Trying to fetch weather for {city}')
                weather_forecast = self._fetch_weather(city)
                if weather_forecast == None:
                    self.priv_msg('Haven\'t found weather for city', city)
                else:
                    self.priv_msg(f'Weather for 0-3 days in town {city} is:')
                    self.priv_msg(weather_forecast)

    def _fetch_weather(self, city):
        BEGIN_STR = '<p class="b-forecast__table-description-content"><span class="phrase">'
        END_STR = '</span></p>'
        url = f'https://www.weather-forecast.com/locations/{city}/forecasts/latest'
        http = urllib3.PoolManager()
        req = http.request('GET', url)
        if req.status != 200:
            return None
        data = str(req.data)
        begin_ind = data.find(BEGIN_STR) + len(BEGIN_STR)
        if begin_ind == -1:
            self.log('Couldnt find begin string in fetched data from url')
            return None
        end_ind = data[begin_ind:].find(END_STR)
        if end_ind == -1:
            self.log('Couldnt find end string in fetched data from url')
            return None
        return data[begin_ind:begin_ind + end_ind].replace('&deg;C', '°')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg('channel', type=str)
    args = parser.parse_args()

    bot = WeatherBot(args.channel)
    bot.run()
