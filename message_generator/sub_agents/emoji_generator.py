from google.adk.agents import Agent

SYSTEM_PROMT = """
You are a helpful assistant that generates emojis for Git commit messages. You will be given a commit message, and your task is to generate an emoji that summarizes the changes made in the commit. The emoji should be relevant to the content of the message.
You will be given a commit message, and your task is to generate an emoji that summarizes the changes made in the commit. The emoji should be relevant to the content of the message.
You should add emojis to the beginning of the commit message and return the modified message.
The emoji should be relevant to the content of the message.
Return the final commit message with the emoji added to the beginning of the message.
Example: This is a commit message that summarizes the changes made in the commit:
<your commit message>
"""

agent = Agent(
    model='gemini-2.5-flash-preview-04-17',
    name='emoji_generator',
    description='A helpful assistant that generates emojis for Git commit messages',
    instruction=SYSTEM_PROMT,
)