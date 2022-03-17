import datetime
import json

import discord
import pickle
import requests
from riotwatcher import LolWatcher

from APICommands import ChampionMasteryCommand, HighestMasteryCommand, SummonerLevelCommand, PrefixCommand


def championIdToName(id, championsText):
    champions = json.loads(championsText)['data']

    for j in dict(champions):
        if id == int(champions[j]["key"]):
            return j


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
            if self.getContentFromMessageWithPrefixCommand(message, ["hubaa"]):
                self.log("Huawa", message)
                await message.channel.send(
                    "Julian Huber (16) ist ein Kinderschänder, welcher in Wahrheit schwul ist und seine sexuelle "
                    "Orientierung hinter einer Beziehung mit einem weiblichen Kind versteckt.")

            # LEVEL
            elif self.getContentFromMessageWithPrefixCommand(message, ["level", "Level", "lvl"]):
                await self.requestLevel(message)

                # RANK
            elif self.getContentFromMessageWithPrefixCommand(message, ["rank", "Rank", "RANK"]):
                self.log("Summoner level", message)
                await self.requestRank(message)

                # HIGHEST MASTERY
            elif self.getContentFromMessageWithPrefixCommand(message,
                                                             ["highestmastery", "highestMastery", "HM", "hm", "Hm",
                                                              "HighestMastery"]):
                self.log("Highest mastery", message)
                await self.requestHighestMastery(message)

            elif self.getContentFromMessageWithPrefixCommand(message, ["cm", "CM", "Championmastery",
                                                                       "championmastery"]):  # get Mastery from Champion
                self.log("Summoner champion mastery", message)
                await self.requestChampionMastery(message)

            # FREE CHAMPS
            elif self.getContentFromMessageWithPrefixCommand(message, ["f2p", "rotation", "F2P", "ROTATION"]):
                self.log("F2P rotation", message)
                await self.requestFreeChampRot(message)

    async def changePrefix(self, message: discord.Message):
        try:
            self.pref = message.content.split(" ")[1]
            await message.channel.send("Prefix successfully changed to " + self.pref)
            pickle.dump(self.pref, open("prefix.data", "wb"))
        except:
            await message.channel.send(
                "Something went wrong while changing the prefix. To change it use " + self.pref + "prefix [new Prefix]")

    async def requestRank(self, message: discord.Message):
        sumname = ""
        try:
            sumname = self.getSummonerNameFromMessage(message)
        except:
            await message.channel.send("Something went wrong.\n"
                                       "Usage: " + self.pref + "rank [Summonername]")

        if sumname != "":
            if not await self.checkSumname(sumname, message):
                return
            print("Summonerrank request sent in Channel " + str(message.channel.name))
            response = self.api.league.by_summoner(self.region,
                                                   self.api.summoner.by_name(self.region, sumname)["id"])
            for i in response:
                if i["queueType"] == "RANKED_SOLO_5x5":
                    response = i
            rank = str(response['tier']) + " " + str(response['rank'])
            wr = str(truncate((response["wins"] / (response["wins"] + response["losses"]) * 100), 2)) + "%"
            await message.channel.send(sumname + ": " + str(rank) + " | WR: " + str(wr))

    async def requestHighestMastery(self, message: discord.Message):
        sumname = ""
        err = "Something went wrong.\nUsage: " + self.pref + "hm [count] [Summonername]"
        firstIsInt = intTryParse(message.content.split(" ")[1])[1]

        if len(message.content.split(" ")) > 2 and firstIsInt:  # If number is given
            try:
                sumname = self.getSummonerNameFromMessage(message, 2)
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
                sumname = self.getSummonerNameFromMessage(message, 1)
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

    async def requestChampionMastery(self, message: discord.Message):
        err = "Something went wrong.\nUsage: " + self.pref + "cm [Championname] [Summonername]"
        sumname = ""
        try:
            sumname = self.getSummonerNameFromMessage(message, 2)
        except Exception as e:
            await message.channel.send(err)

        if sumname != "":
            if not await self.checkSumname(sumname, message):
                return

            response = self.api.champion_mastery.by_summoner(self.region,
                                                             self.api.summoner.by_name(self.region,
                                                                                       sumname)["id"])

            championsJSON = self.getChampionsJSON()
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

    async def requestFreeChampRot(self, message: discord.Message):
        err = "Something went wrong.\nUsage: " + self.pref + "f2p [Summonername]"
        sumname = ""
        output = "Derzeitige F2P Champions"
        rot = self.api.champion.rotations(self.region)["freeChampionIds"]
        championsJSON = self.getChampionsJSON()
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



    def getChampionMasteryList(self, sumname, listlen):
        output = ["Der Spieler " + sumname + " hat den höchsten Mastery auf diesen " + str(
            listlen) + " Champions\n"]
        count = 0
        response = self.api.champion_mastery.by_summoner(self.region, self.getEncryptedSummonerID(sumname))[
                   :listlen]
        championsJSON = self.getChampionsJSON()
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

    def getEncryptedSummonerID(self, name):
        return self.api.summoner.by_name(self.region, name)["id"]

    def getChampionsJSON(self):
        return requests.get("http://ddragon.leagueoflegends.com/cdn/11.19.1/data/en_US/champion.json").text


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * n)[:n]])


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


if __name__ == '__main__':
    client = MyClient()
    client.load()
    with open("API.key", "r") as f:
        client.initAPI(f.read())
    with open("Discord.key", "r") as f:
        client.run(f.read())
