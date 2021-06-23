import tweepy
import logging
import os
import datetime
from datetime import datetime

logger = logging.getLogger()

cuentas = ['222241634'] # Cuenta @112cmadrid

def create_api():
    auth = tweepy.OAuthHandler("", "")
    auth.set_access_token("",
                          "")
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")

        tuit_hour = int(tweet.created_at.strftime("%H")) + 2

        if (5 <= tuit_hour <= 9):
            if tweet.author.id != cuentas[0]:
                return
            else:
                print(tweet.text + " " + str(tweet.author.screen_name) + " Hora de publicación: " + str(
                    int(tweet.created_at.strftime("%H")) + 2) + " Id del usuario: " + str(tweet.author.id))

            if tweet.in_reply_to_status_id is not None or \
                    tweet.user.id == self.me.id:
                # Comprueba que el tuit no esté escrito por mí ni que sea una respuesta
                return
            if not tweet.favorited:
                # Le da like al tuit
                try:
                    tweet.favorite()
                    print("Tuit marcado como me gusta")
                except Exception as e:
                    logger.error("Error al dar me gusta", exc_info=True)

            if not tweet.retweeted:
                # Retuitea
                try:
                    tweet.retweet()
                except Exception as e:
                    logger.error("Error al retuitear", exc_info=True)


    def on_error(self, status):
        logger.error(status)


def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(languages=["es"], follow=cuentas, track=keywords)

if __name__ == "__main__":
    main(["#BomberosCM", "#bomberoscm", "#Infoma21", "#INFOMA21"])
