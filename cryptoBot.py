import discord
import asyncio
from cryptography.fernet import Fernet

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    await client.change_presence(game=discord.Game(name="with Crypting Keys"))

@client.event
async def on_message(message):
    message1 = str(message.content).split(' ',1)[0].upper()
        
    if '$ENCRYPT' == message1:
        try:
            message2 = str(message.content).split(' ',1)[1]
            if message2.count("") <= 4:
                embed = discord.Embed(title=':no_entry: ERROR', description='Your message must be longer!', color= 0xf44242)
                error = await client.send_message(message.channel, embed=embed)
                await asyncio.sleep(10)
                await client.delete_message(error)
                try:
                    await client.delete_message(message)
                except:
                    pass
                return
        except:
            embed = discord.Embed(title=':no_entry: ERROR', description='Your message must be longer!', color= 0xf44242)
            error = await client.send_message(message.channel, embed=embed)
            await asyncio.sleep(10)
            await client.delete_message(error)
            try:
                await client.delete_message(message)
            except:
                pass
            return
            
        try:
            key = Fernet.generate_key()
            f = Fernet(key)
            token = f.encrypt(message2.encode())
            encryptedMessage = key.decode()+"/"+token.decode()
            embed = discord.Embed(title='Your encrypted message:', description=encryptedMessage, color= 0x4fff63)
            try:
                await client.delete_message(message)
            except:
                pass
            await client.send_message(message.author, embed=embed)
        except:
            embed = discord.Embed(title=':no_entry: ERROR', description='There was an unexpected error. Please try again!', color= 0xf44242)
            error = await client.send_message(message.channel, embed=embed)
            await asyncio.sleep(10)
            await client.delete_message(error)
            try:
                await client.delete_message(message)
            except:
                pass
            
    elif '$DECRYPT' == message1:
        try:
            message2 = str(message.content).split(' ',1)[1]
        except:
            embed = discord.Embed(title=':no_entry: ERROR', description='Your message token must be longer!', color= 0xf44242)
            error = await client.send_message(message.channel, embed=embed)
            await asyncio.sleep(10)
            await client.delete_message(error)
            try:
                await client.delete_message(message)
            except:
                pass
            return
        try:
            key = message2.split("/")[0]
            f = Fernet(key)
            token = message2.split("/")[1]
            decryptedMessage = f.decrypt(token.encode())
            embed = discord.Embed(title='Your decrypted message:', description=decryptedMessage.decode(), color= 0x4fff63)
            try:
                await client.delete_message(message)
            except:
                pass
            await client.send_message(message.author, embed=embed)
        except:
            embed = discord.Embed(title=':no_entry: ERROR', description='Invalid message token!', color= 0xf44242)
            error = await client.send_message(message.channel, embed=embed)
            await asyncio.sleep(10)
            await client.delete_message(error)
            try:
                await client.delete_message(message)
            except:
                pass

    elif '$HELP' == message1:
        embed = discord.Embed(title='HELP', color= 0x4fff63)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/551333056078675970/551373116241346580/data_encryption.jpg')
        embed.add_field(name='$encrypt <message>',value='Encrypt message to crypted token.\n\u200B',inline=False)
        embed.add_field(name='$decrypt <crypted token>',value='Decrypt crypted token to message.\n\u200B',inline=False)
        embed.add_field(name='Get CryptoBOT',value='Click [here](https://discordapp.com/oauth2/authorize?client_id=551322860875153418&scope=bot&permissions=387072) to invite CryptoBOT to your server!')
        await client.send_message(message.channel, embed=embed)

client.run('NTUxMzIyODYwODc1MTUzNDE4.D1vTNw.MEy6YwOf5sfb9q3XIzNkjXsCPRw')
#https://discordapp.com/oauth2/authorize?client_id=551322860875153418&scope=bot&permissions=387072

