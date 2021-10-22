from abc import abstractmethod, ABCMeta
from datetime import datetime

import discord
import riotwatcher


class Command:
    __metaclass__ = ABCMeta
    keywords = []
    pref = ""
    api: riotwatcher.LolWatcher
    commandName = ""

    def __init__(self, pref, api: riotwatcher.LolWatcher, additionalKeywords: list):
        for i in additionalKeywords:
            self.keywords.append(i)
        self.pref = pref
        self.api = api

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
