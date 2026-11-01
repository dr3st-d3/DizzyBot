
import discord
from discord.ext import commands


class BemVindo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

# Comando de Boas-vindas

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        canal = self.bot.get_channel(1564792258451087534)

        if canal is None:
            print("Canal de boas vindas não encontrado.")
            return

        embed = discord.Embed(
            title="Bem-vindo(a) ao servidor! 🎉",
            description=(
                f"Usuário: {member.mention}\n"
                f"Membro n°: {member.guild.member_count}\n"
                f"Esperamos que você se divirta, aproveite sua estadia aqui! "
            ),
            color=discord.Color.from_rgb(0, 0, 255)
        )

        embed.set_thumbnail(url=member.display_avatar.url)

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
                f"Usuário: {member.mention}\n"
                f"Nos vemos assim que possível!"
            ),
            color=discord.Color.from_rgb(255, 0, 0)
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BemVindo(bot))
