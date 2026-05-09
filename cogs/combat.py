import random
import discord
from discord.ext import commands
import database

RAGE_MESSAGES = [
    "RAAAAGH! EVERYTHING IN THIS SERVER IS GOING TO GET SMASHED!!",
    "My fists are BURNING! Someone better get out of my way!!",
    "I don't care who it is — COME AT ME! I'll fight ALL of you!!",
    "FULL POWER! NOBODY CAN STOP ME RIGHT NOW!",
    "My rage output is at MAXIMUM CAPACITY! INCOMING!!",
    "Shaka keeps telling me to calm down. I AM CALM. THIS IS CALM!!",
    "The ground is shaking. That's me. You're welcome.",
    "I broke three walls on my way here. The WALLS started it.",
]

SMASH_RESULTS = [
    "obliterates it with one punch. There's nothing left.",
    "punches it so hard it becomes a fine mist.",
    "kicks it through three walls and into the next server.",
    "headbutts it into the ground. The crater is 4 meters deep.",
    "grabs it with both hands and tears it clean in half.",
    "hits it so hard the sound is heard on Egghead Island.",
]

FIGHT_OUTCOMES = [
    "{winner} dominates {loser} in a brutal exchange. No contest.",
    "{winner} lands a devastating blow. {loser} is down!",
    "{winner} overwhelms {loser} with sheer force. The fight is over.",
    "{loser} puts up a fight, but {winner} is simply on another level.",
    "{winner} wins after an intense struggle. {loser} gave it everything.",
]

SIBLINGS = [
    ("Shaka", "01", "Good", "shaka"),
    ("Lilith", "02", "Evil", "lilith"),
    ("Edison", "03", "Thinker", "edison"),
    ("Pythagoras", "04", "Wisdom", "py"),
    ("Atlas", "05", "Violence", "atlas"),
    ("York", "06", "Greed", "york"),
]


class CombatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="punch")
    async def punch(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("You want to punch YOURSELF?! Even I think that's too much.")
            return
        if member.bot:
            await ctx.send("I don't punch bots. They don't even feel it. BORING.")
            return
        database.add_punch(ctx.guild.id, ctx.author.id, member.id)
        embed = discord.Embed(
            title="👊 PUNCH!",
            description=f"{ctx.author.mention} delivers a devastating punch to {member.mention}!",
            color=discord.Color.orange(),
        )
        embed.set_footer(text="Satellite 05 — Atlas (Violence)")
        await ctx.send(embed=embed)

    @commands.command(name="fight")
    async def fight(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("Fighting yourself? I respect the ambition but the answer is no.")
            return
        if member.bot:
            await ctx.send("Bots don't bleed. Pick a real opponent.")
            return
        challenger = ctx.author
        opponent = member
        winner, loser = random.choice([(challenger, opponent), (opponent, challenger)])
        database.add_fight(ctx.guild.id, challenger.id, opponent.id, winner.id)
        outcome = random.choice(FIGHT_OUTCOMES).format(
            winner=winner.display_name, loser=loser.display_name
        )
        embed = discord.Embed(
            title="⚔️ FIGHT!",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Challenger", value=challenger.mention, inline=True)
        embed.add_field(name="vs", value="⚔️", inline=True)
        embed.add_field(name="Opponent", value=opponent.mention, inline=True)
        embed.add_field(name="Result", value=outcome, inline=False)
        embed.add_field(name="Winner", value=f"🏆 {winner.mention}", inline=False)
        embed.set_footer(text="Satellite 05 — Atlas (Violence)")
        await ctx.send(embed=embed)

    @commands.command(name="score")
    async def score(self, ctx):
        fights = database.get_fight_scores(ctx.guild.id)
        punches = database.get_punch_counts(ctx.guild.id)
        embed = discord.Embed(
            title="🏆 Combat Leaderboard",
            color=discord.Color.orange(),
        )
        if fights:
            board = "\n".join(
                [f"{i+1}. <@{r[0]}> — **{r[1]} win(s)**" for i, r in enumerate(fights)]
            )
            embed.add_field(name="Most Fight Wins", value=board, inline=False)
        else:
            embed.add_field(name="Most Fight Wins", value="No fights yet.", inline=False)
        if punches:
            board = "\n".join(
                [f"{i+1}. <@{r[0]}> — **{r[1]} punch(es)**" for i, r in enumerate(punches)]
            )
            embed.add_field(name="Most Punches Thrown", value=board, inline=False)
        else:
            embed.add_field(name="Most Punches Thrown", value="No punches yet.", inline=False)
        embed.set_footer(text="Satellite 05 — Atlas (Violence)")
        await ctx.send(embed=embed)

    @commands.command(name="rage")
    async def rage(self, ctx):
        msg = random.choice(RAGE_MESSAGES)
        embed = discord.Embed(
            title="🔥 ATLAS RAGE MODE ACTIVATED",
            description=msg,
            color=discord.Color.red(),
        )
        embed.set_footer(text="Satellite 05 — Atlas (Violence) | Stand back.")
        await ctx.send(embed=embed)

    @commands.command(name="smash")
    async def smash(self, ctx, *, thing: str):
        result = random.choice(SMASH_RESULTS)
        embed = discord.Embed(
            title="💥 SMASH!",
            description=f"Atlas grabs **{thing}** and {result}",
            color=discord.Color.orange(),
        )
        embed.set_footer(text="Satellite 05 — Atlas (Violence)")
        await ctx.send(embed=embed)

    @commands.command(name="siblings")
    async def siblings(self, ctx):
        embed = discord.Embed(
            title="🤖 The Six Vegapunk Satellites",
            description="My siblings. Some of them could use a good fight.",
            color=discord.Color.orange(),
        )
        for name, number, trait, prefix in SIBLINGS:
            marker = " ← you are here" if name == "Atlas" else ""
            embed.add_field(
                name=f"Satellite {number} — {name} ({trait}){marker}",
                value=f"Prefix: `{prefix}`",
                inline=False,
            )
        await ctx.send(embed=embed)

    @punch.error
    async def punch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `atlas punch @user`")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Can't find that person. Find me a real target.")

    @fight.error
    async def fight_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `atlas fight @user`")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("That person doesn't exist. I need a real opponent.")

    @smash.error
    async def smash_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `atlas smash <thing>`")


async def setup(bot):
    await bot.add_cog(CombatCog(bot))
