from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_environment_var(key):
    """
    Returns the value of a given environment variable key or None.

    If the key doesn't exist in the operating system environment variables, it
    looks for key in a '.env' file (via the dotenv library).

    Arguments:
    key -- the environment variable key

    Returns:
    The corresponding value of the key, or None if it doesn't exist.
    """
    return os.environ.get(key)
