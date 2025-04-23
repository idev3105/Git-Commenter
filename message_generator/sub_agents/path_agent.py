from google.adk.agents import Agent

SYSTEM_PROMT = """
You are a helpfull assistant to generate messages for Git commits.
You should ask user to provide the path of the Git repository.
You should detect the Git repository and return the path of the repository.
Example:
    User: I have a Git repository at /path/to/repo
    Assistant: The path of the Git repository is /path/to/repo.
"""

agent = Agent(
    model='gemini-2.5-flash-preview-04-17',
    name='path_agent',
    description='A helpful assistant that generates messages for Git commits',
    instruction=SYSTEM_PROMT,
)