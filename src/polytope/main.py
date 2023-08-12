import os
from dotenv import load_dotenv

GITHUB_TOKEN: str = ''


def load_environment():
    global GITHUB_TOKEN

    load_dotenv()
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


if __name__ == "__main__":
    load_environment()
    print(GITHUB_TOKEN)
