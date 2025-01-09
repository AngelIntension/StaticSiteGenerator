import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {}
        href = "href"
        url = "https://foo.bar"
        props[href] = url
        target = "target"
        blank = "_blank"
        props[target] = blank
        node = HTMLNode(props = props)

        actual = node.props_to_html()

        expected = f"{href}=\"{url}\" {target}=\"{blank}\""
        self.assertEqual(actual, expected)

    def test_repr(self):
        tag = "p"
        value = "foo"
        children = None
        props = { "href": "https://foo.bar", "target": "_blank" }
        node = HTMLNode(tag, value, children, props)

        actual = str(node)

        expected = f"HTMLNode({tag}, {value}, {children}, {props})"
        self.assertEqual(actual, expected)

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, lambda: node.to_html())

if __name__ == "__main__":
    unittest.main()
