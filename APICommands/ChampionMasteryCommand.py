from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class ChampionMastery(APICommands.Command.Command, ABC):
    keywords = ["cm", "CM", "Championmastery", "championmastery"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords: list):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        pass

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        pass
