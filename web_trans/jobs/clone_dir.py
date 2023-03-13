import shutil
from web_trans.jobs.base import BaseJob


class CloneDir(BaseJob):
    def __init__(self, src_dir_path: str, cloned_dir_path: str) -> None:
        self.src_dir_path = src_dir_path
        self.cloned_dir_path = cloned_dir_path
        self.is_cloned = False

    def execute_job(self) -> None:
        shutil.copytree(self.src_dir_path, self.cloned_dir_path, dirs_exist_ok=True)
        self.is_cloned = True

    def is_cloned(self) -> bool:
        return self.is_cloned
