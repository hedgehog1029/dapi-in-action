#!/usr/bin/python3

from datetime import datetime
import yaml
import discord
from discord.ext import commands
import logging


class DIA(commands.Bot):

    def __init__(self, prefixes: str="DIA-"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.debug("Started process")

        self.prefixes = prefixes
        self.tokens = self.find_tokens()

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


if __name__ == '__main__':
    DIA().run()
