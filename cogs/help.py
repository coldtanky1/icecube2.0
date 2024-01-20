import discord
from discord.ext import commands
from discord.utils import get


new_line = '\n'

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')


    @commands.command()
    async def help(self, ctx, cmd: str = ''):
        cmd = cmd.lower()

        match cmd:   # Description and syntax of each command
            case "create":
                embed = discord.Embed(colour=0xdd7878, title="Help: Create", type='rich',
                                      description=f'Syntax: `$create`{new_line}{new_line}'
                                                  f'Creates a new nation if you don\'t have one already')
                await ctx.send(embed=embed)
            case "private":
                embed = discord.Embed(colour=0xdd7878, title="Help: Private", type='rich',
                                      description=f'Syntax: `$private`{new_line}{new_line}'
                                                  f'Creates a private channel that will be deleted after 1 hour.')
                await ctx.send(embed=embed)
            case "infra":
                embed = discord.Embed(colour=0xdd7878, title="Help: Infra", type='rich',
                                      description=f'Syntax: `$infra`{new_line}{new_line}'
                                                  f'Displays your infrastructure.')
                await ctx.send(embed=embed)
            case "mstats":
                embed = discord.Embed(colour=0xdd7878, title="Help: Mstats", type='rich',
                                      description=f'Syntax: `$mstats`{new_line}{new_line}'
                                                  f'Displays your military statistics.')
                await ctx.send(embed=embed)
            case "rename":
                embed = discord.Embed(colour=0xdd7878, title="Help: Rename", type='rich',
                                      description=f'Syntax: `$rename [new name]`{new_line}{new_line}'
                                                  f'Changes the name of your nation to the [new name].{new_line}'
                                                  f'Mind that the name cannot be longer than 25 characters.')
                await ctx.send(embed=embed)

            case "stats":
                embed = discord.Embed(colour=0xdd7878, title="Help: Stats", type='rich',
                                      description=f'Syntax: `$stats`{new_line}{new_line}'
                                                  f'Displays your nation\'s statistics.')
                await ctx.send(embed=embed)

            case "res":
                embed = discord.Embed(colour=0xdd7878, title="Help: Resource", type='rich',
                                      description=f'Syntax: `$res`{new_line}{new_line}'
                                                  f'Displays your nation\'s production.')
                await ctx.send(embed=embed)

            case "reserve":
                embed = discord.Embed(colour=0xdd7878, title="Help: Reserve", type='rich',
                                      description=f'Syntax: `$reserve`{new_line}{new_line}'
                                                  f'Displays your nation\'s national reserves.')
                await ctx.send(embed=embed)

            case "update":
                embed = discord.Embed(colour=0xdd7878, title="Help: Update", type='rich',
                                      description=f'Syntax: `$update`{new_line}{new_line}'
                                                  f'Updates your nation\'s statistics.')
                await ctx.send(embed=embed)

            case "recruit":
                embed = discord.Embed(colour=0xdd7878, title="Help: Recruit", type='rich',
                                      description=f'Syntax: `$recruit <amount>`{new_line}{new_line}'
                                                  f'Recruit soldiers into your military.')
                await ctx.send(embed=embed)

            case "construct":
                embed = discord.Embed(colour=0xdd7878, title="Help: Construct", type='rich',
                                      description=f'Syntax: `$construct <building> <amount>`{new_line}{new_line}'
                                                  f'Construct buildings in your nation.')
                await ctx.send(embed=embed)

            case "allocate":
                embed = discord.Embed(colour=0xdd7878, title="Help: Allocate", type='rich',
                                      description=f'Syntax: `$allocate <mil_equip> <amount>`{new_line}{new_line}'
                                                  f'Allocate military factories to military equipment.')
                await ctx.send(embed=embed)

            case "deallocate":
                embed = discord.Embed(colour=0xdd7878, title="Help: Deallocate", type='rich',
                                      description=f'Syntax: `$deallocate <mil_equip> <amount>`{new_line}{new_line}'
                                                  f'Deallocate military factories from military equipment.')
                await ctx.send(embed=embed)

            case "trade":
                embed = discord.Embed(colour=0xdd7878, title="Help: Trade", type='rich',
                                      description=f'Syntax: `$trade <target_nation> <material> <amount>`{new_line}{new_line}'
                                                  f'Trade resources with other nations.')
                await ctx.send(embed=embed)

            case _:   # Actual command list
                generating = discord.Embed(colour=0xdce0e8, title="Help", type='rich',
                                           description="Generating help pages...")

                gen_emb = discord.Embed(colour=0xea76cb, title="Help | General", type='rich')   # General Tab
                gen_emb.add_field(name="Statistic Visualization", value="Stats - Displays your stats.\n"
                                                                        "Mstats - Displays your military stats.\n"
                                                                        "Infra - Displays your infrastructure.\n"
                                                                        "Update - Updates your nation's statistics.",
                                  inline=False)
                gen_emb.add_field(name="Other Features", value="Private - Creates a private channel.\n"
                                                               "Create - Creates a nation.",
                                  inline=False)

                eco_emb = discord.Embed(colour=0xdf8e1d, title="Help | Economy", type='rich')   # Economy Tab
                eco_emb.add_field(name="Economy", value="Res - Displays your nation's production.\n"
                                                        "Reserve - Displays your nation's national reserves.\n"
                                                        "Trade - Trade resources with other nations.",
                                  inline=False)

                tec_emb = discord.Embed(colour=0x04a5e5, title="Help | Technology", type='rich')   # Technology Tab
                tec_emb.add_field(name="Category", value="Command - Description",
                                  inline=False)

                cus_emb = discord.Embed(colour=0x7287fd, title="Help | Customization", type='rich')   # Customization Tab
                cus_emb.add_field(name="Name Changing", value="Rename - Changes your name to something else.",
                                  inline=False)

                set_emb = discord.Embed(colour=0x7c7f93, title="Help | Settings", type='rich')   # Settings Tab
                set_emb.add_field(name="Category", value="Command - Description",
                                  inline=False)

                mil_emb = discord.Embed(colour=0xe64553, title="Help | Military", type='rich')   # Military Tab
                mil_emb.add_field(name="Ground Forces", value="Recruit - Recruit soldiers into your military.",
                                  inline=False)
                mil_emb.add_field(name="War Economy", value="Allocate - Allocate military factories to military equipment.\n"
                                                            "Deallocate - Deallocate military factories from military equipment.",
                                  inline=False)

                pol_emb = discord.Embed(colour=0x8839ef, title="Help | Politics", type='rich')   # Politics Tab
                pol_emb.add_field(name="Category", value="Command - Description",
                                  inline=False)

                adm_emb = discord.Embed(colour=0x40a02b, title="Help | Administration", type='rich')   # Administration Tab
                adm_emb.add_field(name="Construction", value="Construct - Construct buildings in your nation.",
                                  inline=False)

                help_emb = await ctx.send(embed=generating)   # Prepares Embed
                await help_emb.add_reaction('📊')
                await help_emb.add_reaction('💶')
                await help_emb.add_reaction('🧪')
                await help_emb.add_reaction('🖍️')
                await help_emb.add_reaction('🔨')
                await help_emb.add_reaction('💥')
                await help_emb.add_reaction('📜')
                await help_emb.add_reaction('✒️')
                match cmd:   # Chooses first page depending on [cmd]
                    case "eco" | "economy":
                        await help_emb.edit(embed=eco_emb)
                    case "tec" | "tech" | "technology":
                        await help_emb.edit(embed=tec_emb)
                    case "cus" | "custom" | "customization":
                        await help_emb.edit(embed=cus_emb)
                    case "set" | "settings":
                        await help_emb.edit(embed=set_emb)
                    case "mil" | "military":
                        await help_emb.edit(embed=mil_emb)
                    case "pol" | "politics" | "politic":
                        await help_emb.edit(embed=pol_emb)
                    case "adm" | "admin" | "pop" | "population" | "administration":
                        await help_emb.edit(embed=adm_emb)
                    case _:
                        await help_emb.edit(embed=gen_emb)

                def chk(rec, usr):
                    return usr == ctx.author and str(rec.emoji) in ['📊', '💶', '🧪', '🖍️', '🔨', '💥', '📜', '✒️']

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=chk)
                    except TimeoutError:
                        break
                    match(str(reaction.emoji)):   # Choosing Tab based on emoji
                        case '📊':
                            await help_emb.edit(embed=gen_emb)
                        case '💶':
                            await help_emb.edit(embed=eco_emb)
                        case '🧪':
                            await help_emb.edit(embed=tec_emb)
                        case '🖍️':
                            await help_emb.edit(embed=cus_emb)
                        case '🔨':
                            await help_emb.edit(embed=set_emb)
                        case '💥':
                            await help_emb.edit(embed=mil_emb)
                        case '📜':
                            await help_emb.edit(embed=pol_emb)
                        case '✒️':
                            await help_emb.edit(embed=adm_emb)
                        case _:
                            break
                    await help_emb.remove_reaction(reaction.emoji, user)


async def setup(bot):
    await bot.add_cog(Help(bot))