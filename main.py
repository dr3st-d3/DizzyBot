import os 
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN =  os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("O Token do Discord não foi encontrado.")

class DizzyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):

        for arquivo in os.listdir("./cogs"):
            if arquivo.endswith(".py") and not arquivo.startswith("__"):
                await self.load_extension(f"cogs.{arquivo[:-3]}")

                print(f"Cog carregado: {arquivo}")

        comandos = await self.tree.sync()
        print(f"Comandos sincronizados: {len(comandos)}")

    async def on_ready(self):
        print(f"{self.user} foi iniciado e está pronto para uso!")

bot = DizzyBot()

bot.run(DISCORD_TOKEN)