import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import shared_db

load_dotenv()
shared_db.init_db()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=["atlas ", "atlas", "Atlas ", "Atlas"],
    intents=intents,
    help_command=None,
)

EXTENSIONS = [
    "cogs.help_command",
    "cogs.economy",
]


async def setup_hook():
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"[ATLAS] Loaded {ext}")
        except Exception as e:
            print(f"[ATLAS] Failed to load {ext}: {e}")

bot.setup_hook = setup_hook


@bot.event
async def on_ready():
    print(f"[ATLAS] Online as {bot.user} | Satellite 05 — Violence (Economy & Utility)")
    print(f"[ATLAS] DB path: {shared_db.get_db_path()}")
    print(f"[ATLAS] Guilds: {len(bot.guilds)}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: `{error.param.name}`. Use `atlas help` for usage.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found. Mention them directly.")
    else:
        print(f"[ATLAS] Error in {ctx.command}: {error}")


bot.run(os.getenv("DISCORD_TOKEN"))
