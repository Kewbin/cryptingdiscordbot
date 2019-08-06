import discord
import asyncio
import datetime
import mysql.connector
from mcstatus import MinecraftServer
import config

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    await client.change_presence(game=discord.Game(name="at FireRedwood.aternos.me"))

@client.event
async def on_message(message):
    message1 = str(message.content).split(' ',1)[0].upper()
        
    if '.BALTOP' == message1:
        await client.send_typing(message.channel)
        try:
            mySQLconnection = mysql.connector.connect(host='remotemysql.com',
                database='3DC9jFsMhS',
                user='3DC9jFsMhS',
                password='CAM1XJFAlz')
        except:
            print('error')
        sql_select_Query = "select * from Economy where Name != 'kewbin' order by Balance desc limit 5"
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        balances = cursor.fetchall()
        width = len('{:,}'.format(int(balances[0][1])))+2
        i=0
        embed = discord.Embed(title=':trophy: **PLAYERS WITH HIGHEST AMOUNT OF MONEY**', description='⠀', color= 0x42f548)
        for row in balances:
            i = i+1
            if i == 1:
                pos = ':first_place:'
            elif i == 2:
                pos = ':second_place:'
            elif i == 3:
                pos = ':third_place:'
            elif i == 4:
                pos = ':four:'
            elif i == 5:
                pos = ':five:'

            
            embed.add_field(name='{:⠀<2s}{:⠀>{width}s}{:⠀^2s}{:⠀<15s}'.format(pos + ' ` ','${:,}'.format(int(row[1])) + '`', ' | ', row[0].upper() , width=width), value='⠀', inline=False)


        
        await client.send_message(message.channel, embed=embed)
        cursor.close()
            
    elif '.TOPTIME' == message1:
        await client.send_typing(message.channel)
        try:
            mySQLconnection = mysql.connector.connect(host='remotemysql.com',
                database='3DC9jFsMhS',
                user='3DC9jFsMhS',
                password='CAM1XJFAlz')
        except:
            print('error')
        sql_select_Query = "SELECT uuid, CAST(time AS UNSIGNED) as inttime from playertime order by inttime desc limit 5"
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        times = cursor.fetchall()

        time = int(times[0][1])/1000
        width = len(str(datetime.timedelta(seconds=time)))+1

        uuids = {}

        sql_select_Query = "select * from luckperms_players"
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        names = cursor.fetchall()

        for row in names:
            uuids.update({row[0] : row[1]})
        
        i=0
        embed = discord.Embed(title=':trophy: **PLAYERS WITH HIGHEST PLAYTIME**', description='⠀', color= 0x42f548)
        for row in times:
            i = i+1
            if i == 1:
                pos = ':first_place:'
            elif i == 2:
                pos = ':second_place:'
            elif i == 3:
                pos = ':third_place:'
            elif i == 4:
                pos = ':four:'
            elif i == 5:
                pos = ':five:'
            time = int(row[1])/1000
            embed.add_field(name='{:⠀<2s}{:⠀>{width}s}{:⠀^2s}{:⠀<15s}'.format(pos + ' ` ', str(datetime.timedelta(seconds=time)) + '`', ' | ', uuids.get(row[0]).upper() , width=width), value='⠀', inline=False)
        await client.send_message(message.channel, embed=embed)
        cursor.close()

    elif '.STATS' == message1:
        await client.send_typing(message.channel)
        message2 = str(message.content).split(' ',1)[1]
        try:
            mySQLconnection = mysql.connector.connect(host='remotemysql.com',
                database='3DC9jFsMhS',
                user='3DC9jFsMhS',
                password='CAM1XJFAlz')
        except:
            print('error')

        playerdata = {}

        sql_select_Query = "select * from luckperms_players where username = '" + str(message2).lower() + "'" 
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        names = cursor.fetchall()

        for row in names:
            playerdata.update({row[1] : [row[0], row[2]]})

        try:
            sql_select_Query = "select * from wg_user where uuid = '" + playerdata.get(message2.lower())[0] + "'" 
            cursor = mySQLconnection .cursor()
            cursor.execute(sql_select_Query)
            wg_id = cursor.fetchall()


            playerdata[message2].append(wg_id[0][0])
            playerdata[message2].append({'regions':[]})
        except:
            playerdata[message2].append('id')
            playerdata[message2].append({'regions':[]})
            

        try:
            sql_select_Query = "select region_id from wg_region_players where user_id = '" + str(playerdata.get(message2.lower())[2]) + "' and owner = '1' and world_id = '6'" 
            cursor = mySQLconnection .cursor()
            cursor.execute(sql_select_Query)
            regions = cursor.fetchall()

            if regions == []:
                playerdata[message2][3]['regions'].append('This player does not own any region!')
            else:
                for row in regions:
                    playerdata[message2][3]['regions'].append(row[0])
        except:
            pass

        sql_select_Query = "select Balance from Economy where Name = '" + message2 + "'"
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        balance = cursor.fetchall()

        for row in balance:
            playerdata[message2].append(row[0])


        sql_select_Query = "SELECT CAST(time AS UNSIGNED) as inttime from playertime where uuid = '" + playerdata[message2][0] + "'"
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        playtime = cursor.fetchall()

        for row in playtime:
            playerdata[message2].append(row[0])


        time = int(playerdata[message2][5])/1000
        translatedtime = str(datetime.timedelta(seconds=time))

        sql_select_Query = "SELECT Skin from MySkin_Player where Player = '" + playerdata[message2][0] + "'"
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        skin = cursor.fetchall()

        if skin == []:
            playerdata[message2].append(playerdata[message2][0])
        else:
            for row in skin:
                playerdata[message2].append(row[0])

        embed = discord.Embed(title=':ballot_box_with_check: **' + message2.upper() + '**', description='⠀', color= 0x42f548)
        embed.set_thumbnail(url='https://minotar.net/helm/'+str(playerdata[message2][6]))
        embed.set_footer(text=playerdata[message2][0])
        embed.add_field(name=':shield: RANK', value=playerdata[message2][1].upper() + '\n⠀',inline=False)
        embed.add_field(name=':dollar: MONEY', value='${:,}'.format(int(playerdata[message2][4])) + '\n⠀',inline=False)
        embed.add_field(name=':clock1: PLAYTIME', value=translatedtime + '\n⠀',inline=False)
        regions = ''
        for region in playerdata[message2][3]['regions']:
            regions = regions + '- ' + region + '\n'
        embed.add_field(name=':bank: OWNED REGIONS', value=regions + '⠀',inline=False)
        await client.send_message(message.channel, embed=embed)

        cursor.close()


    elif '.SERVER' == message1:
        await client.send_typing(message.channel)
        server = MinecraftServer.lookup("fireredwood.aternos.me")
        try:
            status = server.status()
            embed = discord.Embed(title=':white_check_mark: SERVER IS ONLINE', description=':busts_in_silhouette: PLAYERS: ' + str(status.raw.get('players').get('online')) + '/' + str(status.raw.get('players').get('max')), color= 0x42f548)
        except:
            embed = discord.Embed(title=':no_entry: SERVER IS CURRENTLY OFFLINE', color= 0xe0191c)
        await client.send_message(message.channel, embed=embed)

        

    elif '.HELP' == message1:
        await client.send_typing(message.channel)
        embed = discord.Embed(title=':question: **HELP**',description='⠀', color= 0x4fff63)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/525341774969962497/608318761400795146/fire.png')
        embed.add_field(name=':white_small_square: **.server** | *Get server status*',value='⠀' ,inline=False)
        embed.add_field(name=':white_small_square: **.baltop** | *Shows money leaderboard*',value='⠀',inline=False)
        embed.add_field(name=':white_small_square: **.toptime** | *Shows playtime leaderboard*',value='⠀',inline=False)
        embed.add_field(name=':white_small_square: **.stats** <playerName> | *Shows players stats*',value='⠀' ,inline=False)
        await client.send_message(message.channel, embed=embed)

client.run(config.token)
#https://discordapp.com/oauth2/authorize?client_id=551322860875153418&scope=bot&permissions=387072

