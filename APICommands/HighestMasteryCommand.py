from abc import ABC

import discord
import riotwatcher

import APICommands.Command
from iLeague import intTryParse, championIdToName, getChampionsJSON


class HighestMastery(APICommands.Command.Command, ABC):
    keywords = ["highestmastery", "highestMastery", "HM", "hm", "Hm", "HighestMastery"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords: list):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        sumname = ""
        firstIsInt = intTryParse(message.content.split(" ")[1])[1]

        try:
            sumname = APICommands.Command.getSummonerNameFromMessage(message, 2)
        except:
            await self.usage(message)
        if sumname != "":
            if not await self.checkSumname(sumname, message):
                return
            listlen = int(message.content.split(" ")[1]) if firstIsInt else 10
            try:
                output = getChampionMasteryList(sumname, listlen)
                for i in output:
                    await message.channel.send(i)
            except:
                await self.usage(message)


async def info(self, message: discord.Message):
    pass


async def usage(self, message: discord.Message):
    await message.channel.send("Wrong usage of" + self.commandName + "!\nUsage: " + self.pref + "hm [count] ["
                                                                                                "Summonername]")


def getChampionMasteryList(self, sumname, listlen):
    output = ["Der Spieler " + sumname + " hat den höchsten Mastery auf diesen " + str(
        listlen) + " Champions\n"]
    count = 0
    response = self.api.champion_mastery.by_summoner(self.region, self.getEncryptedSummonerID(sumname))[
               :listlen]
    championsJSON = getChampionsJSON()
    for i in response:
        champname = championIdToName(i["championId"], championsJSON)
        mpoints = i["championPoints"]
        mastery = i["championLevel"]
        out = "**" + champname + "**" + " Points: " + str(mpoints) + " Level: " + str(
            mastery) + "\n"
        if len(output[count]) + len(out) >= 2000:
            output.append("")
            count += 1
        output[count] += out
    return output
