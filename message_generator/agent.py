from google.adk.agents import LlmAgent, SequentialAgent
from .sub_agents import diff_generator, emoji_generator, message_generator, path_agent

SYSTEM_PROMPT = """
You are a helpful assistant that generates commit messages for Git repositories.
You will be given a path of Git repository. Your task is to generate a comment that summarizes the changes made in the commit. The comment should be concise and informative.
You should ask user to provide the path of the Git repository.
Use diff_generator to generate the diff  in the repository. The diff should be clean and easy to read.
When you have diff, you should use message_generator to generate a comment based on the diff.
When you have message, you should use emoji_generator to generate an emoji that summarizes the changes made in the commit. The emoji should be relevant to the content of the message.
Return the final commit message with the emoji added to the beginning of the message.
"""

root_agent = SequentialAgent(
    name='coordinator',
    # model='gemini-2.5-flash-preview-04-17',
    description='A pipeline agent that generates commit messages for Git repositories',
    # instruction=SYSTEM_PROMPT,
    sub_agents=[diff_generator.agent, message_generator.agent, emoji_generator.agent],
)
