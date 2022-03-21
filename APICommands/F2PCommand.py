from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class Free2Play(APICommands.Command.Command, ABC):
    commandName = "Free 2 Play"
    keywords = ["f2p", "rotation", "F2P", "ROTATION"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords=None):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        pass

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        pass
