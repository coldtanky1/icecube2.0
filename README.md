# Ice Cube 2.0
the ice cube revolution is here, from google spreadsheets to all new discord bots!

# Requirements
- python3
- discord.py (duh)
- pysqlite3
- asyncio

# Installation
- discord.py
- `pip install discord.py`

- pysqlite3
- `pip install pysqlite3`

- asyncio
- `pip install asyncio`


# Changelog VER 01
- Added new SQL table for resources.
- Added "res" command to display resource production.
- Added "res" command to help menu.

# Changelog VER 02
- Added "update" command to update your nation.
- Added "reserve" command to view your nation's reserves.
- Added "update" and "reserve" commands to the help menu.
- Added "construct" command but it isn't complete.

# Changelog VER 03
- Completed the "construct" command.
- If you have 0 or negative resources, you won't be able to produce.
- Added "recruit" command to recruit soldiers into your military.
- Added "construct" and "recruit" commands into the help menu.
- Updated "user_stats" table to include balance (idk why i didnt do this to begin with).
- Added command cooldown to "update".

# Changelog VER 04
- Added cogs, code is now much easier to read.
- Added "allocate" command to allocate military factories for military equipment.
- Added "barracks" and "militaryfactory" to construct command.
- Added "deallocate" command to deallocate military factories for military equipment.
- Updated the "update" command to update production of military equipment.
- Added "allocate" and "deallocate" commands to help menu.