from google import genai

from dotenv import load_dotenv

import os


load_dotenv()


def summarize(delta: str):

    client = genai.Client()  # picks up GEMINI_API_KEY from env automatically

    interaction = client.interactions.create(

        model="gemini-3.5-flash",

        input=f"You are a senior software engineer. Explain the changes made to the given git repository between the users last seen commit and the head commit, given as a git diff:\n\n{delta}"

    )

    return interaction.output_text

