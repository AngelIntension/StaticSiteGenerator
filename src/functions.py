import re
from textnode import TextNode, TextType

def split_nodes_delimiter(nodes, delimiter, text_type):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception(f"text contains unmatched delimiter: '{delimiter}'")
        for i in range(0, len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 1:
                new_nodes.append(TextNode(sections[i], text_type))
            else:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_link(nodes):
    return split_nodes_complex(
        nodes,
        extract_markdown_links,
        lambda link_tuple: f"[{link_tuple[0]}]({link_tuple[1]})",
        TextType.LINK)

def split_nodes_image(nodes):
    return split_nodes_complex(
        nodes,
        extract_markdown_images,
        lambda image_tuple: f"![{image_tuple[0]}]({image_tuple[1]})",
        TextType.IMAGE)

def split_nodes_complex(nodes, extract_function, split_delimiter_function, text_type):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        markdown_items = extract_function(remaining_text)
        for tuple in markdown_items:
            sections = remaining_text.split(split_delimiter_function(tuple), 1)
            remaining_text = sections[1]
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], text_type, tuple[1]))
        new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return list(filter(lambda node: node.text != "", new_nodes))

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)

def markdown_to_blocks(markdown):
    stripped_markdown = '\n'.join(map(str.strip, markdown.split('\n')))
    blocks = re.split("\n{2,}", stripped_markdown)
    blocks = list(filter(lambda block: block != "", blocks))
    return list(map(str.strip, blocks))

def block_to_block_type(block):
    # check for header markup
    regex_match = re.match(r"^(#{1,6}) ", block)
    if regex_match:
        return f"h{len(regex_match.group(1))}"

    #check for code block
    regex_match = re.match(r"^```.*```$", block, re.DOTALL)
    if regex_match:
        return "code"
    
    lines = block.split('\n')

    #check for quote block
    if all(re.match(r"^>", line) for line in lines):
        return "quote"
    
    # check for unordered list
    if all(re.match(r"^[*-] ", line) for line in lines):
        return "ul"
    
    # check for ordered list
    matches = list(map(lambda line: re.match(r"^(\d{1,})[.] ", line), lines))
    if None not in matches:
        list_numbers = list(map(lambda match: int(match.group(1)), matches))
        if list_numbers == list(range(1, len(lines) + 1)):
            return "ol"
    
    # normal paragraph
    return "p"
