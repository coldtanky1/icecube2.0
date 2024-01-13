import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Infra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def infra(self, ctx):
        user_id = ctx.author.id

        # fetch user nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            nation_name = result[0]

            # fetch user's military stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            # fetch user's infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (nation_name,))
            infra_result = cursor.fetchone()

            if infra_result and mil_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                fields = [
                    ("Housing", f"Displays {name}'s Housing."),
                    ("", ""),
                    ("Basic House", str(basic_house)),
                    ("", ""),
                    ("Small Flat", str(small_flat)),
                    ("", ""),
                    ("Apartment Complex", str(apt_complex)),
                    ("", ""),
                    ("Skyscraper", str(skyscraper)),
                    ("", ""),
                    ("Production", f"Displays {name}'s Resource Production."),
                    ("", ""),
                    ("Lumber Mill", str(lumber_mill)),
                    ("", ""),
                    ("Coal Mine", str(coal_mine)),
                    ("", ""),
                    ("Iron Mine", str(iron_mine)),
                    ("", ""),
                    ("Lead Mine", str(lead_mine)),
                    ("", ""),
                    ("Bauxite Mine", str(bauxite_mine)),
                    ("", ""),
                    ("Oil Derrick", str(oil_derrick)),
                    ("", ""),
                    ("Uranium Mine", str(uranium_mine)),
                    ("", ""),
                    ("Farm", str(farm)),
                    ("", ""),
                    ("Aluminium Factory", str(aluminium_factory)),
                    ("", ""),
                    ("Steel Factory", str(steel_factory)),
                    ("", ""),
                    ("Oil Refinery", str(oil_refinery)),
                    ("", ""),
                    ("Munitions Factory", str(ammo_factory)),
                    ("", ""),
                    ("Concrete Factory", str(concrete_factory)),
                    ("", ""),
                    ("Military", f'Displays {name}\'s Military Production.'),
                    ("", ""),
                    ("Military Factory", str(militaryfactory)),
                    ("", ""),
                    ("Tank Factory", str(tank_factory)),
                    ("", ""),
                    ("Plane Factory", str(plane_factory)),
                    ("", ""),
                    ("Artillery Factory", str(artillery_factory)),
                    ("", ""),
                    ("Anti-Air Factory", str(anti_air_factory)),
                ]

                # paginate (if that's a word) the fields
                pages = []
                current_page = 0
                fields_per_page = 10

                while current_page < len(fields):
                    embed = discord.Embed(title=f"{name}'s Infrastructure", color=0x8839ef)

                    for field_name, field_value in fields[current_page:current_page + fields_per_page]:
                        embed.add_field(name=field_name, value=field_value, inline=False)

                    pages.append(embed)
                    current_page += fields_per_page

                # Send the first page and add reactions for navigation
                message = await ctx.send(embed=pages[0])
                await message.add_reaction('⬅️')
                await message.add_reaction('➡️')

                def check(react, usr):
                    return usr == ctx.author and str(react.emoji) in ['⬅️', '➡️']

                current_page = 0

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except TimeoutError:
                        break

                    if str(reaction.emoji) == '➡️' and current_page + 1 < len(pages):
                        current_page += 1
                    elif str(reaction.emoji) == '⬅️' and current_page > 0:
                        current_page -= 1

                    await message.edit(embed=pages[current_page])
                    await message.remove_reaction(reaction.emoji, user)
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
    await bot.add_cog(Infra(bot))