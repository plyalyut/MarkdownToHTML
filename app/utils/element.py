#!/usr/bin/env python3

from __future__ import annotations
from enum import Enum, auto
from typing import List, Dict
from dataclasses import dataclass, field

class ElementCreationError(Exception):
    ''' Exception thrown whenever there is an error building an Element'''
    pass

class ElementType(Enum):
    '''
    ElementType contains all the valid ElementTypes it could be
    '''
    HEADING = auto()
    PARAGRAPH = auto()
    LINK = auto()
    TEXT = auto()
    NULL_ELEMENT = auto()


MAX_HEADING_COUNT = 6 # Defines the max heading size

@dataclass()
class Element:
    """
    Generic Element data class. Stores a number of fields
    element_type: stores one of the element types present in the ElementType enum
    attributes: Contains element information that modifies the element (e.g. href)
    content: A list for storing the sub-elements in the tree
    allowed_sub_elements: Defines what elements are able to be the children of this element.
    """
    element_type: ElementType
    attributes: Dict[str, str] = field(default_factory=dict)
    content: List[Element] = field(default_factory=list)
    allowed_sub_elements: List[ElementType] = field(default_factory=list) # Could be not useful
    
    def add_content(self, element: Element) -> Element:
        """ Adds content elements to the element"""
        self.content.append(element)
        return self

@dataclass
class LinkElement(Element):
    ''' LinkElement data class for holding inlines and references'''
    element_type: ElementType = ElementType.LINK
    href: str = ""
    available_sub_elements = [ElementType.TEXT]

@dataclass
class ParagraphElement(Element):
    ''' Paragraph element data class for holding one or more consective pieces of text seperated by blank lines'''
    element_type: ElementType = ElementType.PARAGRAPH
    available_sub_elements = [ElementType.LINK, ElementType.TEXT]

@dataclass
class HeadingElement(Element):
    ''' Heading element for holding the heading information such as h1 etc'''
    element_type: ElementType = ElementType.HEADING
    available_sub_elements = [ElementType.LINK, ElementType.TEXT]
    level: int = 1

@dataclass
class TextElement(Element):
    ''' Text element for holding random pieces of strings'''
    element_type: ElementType = ElementType.TEXT
    text: str = ""

@dataclass
class NullElement(Element):
    ''' Null element for holding empty lines'''
    element_type: ElementType = ElementType.NULL_ELEMENT