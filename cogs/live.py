
import discord
from discord import app_commands
from discord.ext import commands, tasks

from TikTokLive import TikTokLiveClient

from services.live_monitor import (
    criar_tabela,
    adicionar_perfil,
    remover_perfil,
    listar_perfis,
    atualizar_status
)


# CONFIGURAÇÕES
CANAL_DIVULGACAO = 123456789012345678


class Live(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        criar_tabela()

    async def cog_load(self):
        self.verificar_lives.start()

    async def cog_unload(self):
        self.verificar_lives.cancel()

    # ----------------------------------
    # CONTAINER DA DIVULGAÇÃO
    # ----------------------------------

    def criar_divulgacao(self, username):

        link = f"https://www.tiktok.com/@{username}/live"

        view = discord.ui.LayoutView()

        container = discord.ui.Container(
            discord.ui.TextDisplay(
                "## 🔴 ESTÁ AO VIVO!\n"
                f"**@{username}** começou uma transmissão no TikTok!\n\n"
                "Entre agora e acompanhe a LIVE."
            ),
            discord.ui.Separator(),

            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Assistir LIVE",
                    style=discord.ButtonStyle.link,
                    url=link
                )
            ),

            accent_colour=discord.Colour.from_rgb(254, 44, 85)
        )

        view.add_item(container)

        return view

    # ----------------------------------
    # PUBLICAR DIVULGAÇÃO
    # ----------------------------------

    async def publicar_live(self, username):

        canal = self.bot.get_channel(CANAL_DIVULGACAO)

        if canal is None:
            canal = await self.bot.fetch_channel(
                CANAL_DIVULGACAO
            )

        view = self.criar_divulgacao(username)

        await canal.send(view=view)

        print(f"Divulgação publicada: @{username}")

    # ----------------------------------
    # MONITORAMENTO
    # ----------------------------------

    @tasks.loop(minutes=2)
    async def verificar_lives(self):

        perfis = listar_perfis()

        for username, estava_ao_vivo in perfis:

            try:
                client = TikTokLiveClient(
                    unique_id=username
                )

                ao_vivo = await client.is_live()

                if ao_vivo and not estava_ao_vivo:

                    await self.publicar_live(username)

                    atualizar_status(username, True)

                    print(f"@{username} iniciou uma LIVE!")

                elif not ao_vivo and estava_ao_vivo:

                    atualizar_status(username, False)

                    print(f"@{username} encerrou a LIVE.")

            except Exception as erro:

                print(
                    f"Erro ao verificar @{username}: {erro}"
                )

    @verificar_lives.before_loop
    async def antes_de_verificar(self):
        await self.bot.wait_until_ready()

    # ----------------------------------
    # CADASTRAR PERFIL
    # ----------------------------------

    @app_commands.command(
        name="registrarlive",
        description="Cadastra um perfil do TikTok."
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def registrar_live(
        self,
        interaction: discord.Interaction,
        usuario: str
    ):

        username = usuario.strip().removeprefix("@")

        if not username or "/" in username or " " in username:
            await interaction.response.send_message(
                "Informe apenas o nome de usuário do TikTok.",
                ephemeral=True
            )
            return

        try:
            adicionar_perfil(username)

            await interaction.response.send_message(
                f"Perfil **@{username}** cadastrado com sucesso!",
                ephemeral=True
            )

        except Exception:
            await interaction.response.send_message(
                "Esse perfil já está cadastrado.",
                ephemeral=True
            )

    # ----------------------------------
    # REMOVER PERFIL
    # ----------------------------------

    @app_commands.command(
        name="removerlive",
        description="Remove um perfil do monitoramento."
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def remover_live(
        self,
        interaction: discord.Interaction,
        usuario: str
    ):

        username = usuario.strip().removeprefix("@")

        removido = remover_perfil(username)

        mensagem = (
            f"Perfil **@{username}** removido."
            if removido
            else "Esse perfil não está cadastrado."
        )

        await interaction.response.send_message(
            mensagem,
            ephemeral=True
        )

    # ----------------------------------
    # LISTAR PERFIS
    # ----------------------------------

    @app_commands.command(
        name="listarlives",
        description="Lista os perfis monitorados."
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def listar_lives(
        self,
        interaction: discord.Interaction
    ):

        perfis = listar_perfis()

        if not perfis:
            mensagem = "Nenhum perfil cadastrado."
        else:
            mensagem = "\n".join(
                f"• @{perfil[0]}" for perfil in perfis
            )

        await interaction.response.send_message(
            f"**Perfis monitorados:**\n{mensagem}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Live(bot))
