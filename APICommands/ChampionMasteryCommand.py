from abc import ABC

import discord
import riotwatcher

import APICommands.Command
from APICommands.Command import getSummonerNameFromMessage, getChampionsJSON, championIdToName


class ChampionMastery(APICommands.Command.Command, ABC):
    keywords = ["cm", "CM", "Championmastery", "championmastery"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords: list):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        sumname = ""
        try:
            sumname = getSummonerNameFromMessage(message, 2)
        except:
            await self.usage(message)

        if sumname != "":
            if not await self.checkSumname(sumname, message):
                return

            response = self.api.champion_mastery.by_summoner(self.region,
                                                             self.api.summoner.by_name(self.region,
                                                                                       sumname)["id"])

            championsJSON = getChampionsJSON()
            for i in response:
                champname = championIdToName(i["championId"], championsJSON)
                if champname == message.content.split(" ")[1]:
                    mpoints = i["championPoints"]
                    mastery = i["championLevel"]
                    out = "**" + sumname + "** --> **" + champname + "**" + " Points: " + str(
                        mpoints) + " Level: " + str(
                        mastery) + "\n"

                    await message.channel.send(out)
                    return
            await message.channel.send("No matching champion was found.")

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        await message.channel.send("Wrong usage of " + self.commandName + "!\nUsage: " + self.pref + "cm [champion] ["
                                                                                                     "Summoner]")
