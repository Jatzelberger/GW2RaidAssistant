import os
import glob


class FileService:
    def __init__(self):
        self.folder: str = ''
        self.include_subdir: bool = False
        self.file_name: str = ''
        self.file_extension: str = ''
        self.path = ''

    def setup(
            self,
            folder: str,
            subdir: bool = True,
            file_name: str = '*',
            file_extension: str = '*'
    ):
        self.folder = folder.replace('\\', '/')
        self.include_subdir = subdir
        self.file_name = file_name
        self.file_extension = file_extension
        self.path = self.__formatPath()

    def __formatPath(self) -> str:
        path = self.folder
        if self.include_subdir:
            path += '**/' if self.folder[-1] == '/' else '/**/'
        path += f'{"" if path[-1] == "/" else "/"}{self.file_name}.{self.file_extension}'
        return path

    def get(self):
        glob_object = glob.iglob(self.path, recursive=True)
        file = max(glob_object, key=os.path.getctime, default=None)
        file = file.replace('\\', '/')
        return file
