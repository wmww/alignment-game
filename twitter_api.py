from twitter import Api # type: ignore
from dotenv import load_dotenv
import os
from os import environ
import logging

secrets_path = 'secrets/secrets.env'

logger = logging.getLogger(__name__)
api_global = None

def get_environ_or_raise(name: str):
    value = environ.get(name)
    if value:
        return value
    else:
        raise RuntimeError('environment variable ' + name + ' not set')

def lazy_get_api():
    global api_global
    if api_global:
        return api_global
    if not os.path.exists(secrets_path):
        logger.warning(secrets_path + ' does not exists, secrets will need to be stored in environment variables')
    load_dotenv(secrets_path)
    consumer_key = get_environ_or_raise('TWITTER_CONSUMER_API_KEY')
    consumer_secret = get_environ_or_raise('TWITTER_CONSUMER_API_SECRET_KEY')
    access_token_key = get_environ_or_raise('TWITTER_ACCESS_TOKEN')
    access_token_secret = get_environ_or_raise('TWITTER_ACCESS_TOKEN_SECRET')
    logger.info('Building new Twitter API object')
    api_global = Api(consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)
    return api_global

def post_text_tweet(message: str):
    api = lazy_get_api()
    status = api.PostUpdate(message)
    logger.info('Posted "' + str(status.text) + '" on behalf of @' + str(status.user.screen_name))
