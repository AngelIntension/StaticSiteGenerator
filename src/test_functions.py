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
