import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter

class TestFunctions(unittest.TestCase):
    def test_split_nodes_delimiter_should_split_single_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_split_nodes_delimiter_should_split_multiple_nodes(self):
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

    def test_split_nodes_delimiter_should_split_node_with_multiple_delimited_strings(self):
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

    def test_split_nodes_delimiter_should_split_node_starting_with_delimiter(self):
        node = TextNode("`code block` with additional text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" with additional text", TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_split_nodes_delimiter_should_return_non_text_nodes_without_changes(self):
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

    def test_split_nodes_delimiter_should_raise_exception_if_no_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "text contains unmatched delimiter: '`'")
