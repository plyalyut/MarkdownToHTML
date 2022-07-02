#!/usr/bin/env python3

from typing import List

class FileReader:
    """
    FileReader handles in reading of files and storing
    the file in a useful format.
    """

    def __init__(self, filepath):
        self.__data = self.read_file(filepath)

    @property
    def data(self):
        """
        Returns the data parsed by the object.
        """
        return self.__data

    def read_file(self, filepath: str) -> List[str]:
        """
        Reads in the file if it exists.
        Inputs: Filepath (string), representing the file
        Outputs: List of 
        """
        try:
            with open(filepath) as f:
                return f.readlines()
        except:
            raise IOError("File not found")