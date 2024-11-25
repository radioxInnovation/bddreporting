import pypandoc
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert(text, outputfile, **kwargs):
    prefix = kwargs.get("prefix", "xml")
    encoding = kwargs.get("encoding", "utf-8")
    classes = kwargs.get("classes", [])

    # Step 1: Convert Markdown to HTML using pypandoc
    html_text = pypandoc.convert_text(text, 'html', format='md')

    # Step 2: Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")

    # Define root XML tag
    root = ET.Element(kwargs.get("root", "steps"))

    # Add attributes from the `attr` dictionary to the root element
    for key, value in kwargs.get("attr", {}).items():
        root.set(key, value)
    
    # Add classes as a single class attribute to the root element
    if len(classes) > 0:
        root.set("class", " ".join(classes))

    # Step 3: Process each tag, adding specific data-xml-* attributes
    for i, tag in enumerate(soup.find_all(True), start=1):  # True finds all tags
        # Check if there are any 'xml-*' attributes in this tag
        xml_attrs = {attr: value for attr, value in tag.attrs.items() if attr.startswith(f"data-{prefix}")}

        # If xml-* attributes exist, process each in sorted order
        for attr_name in sorted(xml_attrs.keys()):
            attr_value = xml_attrs[attr_name]
            # Wrap the XML snippet in a temporary root to handle multiple nodes
            wrapped_value = f"<root>{attr_value}</root>"
            try:
                # Parse the wrapped XML snippet and add each child element to root
                temp_root = ET.fromstring(wrapped_value)
                for child in temp_root:
                    root.append(child)
            except ET.ParseError as e:
                print(f"Error parsing {attr_name}: {e}")

    # Convert the final XML structure to a string
    rough_xml_output = ET.tostring(root, encoding=encoding, method="xml")

    # Pretty-print the XML using minidom
    parsed_xml = minidom.parseString(rough_xml_output)
    pretty_xml_output = parsed_xml.toprettyxml(indent=" " * 4)

    # Write to output file
    with open(outputfile, "w", encoding=encoding) as file:
        file.write(pretty_xml_output)

if __name__ == '__main__':
    # Example usage
    markdown_text = """
# Title {xml-01="<tag1>some text</tag1><tag2>other text</tag2>" xml-02="<tag3>final text</tag3>"}

This is a **bold** text and *italic* text.

- Item 1
- Item 2
"""

    convert(markdown_text, "test.xml")
