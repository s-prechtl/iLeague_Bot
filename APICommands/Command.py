import json
from abc import abstractmethod, ABCMeta
from datetime import datetime

import discord
import requests
import riotwatcher


def championIdToName(id, championsText):
    champions = json.loads(championsText)['data']

    for j in dict(champions):
        if id == int(champions[j]["key"]):
            return j


def getChampionsJSON():
    return requests.get("http://ddragon.leagueoflegends.com/cdn/11.19.1/data/en_US/champion.json").text


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def getSummonerNameFromMessage(message: discord.Message, argumentstart=1):
    ret = ""
    inp = message.content.split(" ")
    if len(inp) > argumentstart + 1:
        for i in inp[argumentstart:]:
            ret += " " + i

        ret = ret[1:]
    else:
        ret = inp[argumentstart]
    return ret


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

    async def checkSumname(self, sumname, message: discord.Message):
        try:
            self.api.summoner.by_name(self.region, sumname)["id"]
            return True
        except requests.exceptions.HTTPError:
            await message.channel.send("No matching player found with name **" + sumname + "**")
            return False

    def getEncryptedSummonerID(self, name):
        return self.api.summoner.by_name(self.region, name)["id"]
