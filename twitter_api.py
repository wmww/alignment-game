from tweepy import API, StreamListener, Stream, OAuthHandler # type: ignore
from dotenv import load_dotenv
import os
from os import environ
import logging

secrets_path = 'secrets/secrets.env'

logger = logging.getLogger(__name__)
auth_global = None
api_global = None

def get_environ_or_raise(name: str):
    value = environ.get(name)
    if value:
        return value
    else:
        raise RuntimeError('environment variable ' + name + ' not set')

def lazy_get_auth():
    global auth_global
    if auth_global:
        return auth_global
    if not os.path.exists(secrets_path):
        logger.warning(secrets_path + ' does not exists, secrets will need to be stored in environment variables')
    load_dotenv(secrets_path)
    consumer_key = get_environ_or_raise('TWITTER_CONSUMER_API_KEY')
    consumer_secret = get_environ_or_raise('TWITTER_CONSUMER_API_SECRET_KEY')
    access_token = get_environ_or_raise('TWITTER_ACCESS_TOKEN')
    access_token_secret = get_environ_or_raise('TWITTER_ACCESS_TOKEN_SECRET')
    logger.info('Building tweepy auth object')
    auth_global = OAuthHandler(consumer_key, consumer_secret)
    auth_global.set_access_token(access_token, access_token_secret)
    return auth_global

def lazy_get_api():
    global api_global
    if api_global:
        return api_global
    auth = lazy_get_auth()
    logger.info('Building tweepy API object')
    api_global = API(auth)
    return api_global

def post_text_tweet(message: str):
    api = lazy_get_api()
    status = api.update_status(message)
    logger.info('Posted "%s" on behalf of @%s', status.text, status.user.screen_name)

class Listener(StreamListener):
    def on_connect(self):
        logger.info('Listener connected')

    def on_disconnect(self, notice):
        logger.info('Listener disconnected: %s', notice)

    def on_direct_message(self, status):
        logger.info('DM received: ', status)

    def on_status(self, status):
        logger.info('Got tweet from @%s: "%s"', status.author.screen_name, status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # This means we've hit a rate limit
            # Returning False in on_error disconnects the stream
            logger.warning('Got error 420, disconnecting stream')
            return False
        else:
            logger.warning('Got error %s', status_code)

def listen():
    listener = Listener()
    auth = lazy_get_auth()
    stream = Stream(auth=auth, listener=listener)
    stream.userstream()
