#!/usr/bin/env python3

from abc import ABC, abstractmethod

class Parser(ABC):
    """
    Interface for parsing data objects.
    """

    @abstractmethod
    def parse(self):
        raise NotImplementedError

    #@abstractmethod
    #def parsed_representation(self):
    #    raise NotImplemented
