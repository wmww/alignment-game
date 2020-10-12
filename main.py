import twitter_api

from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    load_dotenv(verbose=True)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logger.info('Posting Tweet…')
    twitter_api.post_text_tweet('Hello Twitter')
