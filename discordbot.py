import os
import re
import discord
import mysql.connector
from dotenv import load_dotenv
from discord.ext import commands
from requestgpt import RequestGPT as RGPT

class Read():

    def read_msgs(client):

        @client.event
        async def on_ready():
            print(f'{client.user.name} has connected to Discord!')


        @client.event
        async def on_message(message):

            # Prevent self-recursion
            if message.author == client.user:
                return
            
            # Help Command
            if message.content.startswith('.help'):
                if message.content[1:5] == 'help':
                    expression = message.content[6:]
                    output = """
**Hello! 👋 I'm May Bot. How may I help you? ✩‧₊˚** 

**May Bot Commands** 📝
1. **May Bot AI** 
    •Example: .cgpt What's the tallest building in the world? 
2.  **Personal Database** 
    •Example: .store [Name] [Message] 
    •Example: .view [Name] 
    •Example: .delete [Name] [Message] 
3. **Programmable Calculator** 
    •Example: .calc (2**31)
                        """
                    await message.channel.send(output)
                    return

            # Calculate Function
            if message.content.startswith('.calc'):
                expression = message.content[6:].replace("^","**")
                allowed = ['pow','max','min','int','sum','floor','ceil','sorted','reversed']
                pattern = re.compile('[a-zA-Z]')
                check = bool(pattern.search(expression))
                if check:
                    i = 0
                    for functions in allowed:
                        i += 1
                        if functions in expression:
                            await message.channel.send('The answer to ' + expression.replace("**","^") + ' is: ' + "**" + str(eval(expression)) + "**")
                            return
                        if i == len(allowed):
                            await message.channel.send('https://tenor.com/view/caught-in-4k-caught-in4k-chungus-gif-19840038')
                            return
                else:
                    await message.channel.send('The answer to ' + expression.replace("**","^") + ' is: ' + "**" + str(eval(expression)) + "**")
                        

            # Save Author Reminders
            if message.content.startswith('.me.new'):
                user_input = message.content[7:].replace("```","")
                file_name = str(message.author) + ".txt"

                with open("/Users/NAME/Projects/Personal/MayBot/User_Data/" + str(file_name), "w") as f:
                    f.write(user_input)
                    return 

            # View Author Reminders
            if message.content.startswith('.me.view'):
                file_name = str(message.author) + ".txt"

                with open("/Users/NAME/Projects/Personal/MayBot/User_Data/" + str(file_name), "r") as f:
                    await message.channel.send(f.read())
                    return 

            # Proud Mother
            if message.content == 'good girl':
                await message.channel.send('https://cdn.discordapp.com/attachments/1075159453315383427/1075196981829435402/happy.png')
                return
            
            # MySQL - Store
            if message.content.startswith('.store'):

                # You can play with this and store the data however you want really
                message_content = message.content[6:]
                words = message_content.split()
                username = words[0]
                message_content = ' '.join(words[1:])

                # Store your MySQL info into a .env file
                DB_HOST = os.getenv("DB_HOST")
                DB_USER = os.getenv("DB_USER")
                DB_PASSWORD = os.getenv("DB_PASSWORD")
                DB_NAME = os.getenv("DB_NAME")
                DB_TABLE = os.getenv("DB_TABLE")

                # MySQL database connection
                db = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )

                # This is where your MySQL queries would go 
                cursor = db.cursor()

                # This is where your MySQL queries would go 
                sql = "INSERT INTO " + DB_TABLE + " (column1, column2) VALUES (%s, %s)"
                val = (username, message_content)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()

            # MySQL - Retrieve & View
            if message.content.startswith('.view'):

                # You can play with this and store the data however you want really
                message_content = message.content[5:]
                words = message_content.split()
                username = words[0]

                # Store your MySQL info into a .env file
                DB_HOST = os.getenv("DB_HOST")
                DB_USER = os.getenv("DB_USER")
                DB_PASSWORD = os.getenv("DB_PASSWORD")
                DB_NAME = os.getenv("DB_NAME")
                DB_TABLE = os.getenv("DB_TABLE")

                # MySQL database connection
                db = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )

                # This is where your MySQL queries would go 
                cursor = db.cursor()

                # Retrieve all instances of user in MySQL table
                query = "SELECT * FROM discord_table WHERE column1 = %s"
                cursor.execute(query, (username,))
                rows = cursor.fetchall()

                # Discord output
                output = ""
                for row in rows:
                    output += str(row) + "\n"
                await message.channel.send(output)

            if message.content.startswith('.delete'):
                message_content = message.content[7:]
                words = message_content.split()
                username = words[0]
                message_content = ' '.join(words[1:])

                # Store your MySQL info into a .env file
                DB_HOST = os.getenv("DB_HOST")
                DB_USER = os.getenv("DB_USER")
                DB_PASSWORD = os.getenv("DB_PASSWORD")
                DB_NAME = os.getenv("DB_NAME")
                DB_TABLE = os.getenv("DB_TABLE")

                # MySQL database connection
                db = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )

                # This is where your MySQL queries would go 
                cursor = db.cursor()

                try:
                    # Define the SQL query to delete rows matching both name and string
                    query = "DELETE FROM {} WHERE column1 = %s AND column2 = %s".format(DB_TABLE)

                    # Execute the query with the username and string_to_delete as parameters
                    cursor.execute(query, (username, message_content,))
                    
                    # Commit the changes to the database
                    db.commit()
                    
                    # Check if any rows were affected (deleted)
                    if cursor.rowcount > 0:
                        return f"Deleted {cursor.rowcount} row(s) with the name: {username} and string: {message_content}"
                    else:
                        return f"No rows found with the name: {username} and string: {message_content}"

                except mysql.connector.Error as error:
                    await message.channel.send(f"{username}'s message [{message_content}] cannot be found.")


            # ChatGPT Function
            if message.content.startswith('.cgpt'):
                prompt = message.content[5:]
                print(prompt)

                # Request ChatGPT API to answer the user's given prompt
                answer = RGPT.answer(prompt)

                # Post-processing 
                i = answer.find("\n")
                answer = answer[i:]

                await message.channel.send(answer)




            
                