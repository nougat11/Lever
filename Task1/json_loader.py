"""This module contains classes of load information"""
import json


class JsonLoader:
    """This class loads information from json file"""
    def __init__(self, path):
        try:
            open(path, 'r')
        except FileNotFoundError:
            print("File Error: File not found!")
        self.path = path

    def load_json(self):
        """This method loads information from json file"""
        with open(self.path, 'r') as file:
            return json.load(file)
