import discord
from discord.ext import commands
from datetime import date
import shared_db

DAILY_BASE = 150


class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        berries, trust, _ = shared_db.get_user(target.id, ctx.guild.id)
        level, label, multiplier = shared_db.get_trust_level(trust)
        embed = discord.Embed(
            title=f"⚙️ Atlas — Balance",
            color=discord.Color.orange(),
        )
        embed.set_author(name=target.display_name, icon_url=target.display_avatar.url)
        embed.add_field(name="🍓 Berries", value=f"**{berries:,}**", inline=True)
        embed.add_field(name="💜 York Trust Lv.", value=f"**{label}** (Lv.{level})", inline=True)
        embed.add_field(name="Daily Multiplier", value=f"×{multiplier}", inline=True)
        embed.set_footer(text="Satellite 05 — Atlas | Economy Unit")
        await ctx.send(embed=embed)

    @commands.command(name="daily")
    async def daily(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        berries, trust, last_daily = shared_db.get_user(user_id, guild_id)
        today = str(date.today())

        if last_daily == today:
            embed = discord.Embed(
                title="⚙️ Daily — Already Claimed",
                description="You already claimed your daily berries today. Come back tomorrow!",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        level, label, multiplier = shared_db.get_trust_level(trust)
        reward = int(DAILY_BASE * multiplier)
        shared_db.add_berries(user_id, guild_id, reward, reason="Daily reward")
        shared_db.set_last_daily(user_id, guild_id, today)

        embed = discord.Embed(
            title="⚙️ Daily Reward Claimed!",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Berries Received", value=f"**{reward:,}** 🍓", inline=True)
        embed.add_field(name="Base", value=f"{DAILY_BASE}", inline=True)
        embed.add_field(name="York Multiplier", value=f"×{multiplier} ({label})", inline=True)
        embed.add_field(name="New Balance", value=f"**{berries + reward:,}** 🍓", inline=False)
        embed.set_footer(text="Satellite 05 — Atlas | Tip: Feed York to increase your multiplier!")
        await ctx.send(embed=embed)

    @commands.command(name="pay")
    async def pay(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return
        if member.id == ctx.author.id:
            await ctx.send("You can't pay yourself.")
            return
        if member.bot:
            await ctx.send("You can't pay a bot.")
            return
        success = shared_db.transfer_berries(
            ctx.author.id, member.id, ctx.guild.id, amount, reason=f"Transfer from {ctx.author.display_name}"
        )
        if not success:
            await ctx.send(f"You don't have enough berries. Your balance: **{shared_db.get_berries(ctx.author.id, ctx.guild.id):,}** 🍓")
            return
        embed = discord.Embed(
            title="⚙️ Transfer Complete",
            color=discord.Color.orange(),
        )
        embed.add_field(name="From", value=ctx.author.mention, inline=True)
        embed.add_field(name="To", value=member.mention, inline=True)
        embed.add_field(name="Amount", value=f"**{amount:,}** 🍓", inline=True)
        embed.set_footer(text="Satellite 05 — Atlas | Economy Unit")
        await ctx.send(embed=embed)

    @commands.command(name="top")
    async def top(self, ctx):
        rows = shared_db.get_leaderboard(ctx.guild.id, by="berries")
        embed = discord.Embed(
            title="⚙️ Atlas — Berry Leaderboard",
            color=discord.Color.orange(),
        )
        if not rows:
            embed.description = "No data yet. Claim your daily with `atlas daily`!"
        else:
            medals = ["🥇", "🥈", "🥉"]
            lines = []
            for i, (uid, berries, trust) in enumerate(rows):
                medal = medals[i] if i < 3 else f"`{i+1}.`"
                lines.append(f"{medal} <@{uid}> — **{berries:,}** 🍓")
            embed.description = "\n".join(lines)
        embed.set_footer(text="Satellite 05 — Atlas | Economy Unit")
        await ctx.send(embed=embed)

    @commands.command(name="siblings")
    async def siblings(self, ctx):
        embed = discord.Embed(
            title="🤖 The Six Vegapunk Satellites",
            description="Hi! I'm Atlas. Here's the whole team:",
            color=discord.Color.orange(),
        )
        data = [
            ("Shaka", "01", "Central Brain / Database", "shaka"),
            ("Lilith", "02", "Moderation", "lilith"),
            ("Edison", "03", "Analysis & Strategy", "edison"),
            ("Pythagoras", "04", "Knowledge & Trivia", "py"),
            ("Atlas", "05", "Economy & Utility", "atlas"),
            ("York", "06", "Hunger & Trust", "york"),
        ]
        for name, num, role, prefix in data:
            marker = " ← you are here" if name == "Atlas" else ""
            embed.add_field(name=f"Satellite {num} — {name}{marker}", value=f"Role: {role} | Prefix: `{prefix}`", inline=False)
        await ctx.send(embed=embed)

    @pay.error
    async def pay_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `atlas pay @user <amount>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid arguments. Usage: `atlas pay @user <amount>`")

    @balance.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("User not found.")


async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
