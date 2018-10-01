#!/usr/bin/python3

from datetime import datetime
import yaml
import discord
from discord.ext import commands


class DIA(commands.Bot):
    def __init__(self, prefixes: str="DIA-"):
        print("Started:", datetime.now())
        self.prefixes = prefixes
        self.tokens = self.find_tokens()

        self.presence = discord.Game(name=f'dapi-in-action | DIA-')

        super().__init__(self.prefixes, activity=self.presence)

    def find_tokens(self):
        with open("tokens.yaml", 'r') as stream:
            tokens = yaml.load(stream)
            return tokens

    def run(self):
        super().run(self.tokens['discord_token'])

    async def on_ready(self):
        print("Hello DAPI!")
        print("Logged in:", datetime.now())


if __name__ == '__main__':
    DIA().run()
