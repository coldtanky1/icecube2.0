import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command()
    async def stats(self, ctx):
        user_id = ctx.author.id

        # fetch user nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            nation_name = result[0]

            # fetch user stats
            cursor.execute('SELECT name, nation_score, gdp, population, balance FROM user_stats WHERE name = ?', (nation_name,))
            stats_result = cursor.fetchone()

            if stats_result:
                name, nation_score, gdp, population, balance = stats_result

                embed = discord.Embed(
                    title=f"📊 {name}'s Stats",
                    description=f'Name: {name}',
                    color=0x04a5e5
                )
                embed.add_field(name='🫅 Ruler', value=f"<@{user_id}>", inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🏆 Nation Score', value=f'{nation_score:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='📈 Gross Domestic Product', value=f'{gdp:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='👪 Population', value=f'{population:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='💰 Balance', value=f'{balance:,}', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command()
    async def mstats(self, ctx):
        user_id = ctx.author.id

        # fetch user nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            nation_name = result[0]

            # fetch user's mil stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            if mil_result:
                name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks = mil_result

                embed = discord.Embed(
                    title=f"⚔ {name_nation}'s Military Stats",
                    description='',
                    color=0xe64553
                )
                embed.add_field(name='🪖 Troops', value=f'{troops:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='⛟ Tanks', value=f'{tanks:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='💥 Artillery', value=f'{artillery:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='💥 Anti-Air', value=f'{anti_air:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🛫 Planes', value=f'{planes:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🎖 Barracks', value=f'{barracks:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🔫 Weapon', value=f'{weapon}', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))