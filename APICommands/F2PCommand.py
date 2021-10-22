from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class Free2Play(APICommands.Command.Command, ABC):
    keywords = ["f2p", "rotation", "F2P", "ROTATION"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, additionalKeywords=None):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, additionalKeywords)

    async def execute(self, message: discord.Message):
        pass

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        pass
