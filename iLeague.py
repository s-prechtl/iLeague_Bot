import datetime
import json

import discord
import pickle
import requests
from riotwatcher import LolWatcher

from APICommands import ChampionMasteryCommand, HighestMasteryCommand, SummonerLevelCommand, PrefixCommand, SummonerRankCommand





class MyClient(discord.Client):
    api: LolWatcher
    region: str
    pref = "$"
    commands = []

    def initAPI(self, APIKey, region="EUW1"):
        self.api = LolWatcher(APIKey)
        self.region = region
        self.initCommands()

    def initCommands(self):
        self.commands = []
        self.commands.append(ChampionMasteryCommand.ChampionMastery(self.pref, self.api, self.region, []))
        self.commands.append(HighestMasteryCommand.HighestMastery(self.pref, self.api, self.region, []))
        self.commands.append(SummonerLevelCommand.SummonerLevel(self.pref, self.api, self.region, []))
        self.commands.append(PrefixCommand.Prefix(self.pref, self.api, self.region, []))
        self.commands.append(SummonerRankCommand.SummonerRank(self.pref, self.api, self.region, []))

    def load(self):  # Loads the prefix file if accessable
        try:
            self.pref = pickle.load(open("prefix.data", "rb"))
            print("Prefix loaded as: " + self.pref)
        except:
            print("No File found.")

    async def on_ready(self):
        print("Beep Boop, suck my cock")

    async def on_message(self, message):
        if message.author == client.user:  # Checks if the User isnt the bot itself
            return

        # COMMANDS
        if message.content.startswith(self.pref) and isinstance(message, discord.Message) and isinstance(self.api,
                                                                                                         LolWatcher):
            if not (
                    message.channel.id == 843900656108437504 or message.channel.id == 673681791932170240):  # Only allows channels bot testing and leaguebot
                await message.channel.send("Bitte #league-bot verwenden.")
                return

            for command in self.commands:
                if command.isCalled(message):
                    command.log(message)
                    await command.execute(message)



            # HUBA
            if message.content == self.pref + "huba":
                self.log("Huawa", message)
                await message.channel.send(
                    "Julian Huber (17) ist ein Kinderschänder, welcher in Wahrheit schwul ist und seine sexuelle "
                    "Orientierung hinter einer Beziehung mit einem weiblichen Kind versteckt.")

            if True:
                return

            # FREE CHAMPS
            elif self.getContentFromMessageWithPrefixCommand(message, ["f2p", "rotation", "F2P", "ROTATION"]):
                self.log("F2P rotation", message)
                await self.requestFreeChampRot(message)

    async def requestFreeChampRot(self, message: discord.Message):
        err = "Something went wrong.\nUsage: " + self.pref + "f2p [Summonername]"
        sumname = ""
        output = "Derzeitige F2P Champions"
        rot = self.api.champion.rotations(self.region)["freeChampionIds"]
        championsJSON = getChampionsJSON()
        try:
            sumname = self.getSummonerNameFromMessage(message, 1)
        except Exception:
            pass

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
                if not i in allIds:
                    output += ("ㅤ\t- **" + championIdToName(i, championsJSON) + "**\n")
        else:
            output += ":\n"
            for i in rot:
                output += ("ㅤ\t- **" + championIdToName(i, championsJSON) + "**\n")

        await message.channel.send(output)
        if len(output.split("\n")) <= 2:
            await message.channel.send("ㅤ\t- **Keine**")




if __name__ == '__main__':
    client = MyClient()
    client.load()
    with open("API.key", "r") as f:
        client.initAPI(f.read())
    with open("Discord.key", "r") as f:
        client.run(f.read())
