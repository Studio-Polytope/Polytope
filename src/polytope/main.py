import os
from dotenv import load_dotenv

from polytope.github.repository.RepositoryConfig import GithubRepositoryConfig

GITHUB_TOKEN: str = ''


def load_environment():
    global GITHUB_TOKEN

    load_dotenv()
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


if __name__ == "__main__":
    load_environment()

    from polytope.github.repository import GithubRepository
    from polytope.github.Token import Token

    ghr = GithubRepository(
        "TAMREF",
        "test_polytope",
        Token(GITHUB_TOKEN)
    )

    print("================")
    res = ghr.create()
    print(res.status_code)
    print(res.content)

    print("================")
    res2 = ghr.get()
    print(res2.status_code)
    print(res2.content)

    print("================")
    res3 = ghr.update(GithubRepositoryConfig("test_polytope_name_changed"))
    print(res3.status_code)
    print(res3.content)

    print("================")
    res4 = ghr.delete()
    print(res4.status_code)
    print(res4.content)