import git
import os
import os.path as osp

def is_git_dir(path: str) -> bool:
    """
    Check if the given directory is a Git repository.
    Args:
        path (str): The path to the directory.
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
    Retrieves the status of the Git repository at the given path.
    Args:
        path (str): The path to the Git repository.
    Returns:
        str: The status of the repository, including staged and unstaged changes.
    """
    repo = git.Repo(path)
    return repo.git.status()

def git_diff_unstaged(path: str) -> str:
    """
    Retrieves the diff for unstaged changes in the repository at the given path.
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
    Retrieves the diff for staged changes in the repository at the given path.
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
        return repo.git.diff("--no-index", "NUL", full_file_path)
    except git.exc.GitCommandError as e:
        return f"Error generating diff: {e}"

def git_diff(path: str, target: str) -> str:
    """
    Retrieves the diff for a specific target in the repository at the given path.
    Args:
        path (str): The path to the Git repository.
        target (str): The target to check for changes.
    Returns:
        str: The diff for the target, or a message indicating no changes were found.
    """
    repo = git.Repo(path)
    full_file_path = osp.join(path, target)
    return repo.git.diff(full_file_path)