import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://foo.bar")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr_without_url(self):
        text = "This is a text node"
        text_type = TextType.BOLD
        node = TextNode(text, text_type)
        expected = f"TextNode({text}, {text_type.value}, None)"
        self.assertEqual(str(node), expected)

    def test_repr_with_url(self):
        text = "This is a text node"
        text_type = TextType.BOLD
        url = "https://foo.bar"
        node = TextNode(text, text_type, url)
        expected = f"TextNode({text}, {text_type.value}, {url})"
        self.assertEqual(str(node), expected)

    def test_text_node_to_html_node_should_raise_exception_given_invalid_text_type(self):
        node = TextNode("foo", "bar")
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "text node must have a valid text type")

    def test_text_node_to_html_node_should_handle_text_type(self):
        node = TextNode("foo", TextType.NORMAL)
        actual = text_node_to_html_node(node)
        expected = LeafNode(None, "foo")
        self.assertEqual(str(actual), str(expected))

    def test_text_node_to_html_node_should_handle_bold_type(self):
        node = TextNode("foo", TextType.BOLD)
        actual = text_node_to_html_node(node)
        expected = LeafNode("b", "foo")
        self.assertEqual(str(actual), str(expected))

    def test_text_node_to_html_node_should_handle_italic_type(self):
        node = TextNode("foo", TextType.ITALIC)
        actual = text_node_to_html_node(node)
        expected = LeafNode("i", "foo")
        self.assertEqual(str(actual), str(expected))

    def test_text_node_to_html_node_should_handle_code_type(self):
        node = TextNode("foo", TextType.CODE)
        actual = text_node_to_html_node(node)
        expected = LeafNode("code", "foo")
        self.assertEqual(str(actual), str(expected))

    def test_text_node_to_html_node_should_handle_link_type(self):
        node = TextNode("foo", TextType.LINK, "bar")
        actual = text_node_to_html_node(node)
        expected = LeafNode("a", "foo", {"href": "bar"})
        self.assertEqual(str(actual), str(expected))

    def test_text_node_to_html_node_should_handle_image_type(self):
        node = TextNode("foo", TextType.IMAGE, "bar")
        actual = text_node_to_html_node(node)
        expected = LeafNode("img", "", {"src": "bar", "alt": "foo"})
        self.assertEqual(str(actual), str(expected))

if __name__ == "__main__":
    unittest.main()
