import unittest
from textnode import TextNode, TextType
from functions import *

class SplitNodesDelimiterShould(unittest.TestCase):
    def test_split_single_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_split_multiple_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        actual = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_split_node_with_multiple_delimited_strings(self):
        node = TextNode("This is text with a `code block` and another `other code block` phrase", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("other code block", TextType.CODE),
            TextNode(" phrase", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_split_node_starting_with_delimiter(self):
        node = TextNode("`code block` with additional text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" with additional text", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_return_non_text_nodes_without_changes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        actual = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is a bold node", TextType.BOLD)
        ]
        self.assertEqual(actual, expected)

    def test_raise_exception_if_no_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "text contains unmatched delimiter: '`'")

class ExtractMarkdownImagesShould(unittest.TestCase):
    def test_extract_valid_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(actual, expected)

    def test_not_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_images(text)
        self.assertEqual(actual, [])

class ExtractMarkdownLinksShould(unittest.TestCase):
    def test_extract_valid_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(actual, expected)

    def test_not_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_links(text)
        self.assertEqual(actual, [])

class SplitNodesLinkShould(unittest.TestCase):
    def test_split_text_into_text_nodes_list(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) for reference.",
            TextType.TEXT,
        )
        actual = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" for reference.", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_ignore_non_text_nodes(self):
        bold_node = TextNode("bold text [foo](bar)", TextType.BOLD)
        link_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) for reference.",
            TextType.TEXT,
        )
        actual = split_nodes_link([bold_node, link_node])
        expected = [
            TextNode("bold text [foo](bar)", TextType.BOLD),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" for reference.", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_not_return_empty_strings(self):
        node = TextNode("[foo](https://bar.baz)", TextType.TEXT)
        actual = split_nodes_link([node])
        expected = [TextNode("foo", TextType.LINK, "https://bar.baz")]
        self.assertEqual(actual, expected)

class SplitNodesImageShould(unittest.TestCase):
    def test_split_text_into_text_nodes_list(self):
        node = TextNode(
            "This is text with an image ![image one](https://foo.bar) and another image ![image two](https://baz.qux) for reference.",
            TextType.TEXT,
        )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("image one", TextType.IMAGE, "https://foo.bar"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("image two", TextType.IMAGE, "https://baz.qux"),
            TextNode(" for reference.", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

class TextToTextNodesShould(unittest.TestCase):
    def test_return_text_nodes_from_given_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(actual, expected)

class MarkDownToBlocksShould(unittest.TestCase):
    def test_split_markdown_into_blocks(self):
        markdown = "# This is a heading   \n \n" + \
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.   \n" + \
            "  \n \n" + \
            "* This is the first list item in a list block\n" + \
            "* This is a list item\n" + \
            "* This is another list item   " + \
            "\n\n\n"
        actual = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" +
            "* This is a list item\n" +
            "* This is another list item"
        ]
        self.assertEqual(actual, expected)

class BlockToBlockTypeShould(unittest.TestCase):
    def test_convert_headings(self):
        blocks = [
            "# heading 1",
            "##  heading 2",
            "### heading 3",
            "#### heading 4",
            "##### heading 5",
            "###### heading 6",
            "####### normal paragraph",
            "#normal paragraph"
        ]
        expected = [
            BlockType.H1,
            BlockType.H2,
            BlockType.H3,
            BlockType.H4,
            BlockType.H5,
            BlockType.H6,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH
        ]
        for i in range(0, len(blocks)):
            actual = block_to_block_type(blocks[i])
            self.assertEqual(actual, expected[i])

    def test_convert_code_blocks(self):
        blocks = [
            "```code block```",
            "```\ncode block\n```",
            "```normal paragraph"
        ]
        expected = [
            BlockType.CODE,
            BlockType.CODE,
            BlockType.PARAGRAPH
        ]
        for i in range(0, len(blocks)):
            actual = block_to_block_type(blocks[i])
            self.assertEqual(actual, expected[i])

    def test_convert_quote_blocks(self):
        blocks = [
            ">quote block",
            ">multi-line\n>quote block",
            ">multi-line\nparagraph"
        ]
        expected = [
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.PARAGRAPH
        ]
        for i in range(0, len(blocks)):
            actual = block_to_block_type(blocks[i])
            self.assertEqual(actual, expected[i])

    def test_convert_unordered_list(self):
        blocks = [
            "* list item",
            "- list item",
            "* list item\n- list item 2",
            "- paragraph\ntext",
            "*paragraph text",
            "-paragraph text"
        ]
        expected = [
            BlockType.UNORDERED_LIST,
            BlockType.UNORDERED_LIST,
            BlockType.UNORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH
        ]
        for i in range(0, len(blocks)):
            actual = block_to_block_type(blocks[i])
            self.assertEqual(actual, expected[i])

    def test_convert_ordered_list(self):
        blocks = [
            "1. item 1\n2. item 2\n3. item 3",
            "2. item 1\n3. item 2",
            "1. item 1\n3. item 2",
            "1.item 1"
        ]
        expected = [
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH
        ]
        for i in range(0, len(blocks)):
            actual = block_to_block_type(blocks[i])
            self.assertEqual(actual, expected[i])
