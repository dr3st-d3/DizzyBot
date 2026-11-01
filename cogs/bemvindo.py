
import discord
from discord.ext import commands


class BemVindo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

# Comando de Boas-vindass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        canal = self.bot.get_channel(1564792258451087534)

        if canal is None:
            print("Canal de boas vindas não encontrado.")
            return

        embed = discord.Embed(
            title="Bem-vindo(a) ao servidor! 🎉",
            description=(
                f"Olá {member.mention}, seja bem-vindo(a) "
                "ao servidor do Léo! Esperamos que você "
                "se divirta e aproveite a comunidade. 💙"
            ),
            color=discord.Color.from_rgb(0, 0, 255)
        )

        await canal.send(embed=embed)

# Comando de Despedida

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        canal = self.bot.get_channel(1564792258451087534)

        if canal is None:
            print("Canal de despedida não encontrado.")
            return

        embed = discord.Embed(
            title="Adeus! 😢",
            description=(
                f"Nos vemos assim que possível, {member.mention}! "
            ),
            color=discord.Color.from_rgb(255, 0, 0)
        )

        await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BemVindo(bot))
