from abc import ABC

import discord
import riotwatcher

import APICommands.Command


def truncate(f, n):
    """Truncates/pads a float f to n decimal places without rounding"""
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * n)[:n]])


class SummonerRank(APICommands.Command.Command, ABC):
    keywords = ["rank", "Rank", "RANK"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords=None):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)

    async def execute(self, message: discord.Message):
        sumname = ""
        try:
            sumname = APICommands.Command.getSummonerNameFromMessage(message)
        except:
            await self.usage(message)

        if sumname != "":
            if not await self.checkSumname(sumname, message):
                return
            response = self.api.league.by_summoner(self.region,
                                                   self.api.summoner.by_name(self.region, sumname)["id"])
            for i in response:
                if i["queueType"] == "RANKED_SOLO_5x5":
                    response = i
            rank = str(response['tier']) + " " + str(response['rank'])
            wr = str(truncate((response["wins"] / (response["wins"] + response["losses"]) * 100), 2)) + "%"
            await message.channel.send(sumname + ": " + str(rank) + " | WR: " + str(wr))

    async def info(self, message: discord.Message):
        pass

    async def usage(self, message: discord.Message):
        await message.channel.send("Wrong usage of " + self.commandName + ".\n"
                                   "Usage: " + self.pref + "rank [Summonername]")
