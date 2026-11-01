
import discord
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="vai-la-dizzy",
        description="Interage com Dizzy"
    )
    async def vaila_dizzy(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "BWIP-BWIP!! BWEHHH!! 💙"
        )


async def setup(bot):
    await bot.add_cog(General(bot))
