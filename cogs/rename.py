import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, new_name: str):
        if new_name == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You forgot to write the new name.{new_line}{new_line}'
                                              f'Command Format: `$rename [new_name]`')
            await ctx.send(embed=embed)

        user_id = ctx.author.id

        if len(new_name) > 25:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Your nation name cannot be longer than 25 characters.')
            await ctx.send(embed=embed)
            return

        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        nation_name = result[0]

        cursor.execute('SELECT 1 FROM user_info WHERE user_id = ?', (user_id,))
        existing_record = cursor.fetchone()

        if existing_record:
            # updates the user_info table
            cursor.execute('UPDATE user_info SET nation_name = ? WHERE user_id = ?', (new_name, user_id))
            conn.commit()
            # updates the user_stats table
            cursor.execute('UPDATE user_stats SET name = ? WHERE name = ?', (new_name, nation_name))
            conn.commit()
            # updates the user_mil table
            cursor.execute('UPDATE user_mil SET name_nation = ? WHERE name_nation = ?', (new_name, nation_name))
            conn.commit()
            # updates the infra table
            cursor.execute('UPDATE infra SET name = ? WHERE name = ?', (new_name, nation_name))
            conn.commit()
            # updates the resources table
            cursor.execute('UPDATE resources SET name = ? WHERE name = ?', (new_name, nation_name))
            conn.commit()

            embed = discord.Embed(
                title='Nation Rename',
                description=f'You have successfully changed your nation\'s name to **{new_name}**!',
                color=0x5BF9A0
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rename(bot))