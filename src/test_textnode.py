import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
