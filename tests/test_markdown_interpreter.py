#!/usr/bin/env python3

import unittest

import app
from app import markdown2html
from app.markdown2html import MarkdownParser
from app.utils.element import Element, HeadingElement, LinkElement, NullElement, ParagraphElement, TextElement
from typing import List


paragraph_tags_combine = [ParagraphElement(content=[TextElement()]),
 ParagraphElement(content=[TextElement(), TextElement()]), NullElement()]

string_with_multiple_links = "[www.google.com](google) is a popular webiste, so is [mailchimp.com](mailchimp)"

sample_data = ["# Sample Document", "Hello!",
"This is sample markdown for the [Mailchimp](https://www.mailchimp.com) homework assignment."]


class TestMarkdownInterpreter(unittest.TestCase):
    def test_combine_paragraphs(self):
        """
        Tests combining tags together e.g. p, p, null => p, null
        """
        output: List[Element] = MarkdownParser.combine_paragraph_lines(paragraph_tags_combine)
        self.assertEqual(len(output), 2)
        self.assertEqual(len(output[0].content), 3)

    def test_split_string(self):
        """
        Checks for how strings are split along 
        """
        output: List[Element] = MarkdownParser.split_string(string_with_multiple_links)
        self.assertEqual(len(output), 3)
        self.assertTrue(isinstance(output[0],  LinkElement))
        self.assertTrue(isinstance(output[1], TextElement))
        self.assertTrue(isinstance(output[2], LinkElement))

    def test_parse(self):
        """
        Checks that you can parse all sorts of elements
        """
        md_parser = MarkdownParser(filepath="./data/sample_1.md")
        parse = md_parser.parse()
        self.assertTrue(isinstance(parse[0], HeadingElement))
        self.assertTrue(isinstance(parse[1], NullElement))
        self.assertTrue(isinstance(parse[2], ParagraphElement))
        self.assertTrue(isinstance(parse[3], NullElement))
        self.assertTrue(isinstance(parse[4], ParagraphElement))

    def test_link_variations(self):
        """
        Tests parsing different types of link variations.
        e.g. Heading, Link
            Link on its own
            Link with additional text after it
        """
        md_parser = MarkdownParser(filepath="./data/link_test.md")
        parse = md_parser.parse()
        self.assertTrue(isinstance(parse[0], LinkElement))
        self.assertTrue(isinstance(parse[1], HeadingElement))
        self.assertTrue(isinstance(parse[2], ParagraphElement))


    def test_paragraph_parsing(self):
        """
        Tests the paragraph merging behavior.
        """
        md_parser = MarkdownParser(filepath="./data/paragraph_test.md")
        parse = md_parser.parse()
        self.assertTrue(len(parse), 4) # The first two lines should be comibined into one
    
        

if __name__ == '__main__':
    unittest.main()



