from pydantic import BaseModel
from abc import abstractmethod


class Bases(BaseModel):
    def get_member(self, name: str):
        for key, value in self.__dict__.items():
            if (callable(value) is False) and (key == name):
                return print(key, value)
        print(f"{name} does not exist")

    def get_members(self):
        return [key for key, value in self.__dict__.items()]

    def get_members_list(self):
        pass

    def todict(self):
        return {key: value for key, value in self.__dict__.items()}

    def addSymbol(self, operator=","):
        return [
            f"{key} {operator} '{value}'" for key,
            value in self.__dict__.items()]

    @abstractmethod
    def get_member_by_key(self, key):
        pass

    @property
    @abstractmethod
    def primary_key(self):
        pass
