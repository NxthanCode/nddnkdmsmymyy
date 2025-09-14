import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import os
import sqlite3

w_channel = 1416518050911490060
log_channel_id = 1416526620935589958
autorole = 987654321098765432

intents = discord.Intents.all()
devs = "Made by n4tk_ & 141at on discord"

bot = commands.Bot(command_prefix="/", intents=intents)


def init_db():
    conn = sqlite3.connect('bot_settings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS server_settings
                 (guild_id INTEGER PRIMARY KEY, welcome_channel INTEGER, autorole INTEGER, log_channel INTEGER)''')
    conn.commit()
    conn.close()

def get_setting(guild_id, setting):
    conn = sqlite3.connect('bot_settings.db')
    c = conn.cursor()
    c.execute(f"SELECT {setting} FROM server_settings WHERE guild_id = ?", (guild_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def set_setting(guild_id, setting, value):
    conn = sqlite3.connect('bot_settings.db')
    c = conn.cursor()
    c.execute("SELECT guild_id FROM server_settings WHERE guild_id = ?", (guild_id,))
    if c.fetchone():
        c.execute(f"UPDATE server_settings SET {setting} = ? WHERE guild_id = ?", (value, guild_id))
    else:
        c.execute(f"INSERT INTO server_settings (guild_id, {setting}) VALUES (?, ?)", (guild_id, value))
    conn.commit()
    conn.close()

def remove_setting(guild_id, setting):
    conn = sqlite3.connect('bot_settings.db')
    c = conn.cursor()
    c.execute(f"UPDATE server_settings SET {setting} = NULL WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()

async def log_action(guild, action, details, color=0xffffff, target=None, moderator=None, transcript=None, thumbnail=None):
    custom_log_channel_id = get_setting(guild.id, 'log_channel')
    channel_id = custom_log_channel_id if custom_log_channel_id else log_channel_id
    channel = bot.get_channel(channel_id)
    
    if not channel:
        return
        
    embed = discord.Embed(title=f"Action: {action}", color=color, timestamp=datetime.now(timezone.utc))
    for key, value in details.items():
        embed.add_field(name=key, value=value, inline=False)
    if target and not thumbnail:
        thumbnail = target.display_avatar.url
    if moderator and not thumbnail:
        thumbnail = moderator.display_avatar.url
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=f"{devs}")
    if transcript:
        await channel.send(file=discord.File(transcript))
        os.remove(transcript)
    await channel.send(embed=embed)

@bot.tree.command(name="setlogchannel", description="Set the log channel for this server")
@app_commands.describe(channel="Channel for logging actions")
async def setlogchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    
    set_setting(interaction.guild.id, 'log_channel', channel.id)
    
    embed = discord.Embed(title=f"Log channel set to {channel.name}", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
    await interaction.response.send_message(embed=embed)
    
    await log_action(interaction.guild, "Log Channel Set", {"Channel": channel.mention}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="removelogchannel", description="Remove the custom log channel")
async def removelogchannel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    
    remove_setting(interaction.guild.id, 'log_channel')
    
    embed = discord.Embed(title="Log channel removed", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
    await interaction.response.send_message(embed=embed)
    
    await log_action(interaction.guild, "Log Channel Removed", {}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="setwelcome", description="Set the welcome channel")
@app_commands.describe(channel="Channel for welcome messages")
async def setwelcome(interaction: discord.Interaction, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    
    set_setting(interaction.guild.id, 'welcome_channel', channel.id)
    
    embed = discord.Embed(title=f"Welcome channel set to {channel.name}", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
    await interaction.response.send_message(embed=embed)
    
    await log_action(interaction.guild, "Welcome Channel Set", {"Channel": channel.mention}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="removewelcome", description="Remove the welcome channel")
async def removewelcome(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    
    remove_setting(interaction.guild.id, 'welcome_channel')
    
    embed = discord.Embed(title="Welcome channel removed", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
    await interaction.response.send_message(embed=embed)
    
    await log_action(interaction.guild, "Welcome Channel Removed", {}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="setautorole", description="Set the auto role for new members")
@app_commands.describe(role="Role to assign automatically")
async def setautorole(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    
    set_setting(interaction.guild.id, 'autorole', role.id)
    
    embed = discord.Embed(title=f"Auto role set to {role.name}", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
    await interaction.response.send_message(embed=embed)
    
    await log_action(interaction.guild, "Auto Role Set", {"Role": role.name}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="removeautorole", description="Remove the auto role")
async def removeautorole(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    
    remove_setting(interaction.guild.id, 'autorole')
    
    embed = discord.Embed(title="Auto role removed", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
    await interaction.response.send_message(embed=embed)
    
    await log_action(interaction.guild, "Auto Role Removed", {}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="clear", description="Clear messages from this channel")
@app_commands.describe(amount="Number of messages to clear (optional)")
async def clear(interaction: discord.Interaction, amount: int = None):
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("You need Manage Messages permission.", ephemeral=True)
    if not interaction.channel.permissions_for(interaction.guild.me).manage_messages:
        return await interaction.response.send_message("I don't have permission to manage messages here.", ephemeral=True)
    deleted = []
    async for msg in interaction.channel.history(limit=None if not amount else amount):
        deleted.append(msg)
    for msg in deleted:
        await msg.delete()
    await interaction.response.send_message(f"Done clearing {len(deleted)} messages.", ephemeral=True)
    await log_action(interaction.guild, "Messages Cleared", {"Amount": len(deleted), "Channel": interaction.channel.mention}, 0xffffff, moderator=interaction.user, thumbnail=interaction.user.display_avatar.url)

@bot.tree.command(name="clearuser", description="Clear messages from a specific user")
@app_commands.describe(user="User to clear messages from", amount="Number of messages to clear (optional)")
async def clearuser(interaction: discord.Interaction, user: discord.Member, amount: int = None):
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("You need Manage Messages permission.", ephemeral=True)
    deleted = []
    async for msg in interaction.channel.history(limit=None):
        if msg.author == user:
            deleted.append(msg)
            if amount and len(deleted) >= amount:
                break
    for msg in deleted:
        await msg.delete()
    await interaction.response.send_message(f"Done clearing {len(deleted)} messages from {user.mention}.", ephemeral=True)
    await log_action(interaction.guild, "User Messages Cleared", {"Amount": len(deleted), "Channel": interaction.channel.mention}, 0xffffff, moderator=interaction.user, thumbnail=user.display_avatar.url)

@bot.tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="Member to kick", reason="Reason for kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(title=f"{member} kicked", description=f"Reason: {reason}", color=0xffffff)
        embed.set_footer(text=f"{devs}")
        embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, "Kick", {"Reason": reason, "User ID": member.id}, 0xffffff, target=member, moderator=interaction.user, thumbnail=member.display_avatar.url)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to kick this member.", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="Member to ban", reason="Reason for ban")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    try:
        await member.ban(reason=reason)
        embed = discord.Embd(title=f"{member} banned", description=f"Reason: {reason}", color=0xffffff)
        embed.set_footer(text=f"{devs}")
        embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, "Ban", {"Reason": reason, "User ID": member.id}, 0xffffff, target=member, moderator=interaction.user, thumbnail=member.display_avatar.url)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to ban this member.", ephemeral=True)

@bot.tree.command(name="unban", description="Unban a user")
@app_commands.describe(user="User ID or Name to unban")
async def unban(interaction: discord.Interaction, user: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("You need Admin perms.", ephemeral=True)
    bans = await interaction.guild.bans()
    user_obj = None
    if user.isdigit():
        for b in bans:
            if b.user.id == int(user):
                user_obj = b.user
                break
    else:
        for b in bans:
            if str(b.user) == user or b.user.name == user:
                user_obj = b.user
                break
    if not user_obj:
        return await interaction.response.send_message("User not found in ban list.", ephemeral=True)
    await interaction.guild.unban(user_obj)
    embed = discord.Embed(title=f"{user_obj} unbanned", color=0xffffff)
    embed.set_footer(text=f"{devs}")
    embed.set_thumbnail(url=user_obj.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    await log_action(interaction.guild, "Unban", {"User ID": user_obj.id}, 0xffffff, target=user_obj, moderator=interaction.user, thumbnail=user_obj.display_avatar.url)

class TicketAddUser(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Add User", style=discord.ButtonStyle.green, custom_id="ticket_add_user")

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Only admins can manage tickets.", ephemeral=True)
        
        await interaction.response.send_message("Please enter the username or user ID you want to add to this ticket.", ephemeral=True)
        
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            user_input = msg.content.strip()
            
            user = None
            if user_input.isdigit():
                user = interaction.guild.get_member(int(user_input))
            else:
                user = discord.utils.get(interaction.guild.members, name=user_input)
            
            if not user:
                await interaction.followup.send("User not found.", ephemeral=True)
                await msg.delete()
                return
                
            await interaction.channel.set_permissions(user, view_channel=True, send_messages=True)
            await interaction.followup.send(f"Added {user.mention} to the ticket.", ephemeral=True)
            await msg.delete()
            
        except TimeoutError:
            await interaction.followup.send("Timed out waiting for user input.", ephemeral=True)

class TicketRemoveUser(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Remove User", style=discord.ButtonStyle.red, custom_id="ticket_remove_user")

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Only admins can manage tickets.", ephemeral=True)
        
        await interaction.response.send_message("Please enter the username or user ID you want to remove from this ticket.", ephemeral=True)
        
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            user_input = msg.content.strip()
            
            user = None
            if user_input.isdigit():
                user = interaction.guild.get_member(int(user_input))
            else:
                user = discord.utils.get(interaction.guild.members, name=user_input)
            
            if not user:
                await interaction.followup.send("User not found.", ephemeral=True)
                await msg.delete()
                return
                
            await interaction.channel.set_permissions(user, overwrite=None)
            await interaction.followup.send(f"Removed {user.mention} from the ticket.", ephemeral=True)
            await msg.delete()
            
        except TimeoutError:
            await interaction.followup.send("Timed out waiting for user input.", ephemeral=True)

class TicketClose(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="ticket_close")

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Only admins can close tickets.", ephemeral=True)

        channel = interaction.channel
        transcript_text = ""
        async for msg in channel.history(limit=None, oldest_first=True):
            transcript_text += f"[{msg.created_at}] {msg.author}: {msg.content}\n"

        filename = f"{channel.name}_transcript.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        await log_action(
            interaction.guild,
            "Ticket Closed",
            {"Ticket": channel.name},
            0xffffff,
            moderator=interaction.user,
            transcript=filename,
            thumbnail=interaction.user.display_avatar.url
        )
                
        await interaction.response.send_message(f"Ticket closed by {interaction.user}.")
        await channel.delete()

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketClose())
        self.add_item(TicketAddUser())
        self.add_item(TicketRemoveUser())

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Support"),
            discord.SelectOption(label="Error"),
            discord.SelectOption(label="Other")
        ]
        super().__init__(placeholder="Select ticket type", min_values=1, max_values=1, options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        ticket_name = f"DANGERX-TICKET-{user.id}"

        existing = discord.utils.get(guild.text_channels, name=ticket_name.lower())
        if existing:
            return await interaction.response.send_message(f"You already have a ticket: {existing.mention}", ephemeral=True)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        for admin in guild.members:
            if admin.guild_permissions.administrator:
                overwrites[admin] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
        
        embed = discord.Embed(
            title=f"{self.values[0]} Ticket",
            description=f"{user.mention} created a ticket.",
            color=0xffffff,
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_footer(text=devs)
        embed.set_thumbnail(url=user.display_avatar.url)

        await channel.send(embed=embed, view=TicketCloseView())
        await log_action(guild, "Ticket Created", {"Ticket": ticket_name}, 0xffffff, moderator=user, thumbnail=user.display_avatar.url)
        await interaction.response.send_message(f"Your ticket has been created: {channel.mention}", ephemeral=True)

class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.tree.command(name="ticket", description="Post the ticket dropdown")
async def ticket(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admins can use this command.", ephemeral=True)

    embed = discord.Embed(
        title="DangerX Tickets",
        description="Select a ticket type from the dropdown below to create a support ticket.",
        color=0xffffff,
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_footer(text=devs)
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")

    await interaction.response.send_message(embed=embed, view=TicketSelectView(), ephemeral=False)

MODERATION_COMMANDS = {
    "ban": "Bans a user from the server.",
    "unban": "Unbans a user from the server.",
    "kick": "Kicks a user from the server.",
    "clear": "Clears a number of messages in a channel.",
    "clearuser": "Clears all messages from a specific user."
}

CONFIG_COMMANDS = {
    "setwelcome": "Sets the welcome message channel.",
    "removewelcome": "Removes the welcome message channel.",
    "setautorole": "Sets the autorole for new members.",
    "removeautorole": "Removes the autorole from new members.",
    "setlogchannel": "Sets the channel for logs.",
    "removelogchannel": "Removes the log channel."
}

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Moderation", description="Shows moderation commands"),
            discord.SelectOption(label="Config", description="Shows configuration commands")
        ]
        super().__init__(placeholder="Choose a category!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Moderation":
            embed = discord.Embed(
                title="Moderation Commands",
                description="List of moderation commands with descriptions:",
                color=0xffffff,
                timestamp=datetime.now(timezone.utc)
            )
            for cmd, desc in MODERATION_COMMANDS.items():
                embed.add_field(name=f"`{cmd}`", value=desc, inline=False)
            embed.set_footer(text=devs)
        elif self.values[0] == "Config":
            embed = discord.Embed(
                title="Configuration Commands",
                description="List of configuration commands with descriptions:",
                color=0xffffff,
                timestamp=datetime.now(timezone.utc)
            )
            for cmd, desc in CONFIG_COMMANDS.items():
                embed.add_field(name=f"`{cmd}`", value=desc, inline=False)
            embed.set_footer(text=devs)
        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpSelect())

@bot.tree.command(name="help", description="Show the help menu with command details")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="DangerX Help",
        description="Select a category from the dropdown.",
        color=0xffffff,
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_footer(text=devs)
    embed.set_thumbnail(url="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")

    await interaction.response.send_message(embed=embed, view=HelpSelectView(), ephemeral=False)


@bot.event
async def on_member_join(member: discord.Member):
    auto_role_id = get_setting(member.guild.id, 'autorole')
    if auto_role_id:
        role = member.guild.get_role(auto_role_id)
        if role:
            await member.add_roles(role)
            await log_action(member.guild, "Auto Role Assigned", {"Role": role.name, "Role ID": role.id}, 0xffffff, target=member, thumbnail=member.display_avatar.url)

    welcome_channel_id = get_setting(member.guild.id, 'welcome_channel')
    channel = bot.get_channel(welcome_channel_id) if welcome_channel_id else bot.get_channel(w_channel)
    
    if channel:
        embed = discord.Embed(title=f"{member} joined {member.guild}", color=0xffffff, timestamp=datetime.now(timezone.utc))
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Joined server", value=discord.utils.format_dt(member.joined_at, style="F"), inline=True)
        embed.add_field(name="Account created", value=discord.utils.format_dt(member.created_at, style="F"), inline=True)
        embed.set_footer(text=f"{devs}")
        await channel.send(embed=embed)

    await log_action(member.guild, "Member Joined", {"Account Created": discord.utils.format_dt(member.created_at, style="R")}, 0xffffff, target=member, thumbnail=member.display_avatar.url)

@bot.event
async def on_member_remove(member: discord.Member):
    log_details = {
        "Joined": discord.utils.format_dt(member.joined_at, style="R") if member.joined_at else "Unknown",
        "Roles": ", ".join([r.name for r in member.roles if r.name != "@everyone"]) or "None"
    }
    await log_action(member.guild, "Member Left", log_details, 0xffffff, target=member, thumbnail=member.display_avatar.url)

@bot.event
async def on_message_delete(message):
    if not message.guild or message.author.bot:
        return
    if getattr(message, "bulk", False):
        return
    content = message.content or "No text content"
    log_details = {
        "Channel": message.channel.mention,
        "Content": content[:1020] + "..." if len(content) > 1020 else content
    }
    await log_action(message.guild, "Message Deleted", log_details, 0xffffff, target=message.author, thumbnail=message.author.display_avatar.url)

@bot.event
async def on_message_edit(before, after):
    if not after.guild or after.author.bot:
        return
    if before.content == after.content:
        return
    log_details = {
        "Channel": after.channel.mention,
        "Before": before.content[:500] + "..." if before.content else "No text content",
        "After": after.content[:500] + "..." if after.content else "No text content"
    }
    await log_action(after.guild, "Message Edited", log_details, 0xffffff, target=after.author, thumbnail=after.author.display_avatar.url)

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        added_roles = [r for r in after.roles if r not in before.roles]
        removed_roles = [r for r in before.roles if r not in after.roles]
        if added_roles or removed_roles:
            log_details = {}
            if added_roles:
                log_details["Roles Added"] = ", ".join([r.name for r in added_roles])
            if removed_roles:
                log_details["Roles Removed"] = ", ".join([r.name for r in removed_roles])
            await log_action(after.guild, "Member Roles Updated", log_details, 0xffffff, target=after, thumbnail=after.display_avatar.url)

@bot.event
async def on_ready():
    init_db()  
    await bot.tree.sync()
    bot.add_view(TicketCloseView())
    activity = discord.Activity(type=discord.ActivityType.watching, name="DangerX Moderation")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f"Connected as {bot.user}")
    for guild in bot.guilds:
        log_details = {"Bot Version": "1.0", "Server Count": len(bot.guilds), "Member Count": guild.member_count}
        await log_action(guild, "Bot Started", log_details, 0xffffff, thumbnail="https://ik.imagekit.io/asw34adc3/ChatGPT%20Image%2010.%20Sept.%202025,%2022_04_07.png?updatedAt=1757622148378")

bot.run("")
