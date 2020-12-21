"""Main file to start the whole bot."""
import logging
import discord
from client.client import BotClient

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def get_token():
    """Get a token from a local file."""
    try:
        with open("tkn") as f:
            lines = f.readlines()
            return lines[0]
    except IOError:
        logger.log("Token file not found.")
    return "token"


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = BotClient(command_prefix=".", intents=intents)
client.run(get_token())
