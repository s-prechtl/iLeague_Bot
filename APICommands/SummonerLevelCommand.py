from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class SummonerLevel(APICommands.Command.Command, ABC):
    keywords = ["level", "Level", "lvl"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, additionalKeywords: list):
        super().__init__(pref, api, additionalKeywords)

    async def execute(self, message: discord.Message):
        pass

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        pass