from dataclasses import dataclass
from typing import Tuple


@dataclass
class GithubRepositoryConfig:
    name: str
    description: str = ""
    homepage: str = ""
    private: bool = True
    has_issues: bool = True
    has_projects: bool = True
    has_wiki: bool = True
    has_discussions: bool = True
    auto_init: bool = False
    gitignore_template: str = ""
    license_template: str = ""
    allow_squash_merge: bool = True
    allow_merge_commit: bool = True
    allow_rebase_merge: bool = True
    allow_auto_merge: bool = False
    delete_branch_on_merge: bool = False
    squash_merge_commit_title: str = "PR_TITLE"
    squash_merge_commit_message: str = "COMMIT_MESSAGES"
    merge_commit_title: str = "PR_TITLE"
    merge_commit_message: str = "PR_BODY"
    has_downloads: bool = True
    is_template: bool = False

    def validate(self) -> Tuple[bool, str]:
        # TODO : adopt github's own validation rules in advance
        if len(self.name) == 0:
            return False, "name should be non-empty"

        # validate squash commit combo
        squash_commit_combo = (self.squash_merge_commit_title, self.squash_merge_commit_message)
        if squash_commit_combo not in (
            ("PR_TITLE", "PR_BODY"),
            ("PR_TITLE", "BLANK"),
            ("PR_TITLE", "COMMIT_MESSAGES"),
            ("COMMIT_OR_PR_TITLE", "COMMIT_MESSAGES"),
        ):
            return False, "squash commit combo is not valid"

        return True, ""