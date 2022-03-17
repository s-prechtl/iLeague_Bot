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
        err = "Something went wrong.\nUsage: " + self.pref + "hm [count] [Summonername]"
        firstIsInt = intTryParse(message.content.split(" ")[1])[1]

        if len(message.content.split(" ")) > 2 and firstIsInt:  # If number is given
            try:
                sumname = APICommands.Command.getSummonerNameFromMessage(message, 2)
            except Exception as e:
                await message.channel.send(err)
                print("Exception in Mastery " + str(e))
            if sumname != "":
                if not await self.checkSumname(sumname, message):
                    return
                try:
                    listlen = int(message.content.split(" ")[1])
                    output = self.getChampionMasteryList(sumname, listlen)
                    for i in output:
                        await message.channel.send(i)
                except Exception as e:
                    await message.channel.send(err)
                    print("Exception in Mastery " + str(e))
        elif not firstIsInt:  # no number given
            try:
                sumname = APICommands.Command.getSummonerNameFromMessage(message, 1)
            except Exception as e:
                await message.channel.send(err)
                print("Exception in Mastery " + str(e))
            if sumname != "":
                try:
                    listlen = 10
                    output = self.getChampionMasteryList(sumname, listlen)
                    for i in output:
                        await message.channel.send(i)
                except Exception as e:
                    await message.channel.send(err)

    async def info(self, message: discord.Message):
        pass

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

    async def usage(self, message: discord.Message):
        pass
