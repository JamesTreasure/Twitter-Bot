import tweepy
import lxml.html
import datetime
import time
import re



class TwitterAPI:
    def __init__(self):
        auth = self.twitter_auth()
        self.api = tweepy.API(auth)

    @staticmethod
    def twitter_auth():
        consumer_key = "4xWceLrAApS795zXBjf3e5Pw9"
        consumer_secret = "fkn7KDUpGRIWB4rCyWbgfo3u00KJ56n812szzqVCMaoV3W1Di1"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "995228744-2v2mgZ8bT0AHBLazUBXOpX934L8HYuRmvT6tEnvo"
        access_token_secret = "b9t2Lkpmlxl7bW1SDrt0YuGt9gnpGAlGXDi5IXHtbs5QF"
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def tweet(self, message):
        self.api.update_status(status=message)

    def ten_minute_takeover_time(self):
        now = datetime.datetime.now()
        #valid_time = now.weekday() < 5 and now.hour == 18 and 1 <= now.minute <= 20
        song_list = []
        while True:
            if 1:
                song_and_artist = self.get_latest_tweet('NowOnBBCRadio1')
            if song_and_artist and song_and_artist not in song_list:
                song_list.append(song_and_artist)
                self.tweet(str(song_and_artist[0]) + " - " + str(song_and_artist[1]))
                print("Tweeted!")
                print("Sleeping for a minute")
                time.sleep(5)
            else:
                time.sleep(30)
        else:
            print("Sleeping for a minute")
            time.sleep(60)

    def get_song_and_artist(self):
        html = lxml.html.parse("http://www.bbc.co.uk/radio1")
        song = html.xpath('//*[@id="live-0"]/div/div/div/h3')
        print(song[0].text)
        artist = html.xpath('//*[@id="live-0"]/div/div/div/h4')
        return song[0].text + " - " + artist[0].text

    def get_latest_tweet(self, screen_name):
        alltweets = []
        new_tweets = self.api.user_timeline(screen_name=screen_name, count=1)
        alltweets.extend(new_tweets)

        plain_text = (''.join(i for i in alltweets[0].text if ord(i)<128).lstrip())
        song = plain_text.split('by', 1)[0]
        artist = re.search('%s(.*)%s' % ("by", "http"), plain_text).group(1).lstrip()
        return (song, artist)


if __name__ == "__main__":
    twitter = TwitterAPI()
    twitter.ten_minute_takeover_time()