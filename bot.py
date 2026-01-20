import os
import discord
from discord.ext import commands

# ==============================
# CONFIGURAÇÃO DE INTENTS
# ==============================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# LÓGICA DE BALANCEAMENTO
# ==============================
def sortear_times(jogadores, n_times):
    jogadores_por_time = 5

    if len(jogadores) != n_times * jogadores_por_time:
        raise ValueError("Quantidade de jogadores incompatível com o número de times.")

    jogadores.sort(key=lambda x: x[1], reverse=True)

    times = [{"jogadores": [], "soma": 0} for _ in range(n_times)]

    for nome, nivel in jogadores:
        time_escolhido = min(
            (t for t in times if len(t["jogadores"]) < jogadores_por_time),
            key=lambda t: t["soma"]
        )

        time_escolhido["jogadores"].append((nome, nivel))
        time_escolhido["soma"] += nivel

    return times

# ==============================
# COMANDO !mix
# ==============================
@bot.command()
async def mix(ctx, n_times: int):
    linhas = ctx.message.content.split("\n")[1:]
    jogadores = []

    try:
        for linha in linhas:
            nome, nivel = linha.rsplit(" ", 1)
            jogadores.append((nome, int(nivel)))

        times = sortear_times(jogadores, n_times)

    except Exception as e:
        await ctx.send(f"Erro: {e}")
        return

    resposta = "**🎮 TIMES SORTEADOS (CS2 MIX)**\n"

    for i, time in enumerate(times, start=1):
        resposta += f"\n**Time {i} | Soma: {time['soma']}**\n"
        for nome, nivel in time["jogadores"]:
            resposta += f"- {nome} ({nivel})\n"

    await ctx.send(resposta)

# ==============================
# INICIAR BOT (TOKEN VIA ENV)
# ==============================
bot.run(os.getenv("DISCORD_TOKEN"))