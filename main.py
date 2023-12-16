# import discord
# from discord.ext import commands
# import mysql.connector
# import hashlib



# intents = discord.Intents.default()
# intents.message_content = True
# # Create a bot object with a command prefix
# bot = commands.Bot(command_prefix="!",intents=intents)

# # Connect to the MySQL database
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="username",
#   password="pass",
#   database="discord_bot",
#   auth_plugin='mysql_native_password',
# )

# # Create a cursor object to execute SQL queries
# mycursor = mydb.cursor()

# def generate_auth_token(server_id):
#     # Convert the server ID to bytes
#     server_id_bytes = str(server_id).encode('utf-8')

#     # Generate the SHA-256 hash of the server ID
#     sha256_hash = hashlib.sha256(server_id_bytes)

#     # Get the hexadecimal representation of the hash
#     auth_token = sha256_hash.hexdigest()

#     return auth_token


# # Define a command that prints "Hello World" and the server name
# @bot.command()
# async def hello(ctx):
#     # Get the server id from the context
#     auth_token = generate_auth_token(ctx.guild.id)
    
#     # Check if the server id is in the tokens table
#     mycursor.execute("SELECT name FROM auth WHERE token = %s", (auth_token,))
    
#     result = mycursor.fetchone()
    
#     # If the server id is not in the table, ask the user to authenticate the bot
#     if result is None:
#         await ctx.send("Please authenticate the bot by typing !auth ")
    
#     # If the server id is in the table, print "Hello World" and the server name
#     else:
#         await ctx.send(f"Hello World {ctx.guild.name}")

# # Define a command that authenticates the bot for a server
# @bot.command()
# async def auth(ctx):
#     # Get the server id and the server name from the context
#     server_name = ctx.guild.name

#     token = generate_auth_token(ctx.guild.id)
#     # Insert the server id and the token into the tokens table
#     mycursor.execute("INSERT INTO auth (name, token) VALUES (%s, %s)", (server_name, token))
#     mydb.commit()
#     # Send a confirmation message to the user
#     await ctx.send(f"The bot is authenticated for {server_name}")

# # Run the bot with the token
# bot.run("your_token")
import discord
from discord.ext import commands
import mysql.connector
import hashlib

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="username",
        password="pass",
        database="discord_bot",
        auth_plugin='mysql_native_password',
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

def generate_auth_token(server_id):
    try:
        server_id_bytes = str(server_id).encode('utf-8')
        sha256_hash = hashlib.sha256(server_id_bytes)
        auth_token = sha256_hash.hexdigest()
        return auth_token
    except Exception as e:
        print(f"Error generating auth token: {e}")

@bot.command()
async def hello(ctx):
    try:
        auth_token = generate_auth_token(ctx.guild.id)
        mycursor.execute("SELECT name FROM auth WHERE token = %s", (auth_token,))
        result = mycursor.fetchone()

        if result is None:
            await ctx.send("Please authenticate the bot by typing !auth ")
        else:
            await ctx.send(f"Hello World {ctx.guild.name}")

    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        await ctx.send("An error occurred while processing the command.")

@bot.command()
async def auth(ctx):
    try:
        server_name = ctx.guild.name
        token = generate_auth_token(ctx.guild.id)
        mycursor.execute("INSERT INTO auth (name, token) VALUES (%s, %s)", (server_name, token))
        mydb.commit()
        await ctx.send(f"The bot is authenticated for {server_name}")

    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        await ctx.send("An error occurred while processing the command.")

# Run the bot with the token
bot.run("your_token")
