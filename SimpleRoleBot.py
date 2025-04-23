import discord
from discord.ext import commands
import traceback
import time

# Set up intents for the bot
intents = discord.Intents.default()
intents.members = True  # Required to access the member list
intents.message_content = True  # Required to detect commands
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def giveverified(ctx):
    """Admin command to give the verified role to all members with the specified role"""
    print(f"\n--- Command !giveverified executed by {ctx.author} ---")
    
    # Only allow admins or specific roles to use this command
    if not ctx.author.guild_permissions.administrator:
        print(f"Permission denied: {ctx.author} doesn't have administrator permissions")
        return
    
    # Define the role IDs
    # The existing role the user has
    required_role_id = 495538893626802190
    # The new role the user will be given
    verified_role_id = 1330278651836497950
    
    # Get the role objects
    required_role = ctx.guild.get_role(required_role_id)
    verified_role = ctx.guild.get_role(verified_role_id)
    
    print(f"Looking for required role (ID: {required_role_id}): {'Found' if required_role else 'NOT FOUND'}")
    print(f"Looking for verified role (ID: {verified_role_id}): {'Found' if verified_role else 'NOT FOUND'}")
    
    if not required_role or not verified_role:
        print("One or both roles not found. Please check the role IDs.")
        return
    
    # Track stats
    count_added = 0
    count_already_had = 0
    errors = 0
    
    # Get total number of members with the required role
    total_members = len(required_role.members)
    print(f"Found {total_members} members with the role '{required_role.name}'")
    
    start_time = time.time()
    
    # Loop through all members with the required role
    for i, member in enumerate(required_role.members, 1):
        try:
            if verified_role not in member.roles:
                await member.add_roles(verified_role)
                count_added += 1
                print(f"[{i}/{total_members}] Added role to {member.name}#{member.discriminator} ({member.id})")
            else:
                count_already_had += 1
                print(f"[{i}/{total_members}] {member.name}#{member.discriminator} already has the role")
            
            # Sleep briefly to respect rate limits
            if i % 5 == 0:
                time.sleep(0.5)
                
        except discord.Forbidden:
            errors += 1
            print(f"[{i}/{total_members}] ERROR: No permission to add role to {member.name}#{member.discriminator}")
        except Exception as e:
            errors += 1
            print(f"[{i}/{total_members}] ERROR with {member.name}#{member.discriminator}: {str(e)}")
            traceback.print_exc()
    
    elapsed_time = time.time() - start_time
    print(f"\n--- SUMMARY ---")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Added '{verified_role.name}' role to {count_added} members")
    print(f"{count_already_had} members already had the role")
    print(f"{errors} errors occurred")
    print(f"--- End of !giveverified execution ---\n")

@bot.event
async def on_ready():
    print(f"\n--- Bot is online ---")
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} servers")
    print("Bot is ready to receive commands!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Command error: {str(error)}")
    traceback.print_exc()

# Run the bot
bot.run('DISCORD BOT TOKEN GOES HERE')
