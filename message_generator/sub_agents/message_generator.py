from google.adk.agents import Agent

SYSTEM_PROMPT = """
You are a helpful assistant that generates messages for Git commits. You will be given Git diff.
Your task is to generate a comment that summarizes the changes made in the commit. The comment should be concise and informative.
User will provide Git diff, and you will generate a comment based on the diff.
Message should be in the format of a comment, and should be clear and easy to understand.
Return the final commit message
Example: This is a commit message that summarizes the changes made in the commit:
<your commit message>
"""

agent = Agent(
    model='gemini-2.5-flash-preview-04-17',
    name='message_generator',
    description='A helpful assistant that generates messages for Git commits',
    instruction=SYSTEM_PROMPT,
)