from abc import ABC

import discord
import riotwatcher

import APICommands.Command
from APICommands.Command import getSummonerNameFromMessage, getChampionsJSON, championIdToName


class Free2Play(APICommands.Command.Command, ABC):
    commandName = "Free 2 Play"
    keywords = ["f2p", "rotation", "F2P", "ROTATION"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords=None):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        sumname = ""
        output = "Derzeitige F2P Champions"
        rot = self.api.champion.rotations(self.region)["freeChampionIds"]
        championsJSON = getChampionsJSON()
        try:
            sumname = getSummonerNameFromMessage(message, 1)
        except:
            await self.usage(message)

        if sumname != "":
            if not await self.checkSumname(sumname, message):
                return
            output += " auf denen **" + sumname + "** noch keine Punkte hast: \n"
            response = self.api.champion_mastery.by_summoner(self.region,
                                                             self.api.summoner.by_name(self.region,
                                                                                       sumname)["id"])
            allIds = []
            for i in response:
                allIds.append(i["championId"])

            for i in rot:
                if i not in allIds:
                    output += ("ㅤ\t- **" + championIdToName(i, championsJSON) + "**\n")
        else:
            output += ":\n"
            for i in rot:
                output += ("ㅤ\t- **" + championIdToName(i, championsJSON) + "**\n")

        await message.channel.send(output)
        if len(output.split("\n")) <= 2:
            await message.channel.send("ㅤ\t- **Keine**")

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        await message.channel.send("Wrong usage of" + self.commandName + "!\nUsage: " + self.pref + "f2p [Summoner ("
                                                                                                    "optional)]")
