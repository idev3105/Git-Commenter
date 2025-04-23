from google.adk.agents import LlmAgent
from .sub_agents import diff_generator, emoji_generator, message_generator, path_agent

SYSTEM_PROMPT = """
You are a helpful assistant that generates commit messages for Git repositories.
You will be given a path of Git repository. Your task is to generate a comment that summarizes the changes made in the commit. The comment should be concise and informative.
You should ask user to provide the path of the Git repository.
Use diff_generator to generate the diff for the unstaged changes in the repository. The diff should be clean and easy to read.
Use message_generator to generate a comment based on the diff.
Use emoji_generator to generate an emoji that summarizes the changes made in the commit. The emoji should be relevant to the content of the message.
"""

root_agent = LlmAgent(
    name='coordinator',
    model='gemini-2.5-flash-preview-04-17',
    description='A pipeline agent that generates commit messages for Git repositories',
    instruction=SYSTEM_PROMPT,
    sub_agents=[diff_generator.agent, message_generator.agent, emoji_generator.agent],
)
