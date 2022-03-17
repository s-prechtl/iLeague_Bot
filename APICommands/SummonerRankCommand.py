from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class SummonerRank(APICommands.Command.Command, ABC):
    keywords = ["rank", "Rank", "RANK"]

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
