import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_should_raise_value_error_if_no_value(self):
        leaf = LeafNode("tag", None)
        self.assertRaises(ValueError, lambda: leaf.to_html())

    def test_to_html_should_return_value_if_no_tag(self):
        value ="foo"
        leaf = LeafNode(None, value)
        actual = leaf.to_html()
        self.assertEqual(actual, value)

    def test_to_html_should_render_html_with_attributes_if_props(self):
        leaf = LeafNode("tag", "value", { "foo": "bar", "baz": "qux" })
        actual = leaf.to_html()
        expected = "<tag foo=\"bar\" baz=\"qux\">value</tag>"
        self.assertEqual(actual, expected)

    def test_to_html_should_render_html_without_attributes_if_no_props(self):
        leaf = LeafNode("tag", "value")
        actual = leaf.to_html()
        expected = "<tag>value</tag>"
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
