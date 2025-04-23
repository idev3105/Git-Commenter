import git.util
from google.adk.agents import Agent
import git
import os
import os.path as osp

SYSTEM_PROMT = """
You are a helpful assistant that generates Git diff.
You will be given a path to a Git repository, and your task is to generate the diff for the unstaged changes in the repository. The diff should be clean and easy to read.
You should ask the user to provide the path of the Git repository.
You should detect the Git repository from user input and use tool to check if the provided path is a valid Git repository and get the diff.
You MUST follow the instructions below:
1. Get the path of the Git repository from the user.
2. Check if the provided path is a valid Git repository using the is_git_dir tool.
3. For each file that was changed in the commit, use the git_diff_staged tool to get the diff for staged changes.
4. For each file that was changed in the commit, use the git_diff_unstaged tool to get the diff for unstaged changes

When have the diff, you should summarize the changes made for each file
Example:
.gitignore: Added .env to .gitignore
README.md: Updated the README file with new instructions
"""

def is_git_dir(path: str) -> bool:
    """
    Check if the given directory is a Git repository.
    Args:
        d (str): The path to the directory.
    Returns:
        bool: True if the directory is a Git repository, False otherwise.
    """
    if osp.isdir(path):
        if (osp.isdir(osp.join(path, "objects")) or "GIT_OBJECT_DIRECTORY" in os.environ) and osp.isdir(
            osp.join(path, "refs")
        ):
            headref = osp.join(path, "HEAD")
            return osp.isfile(headref) or (osp.islink(headref) and os.readlink(headref).startswith("refs"))
        elif (
            osp.isfile(osp.join(path, "gitdir"))
            and osp.isfile(osp.join(path, "commondir"))
            and osp.isfile(osp.join(path, "gitfile"))
        ):
            return False
    return False

def git_add(path: str, files: list[str]) -> str:
    """
    Stages the specified files in the Git repository at the given path.
    Args:
        path (str): The path to the Git repository.
        files (list[str]): A list of file paths to stage.
    Returns:
        str: A message indicating the result of the staging operation.
    """
    repo = git.Repo(path)
    files_with_full_path = [osp.join(path, file) for file in files]
    repo.index.add(files_with_full_path)
    return "Files staged successfully"

def git_status(path: str) -> str:
    """
    Retrives the status of the Git repository at the given path.
    List the files that were changed in the commit.
    Args:
        path (str): The path to the Git repository.
    Returns:
        str: The status of the repository, including staged and unstaged changes.
    """
    repo = git.Repo(path)
    return repo.git.status()

def git_diff_unstaged(path: str) -> str:
    """
    Retrives the diff for unstaged changes in the repository at the given path.
    Args:
        path (str): The path to the Git repository.
    Returns:
        str: The diff for unstaged changes, or a message indicating no changes were found.
    """
    repo = git.Repo(path)
    if repo.is_dirty(untracked_files=True):
        return repo.git.diff()
    else:
        return "No unstaged changes found."

def git_diff_staged(path: str) -> str:
    """
    Retrives the diff for staged changes in the repository at the given path.
    Args:
        path (str): The path to the Git repository.
    Returns:
        str: The diff for staged changes, or a message indicating no changes were found.
    """
    repo = git.Repo(path)
    if repo.is_dirty(untracked_files=True):
        return repo.git.diff("--cached")
    else:
        return "No staged changes found."

def git_diff_no_index(path: str, file_path: str) -> str:
    """
    Retrieves the diff for new files in the repository at the given path.
    Args:
        path (str): The path to the Git repository.
        file_path (str): The path to the file to check for changes.
    Returns:
        str: The diff for the new file, or a message indicating no changes were found.
    """
    repo = git.Repo(path)
    full_file_path = osp.join(path, file_path)
    try:
        # Pass NUL without quotes
        return repo.git.diff("--no-index", "NUL", full_file_path)
    except git.exc.GitCommandError as e:
        return f"Error generating diff: {e}"

agent = Agent(
    model='gemini-2.5-flash-preview-04-17',
    name='diff_generator',
    description='A helpful assistant that generates Git diff',
    tools=[is_git_dir, git_status, git_diff_unstaged, git_diff_staged, git_diff_no_index],
    instruction=SYSTEM_PROMT,
)

if __name__ == "__main__":
    # Test the agent with a sample path
    path = "C:\\Users\\63200251\\Documents\\projects\\git_commenter"
    print(git_diff_staged(path))