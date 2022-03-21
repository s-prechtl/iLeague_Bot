import pickle
from abc import ABC

import discord
import riotwatcher

import APICommands.Command


class Prefix(APICommands.Command.Command, ABC):
    commandName = "Prefix"
    keywords = ["prefix"]

    def __init__(self, pref, api: riotwatcher.LolWatcher, region: str, additionalKeywords=None):
        if additionalKeywords is None:
            additionalKeywords = []
        super().__init__(pref, api, region, additionalKeywords)
        self.commandName = "Prefix change"

    async def execute(self, message: discord.Message):
        if message.content == (self.pref + "prefix"):
            await self.info(message)
        elif message.content.split(" ").length == 2:
            self.log(message)
            await self.changePrefix(message)
        else:
            await self.usage(message)

    async def info(self, message: discord.Message):
        await message.channel.send(
            "Your current prefix is: " + self.pref + ". To change it use " + self.pref + "prefix [new Prefix]")

    async def usage(self, message: discord.Message):
        await message.channel.send("Wrong usage of" + self.commandName + "! Use " + self.pref + "prefix [new Prefix ("
                                                                                                "optional)]")

    async def changePrefix(self, message: discord.Message):
        try:
            self.pref = message.content.split(" ")[1]
            await message.channel.send("Prefix successfully changed to " + self.pref)
            pickle.dump(self.pref, open("prefix.data", "wb"))
        except:
            await self.usage(message)
