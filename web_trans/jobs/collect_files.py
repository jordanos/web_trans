from web_trans.jobs.base import BaseJob
from web_trans.web_files.base import BaseWebFile
import glob


class CollectFiles(BaseJob):
    def __init__(self, dir_path: str, file_type: str) -> None:
        self.web_files: list[BaseWebFile] = None
        self.dir_path = dir_path
        self.file_type = file_type

    def execute_job(self):
        files = glob.glob(self.dir_path + f"/**/*.{self.file_type}", recursive=True)
        return files
