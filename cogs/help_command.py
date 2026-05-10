import discord
from discord.ext import commands

COMMANDS_DATA = {
    "🍓 Economy": {
        "atlas balance [@user]": "Check your (or another user's) berry balance.",
        "atlas daily": "Claim your daily berries. Multiplied by your York trust level.",
        "atlas pay @user <amount>": "Transfer berries to another user.",
        "atlas top": "Show the berry leaderboard for this server.",
    },
    "🤖 Satellite Info": {
        "atlas siblings": "List all six Vegapunk satellites and their roles.",
    },
    "❓ Help": {
        "atlas help": "Show this help menu.",
    },
}


class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=category, description=f"{len(cmds)} command(s)")
            for category, cmds in COMMANDS_DATA.items()
        ]
        super().__init__(placeholder="Select a command category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        cmds = COMMANDS_DATA[category]
        embed = discord.Embed(
            title=f"⚙️ Atlas — {category}",
            color=discord.Color.orange(),
        )
        for name, desc in cmds.items():
            embed.add_field(name=f"`{name}`", value=desc, inline=False)
        embed.set_footer(text="Satellite 05 — Atlas (Violence) | Economy & Utility | Prefix: atlas")
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(CategorySelect())


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["?"])
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="⚙️ ATLAS — Satellite 05 (Violence)",
            description=(
                "Hi! I'm Atlas. I handle berries and economy for the whole system.\n"
                "Claim your daily, check your balance, pay friends, and more!\n\n"
                "**Prefix:** `atlas`\n"
                "Tip: Feed York to boost your daily multiplier!"
            ),
            color=discord.Color.orange(),
        )
        embed.set_footer(text="Select a category below to view commands.")
        await ctx.send(embed=embed, view=HelpView())


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
