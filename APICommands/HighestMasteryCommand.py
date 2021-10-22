from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class HighestMastery(APICommands.Command.Command, ABC):
    keywords = ["highestmastery", "highestMastery", "HM", "hm", "Hm", "HighestMastery"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, additionalKeywords: list):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, additionalKeywords)

    async def execute(self, message: discord.Message):
        pass

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        pass
