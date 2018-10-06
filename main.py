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

    async def on_message(self, message):
        """
        Detect new stars and append them to the queue
        """
        # TODO: Do the above
        # When appending stars to the queue, use the Star class, so that the data is in a consistent format for
        # the reddit module
        pass


if __name__ == '__main__':
    DIA().run()
