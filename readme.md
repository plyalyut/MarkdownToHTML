# Markdown2HTML

The following is a Markdown to HTML converter. It first parses the markdown file using a variety of regex expressions and converts it into a series of Elements in a treelike structure. From there the HTMLFactory recursively converts that element tree into a series of HTML expressions, and saves the result to the disk. 

## How to run
1. Make sure you have Python 3.9+ installed and `pip` installed.
2. Run `pip install pipenv`.
3. Run `pipenv install` followed by `pipenv shell`.
4. Run the runner file by `python3 runner.py --input_filepath "MARKDOWN_FILE" --output_filepath "HTML_OUTPUT_FILE"`, replacing MARKDOWN_FILE and HTML_OUTPUT_FILE with the correct filepaths.
5. This this should generate a HTML file in the directory specified by HTML_OUTPUT_FILE.

## How to run tests
1. Follow steps 1-3 above, setting up the pipenv environement.
2. Run `python3 -m unittest tests.test_markdown_interpreter`

