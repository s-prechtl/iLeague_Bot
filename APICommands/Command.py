from abc import abstractmethod, ABCMeta
from datetime import datetime

import discord
import requests
import riotwatcher


class Command:
    __metaclass__ = ABCMeta
    keywords = []
    pref = ""
    api: riotwatcher.LolWatcher
    commandName = ""
    region = ""

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords: list):
        for i in additionalKeywords:
            self.keywords.append(i)
        self.pref = pref
        self.api = api
        self.region = region

    @abstractmethod
    async def execute(self, message: discord.Message):
        pass

    @abstractmethod
    async def info(self, message: discord.Message):
        pass

    @abstractmethod
    async def usage(self, message: discord.Message):
        pass

    def isCalled(self, message: discord.Message):
        for i in self.keywords:
            if message.content.startswith(self.pref + i):
                return True
        return False

    def log(self, message: discord.Message):
        logMSG = (self.commandName + " request sent:\n\t-in: " + str(message.channel.name) + "\n\t- at: " + str(
            datetime.now())[:-7] + "\n\t- by: " + str(message.author) + "\n\t- content: '" + str(
            message.content) + "'\n")
        print(logMSG)
        with open("requests.log", "a") as f:
            f.write(logMSG)

    def getSummonerNameFromMessage(self, message: discord.Message, argumentstart=1):
        ret = ""
        inp = message.content.split(" ")
        if len(inp) > argumentstart + 1:
            for i in inp[argumentstart:]:
                ret += " " + i

            ret = ret[1:]
        else:
            ret = inp[argumentstart]
        return ret

    async def checkSumname(self, sumname, message: discord.Message):
        try:
            var = self.api.summoner.by_name(self.region, sumname)["id"]
            return True
        except requests.exceptions.HTTPError:
            await message.channel.send("No matching player found with name **" + sumname + "**")
            return False
