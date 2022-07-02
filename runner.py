import argparse
from app.markdown2html import MarkdownParser, HTMLFactory

parser = argparse.ArgumentParser(description="Convert Markdown into HTML")

parser.add_argument("--input_filepath", type=str, help="the filepath to the input markdown file", required=True)
parser.add_argument("--output_filepath", type=str, help="the filepath to store the html somewhere", required=True)

args = parser.parse_args()

parsed = MarkdownParser(args.input_filepath).parse()
html_factory = HTMLFactory(parsed)
html_factory.generate_html()
html_factory.save_html(args.output_filepath)
