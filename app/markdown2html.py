#!/usr/bin/env python3

from enum import Enum
from io import FileIO
from app.utils.element import MAX_HEADING_COUNT, HeadingElement, LinkElement, NullElement, ParagraphElement, ElementType, Element, TextElement
from app.utils.filereader import FileReader
from app.utils.parsing import Parser
from typing import List, Optional
import re
import dominate
from dominate.tags import *
from dominate.util import *

class MarkdownReader(FileReader):
    """
    Handles reading in a markdown file and storing it line by line.
    """

    def __init__(self, filepath: str):
        self.__data: List[str] = self.read_file(filepath)

    @property
    def data(self):
        """
        Getter for the data after reading a file.
        Returns: Markdown file broken into lines
        """
        return self.__data

    def read_file(self, filepath: str) -> List[str]:
        """
        Reads the file, first checking if the filename
        ends in a valid Markdown extension.
        Returns: List of strings containing each line of the markdown file. 
        """
        if filepath.endswith(".md"):
            return super().read_file(filepath)
        else:
            raise IOError("Not a valid Markdown file format")


LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
HEADER_PATTERN = re.compile(r"#+")

class MarkdownParser(Parser):
    """
    Parses the markdow into a usable tree link format.
    """
    
    def __init__(self, filepath: str):
        """
        Initializes the raw data and the initial list for the processed data.
        """
        self.raw_data = MarkdownReader(filepath).data
        self.processed_data: List[Element] = []

    def parse(self) -> List[Element]:
        """
        Converts the raw data into a match function
        """ 
        proccessed_data = []
        match_functions = [
            MarkdownParser.parse_empty_line,
            MarkdownParser.parse_heading,
            MarkdownParser.parse_link_root
        ]
        
        for line in self.raw_data:
            line = line.strip()
            matched: Element = None
            # Get the root element
            for match_fn in match_functions:
                matched = match_fn(line)
                if matched:
                    break
            if not matched:
                matched = MarkdownParser.create_paragraph()
            
            # Check if we need to move up a few spaces ahead from the heading.
            offset = 0
            if matched.element_type == ElementType.HEADING:
                offset = matched.level + 1
            elif matched.element_type == ElementType.LINK or matched.element_type == ElementType.NULL_ELEMENT:
                proccessed_data.append(matched)
                continue
            
            # Split string 
            sub_contents = MarkdownParser.split_string(line[offset:])
            for content_element in sub_contents:
                matched.add_content(content_element)
            proccessed_data.append(matched)

        # Combine paragraph tags together
        self.processed_data = MarkdownParser.combine_paragraph_lines(proccessed_data)
        return self.processed_data

    @staticmethod
    def split_string(s: str) -> List[Element]:
        """
        Breaks up a string into text and link parameters
        """
        # Find all the text
        start = 0
        full_list = []
        matches = re.finditer(LINK_PATTERN, s)
        for match in matches:
            if match.start() - start > 0:
                full_list.append(TextElement(text = s[start: match.start()]))
            link = match.group(2)
            content = match.group(1)
            base_element = MarkdownParser.create_link_element(href = link, text = content)
            full_list.append(base_element)
            start = match.end()
        if start < len(s):
            full_list.append(TextElement(text = s[start: len(s)]))
        return full_list

    @staticmethod
    def create_link_element(href: str, text: str):
        """ Creates a link element w"""
        link_element =  LinkElement(href= href)
        sub_text = TextElement(text = text)
        link_element.add_content(sub_text)
        return link_element
    
    @staticmethod
    def parse_heading(s: str) -> Optional[Element]:
        """
        Attempts to parse a heading, if a heading can't be parsed return None.
        s: String representation of the line
        """
        match = re.match(HEADER_PATTERN, s)
        if match and match.start() == 0 and match.end() - match.start() <= MAX_HEADING_COUNT:
            # Hashtags are followed by a space, otherwise its not a heading
            if len(s) > match.end() and s[match.end()] == " ":
                header_level = match.end() - match.start()
                return HeadingElement(level = header_level)
        return None

    @staticmethod
    def parse_empty_line(s: str) -> Optional[Element]:
        """
        If a line is empty, returns a NullElement. Otherwise returns None
        s: String representation of the line
        """
        if len(s.strip()) == 0:
            return NullElement()
        return None

    def parse_link_root(s: str) -> Optional[Element]:
        """
        Attempts to parse a link.
        s: String representation of the line 
        """
        matches = re.finditer(LINK_PATTERN, s)
        temporary_count = 0
        first_entry = None
        for match in matches:
            temporary_count += 1
            first_entry = match
        if temporary_count != 1: # For the root tag to be an LinkElement, it needs to only have the link.
            return None
        if first_entry.start() == 0 and first_entry.end() == len(s):
            return MarkdownParser.create_link_element(href=first_entry.group(2), text = first_entry.group(1))
        return None
    
    @staticmethod
    def create_paragraph() -> Element:
        """
        Create empty Paragraph element
        """
        return ParagraphElement()
        
    @staticmethod
    def combine_paragraph_lines(parsed_data):
        """
        Combines multiple pargraph lines into one entry as specified by the
        Markdown user guide: https://daringfireball.net/projects/markdown/syntax#html
        Returns: New elements with combined paragraph lines. 
        """
        i = 0
        new_elements = []
        curr_element: Optional[Element] = None
        while i < len(parsed_data):
            if parsed_data[i].element_type == ElementType.PARAGRAPH:
                if curr_element != None:
                    curr_element.content.extend(parsed_data[i].content)
                else:
                    curr_element = parsed_data[i]
            else:
                if curr_element != None:
                    new_elements.append(curr_element)
                    curr_element = None
                new_elements.append(parsed_data[i])
            i += 1
        if curr_element != None:
            new_elements.append(curr_element)
        return new_elements

        

class HTMLFactory:
    """
    Builds the HTML document by parsing 
    """
    def __init__(self, element_list: List[Element]):
        self.html_structure = element_list
        self.doc = None

    def generate_html(self):
        """
        Generates the HTML by recursively going down the
        HTML components up until the root node.
        """
        doc = dominate.document(title='Markdown Parse')
        with doc:
            for element in self.html_structure:
                self.convert_element_to_html_tags(element)
        print(doc)
        self.doc = doc

    def convert_element_to_html_tags(self, e: Element):
        """
        Recursively converts an element into an HTML component.
        Returns root tag
        """
        h_levels = {
            1: h1,
            2: h2,
            3: h3,
            4: h4,
            5: h5,
            6: h6
        }

        tag = None
        if e.element_type == ElementType.HEADING:
            tag: html_tag = h_levels[e.level]()
        elif e.element_type == ElementType.LINK:
            tag: link = a(href = e.href)
        elif e.element_type == ElementType.PARAGRAPH:
            tag: p = p()
        elif e.element_type == ElementType.TEXT:
            return text(e.text)
        else:
            return br()

        for sub_element in e.content:
            tag.add(self.convert_element_to_html_tags(sub_element))
        
        return tag

    def save_html(self, filepath: str):
        """
        Saves the html to file.
        """
        if not self.doc:
            raise IOError("The document needs to be parsed first")

        with open(filepath, "w") as f:
            f.write(self.doc.render())
    

if __name__ == "__main__":
    markdown_object = MarkdownReader("data/link_test.md")

    parse = MarkdownParser(filepath="data/sample_2.md").parse()
    html_factory = HTMLFactory(parse)
    html_factory.generate_html()
    html_factory.save_html("output/sample_1.html")

