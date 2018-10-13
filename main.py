#!/usr/bin/python3

from datetime import datetime
import yaml
import discord
from discord.ext import commands
import logging

from .stars import Star, StarQueue


class DIA(commands.Bot):

    def __init__(self, prefixes: str="DIA-"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.debug("Started process")

        self.watched_channels = []
        self.prefixes = prefixes
        self.tokens = self.find_tokens()

        self.stars = StarQueue()
        # Queue of stars that the bot can append new stars onto
        # and the Reddit posting module can pull stars from
        # Both can work independently and simultaneously
        # self.stars.append(Star(...)) - Add a star to be posted
        # self.stars.pop() - Get next star to post to Reddit

        self.presence = discord.Game(name=f'dapi-in-action | DIA-')

        super().__init__(self.prefixes, activity=self.presence)

    def find_tokens(self):
        try:
            with open("tokens.yaml", 'r') as stream:
                self.logger.debug("Loaded token file")
                tokens = yaml.load(stream)
                return tokens
        except FileNotFoundError:
            self.logger.error("token.yaml not found! Exiting...")
            exit(1)

    def run(self):
        try:
            super().run(self.tokens['discord_token'])
        except discord.LoginFailure:
            self.logger.error("Improper token has been passed! Exiting...")
            exit(1)

    async def on_ready(self):
        self.logger.info("Hello DAPI!")
        self.logger.debug(f"Logged in at {datetime.now()}")

    async def on_message(self, message: discord.Message):
        """
        Detect new stars and append them to the queue
        """
        # Check if this is a starboard & if we have a rich embed attached to the message
        if message.channel.id not in self.watched_channels:
            return
        
        embed = next(ebd for ebd in message.embeds if ebd.type == "rich")

        if embed is None:
            return

        mid = int(message.content.split("ID: ")[1])
        image = None if embed.image.url is discord.Embed.Empty else embed.image.url
        star = Star(message_id=mid, author=embed.author.name, title="?", content=embed.description, img_url=image)

        self.stars.append(star)


if __name__ == '__main__':
    DIA().run()
