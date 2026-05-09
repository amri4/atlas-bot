import discord
from discord.ext import commands

COMMANDS_DATA = {
    "👊 Combat": {
        "atlas punch @user": "Punch someone. Hard. Logged in the database.",
        "atlas fight @user": "Challenge a user to a fight. A winner is decided by fate.",
        "atlas score": "Show the fight leaderboard for this server.",
        "atlas rage": "Atlas enters RAGE MODE. Unpredictable things happen.",
        "atlas smash <thing>": "Atlas smashes something into pieces.",
        "atlas siblings": "List all six Vegapunk satellites.",
    },
    "❓ Help": {
        "atlas?": "Show this help menu.",
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
            title=f"Atlas — {category}",
            color=discord.Color.orange(),
        )
        for name, desc in cmds.items():
            embed.add_field(name=f"`{name}`", value=desc, inline=False)
        embed.set_footer(text="Satellite 05 — Atlas (Violence) | Prefix: atlas")
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(CategorySelect())


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="?")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="👊 Atlas — Satellite 05 (Violence)",
            description=(
                "You want help?! Then STOP WASTING MY TIME and pick a category!\n\n"
                "**Prefix:** `atlas`"
            ),
            color=discord.Color.orange(),
        )
        embed.set_footer(text="Use the menu below to explore commands.")
        await ctx.send(embed=embed, view=HelpView())


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
