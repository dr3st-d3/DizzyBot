import os
import discord

from discord import app_commands
from dotenv import load_dotenv

# Carregar configurações
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise RuntimeError("Configure o token do discord no arquivo .env")


class DizzyBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        comandos = await self.tree.sync()
        print(f"Comandos sincronizados: {len(comandos)}")

    async def on_ready(self):
        print(f"{self.user} foi iniciado e está pronto para uso.")


bot = DizzyBot()


# Comando: interação com Dizzy

@bot.tree.command(
    name="vai-la-dizzy",
    description="Interage com Dizzy"
)
async def vaila_dizzy(interaction: discord.Interaction):

    await interaction.response.send_message(
        "BWIP-BWIP!! BWEHHH!! 💙"
    )


# Evento: mensagem de boas-vindas

@bot.event
async def on_member_join(member: discord.Member):

    canal = bot.get_channel(1564792258451087534)

    if canal is None:
        print("Canal de boas-vindas não encontrado!")
        return

    embed = discord.Embed(
        title="Bem-vindo(a) ao servidor! 🎉",
        description=(
            f"Olá {member.mention}, seja bem-vindo(a) "
            "ao servidor do Léo! Esperamos que você se "
            "divirta e aproveite a comunidade. 💙"
        ),
        color=discord.Color.from_rgb(0, 0, 255)
    )

    await canal.send(embed=embed)


# Inicialização

bot.run(DISCORD_TOKEN)
