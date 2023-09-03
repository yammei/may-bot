from dotenv import *
import openai
import os

class RequestGPT:

    def answer(prompt):

        TOKEN = os.getenv('OPENAI_API_KEY')
        openai.api_key = str(TOKEN)

        max_tokens = 50

        instructions = f""". Keep your response under {max_tokens} tokens by summarizing. 
            Explain the any topics as if you're talking to a university student. 
            Add 1-2 appropriate emojis to the end concerning what you'll be saying. 
            Also if releveant or asked, your name is May Bot.
        """

        prompt += instructions

        # Make the API call with the prompt
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose the appropriate engine
            prompt=prompt,
            max_tokens=max_tokens,  # Set the maximum response length
            temperature=0.4  # Adjust the temperature for randomness
        )

        # ChatGPT response information
        say = response.choices[0].text
        print(str(response) + "\n" + str(response.choices) + "\n" + say)
        return say