import os
import discord
from discordbot import *

if __name__ == "__main__":

    # Start the program
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    client = discord.Client(intents = intents)
    Read.read_msgs(client)
    client.run(TOKEN)