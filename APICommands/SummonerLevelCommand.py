from abc import ABC

import discord
import riotwatcher

import APICommands.Command
from APICommands.Command import getSummonerNameFromMessage


class SummonerLevel(APICommands.Command.Command, ABC):
    keywords = ["level", "Level", "lvl"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords: list):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        sumname = ""
        try:
            sumname = getSummonerNameFromMessage(message)
        except:
            await self.usage(message)
        if sumname != "":
            level = await self.requestLevel(sumname, message)
            if level is not None:
                await message.channel.send("Der Spieler " + sumname + " hat das Level " + str(level) + ".")

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        await message.channel.send("Wrong usage of " + self.commandName + "! Use " + self.pref + "level [Summoner]")

    async def requestLevel(self, sumname: str, message: discord.Message):
        if not await self.checkSumname(sumname, message):
            return
        response = self.api.summoner.by_name(self.region, sumname)
        return response["summonerLevel"]

