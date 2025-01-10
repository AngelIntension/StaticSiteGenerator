import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_should_raise_value_error_if_no_tag(self):
        parent = ParentNode(None, None)
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "parent node must have a tag")

    def test_to_html_should_raise_value_error_if_no_children(self):
        parent = ParentNode("tag", None)
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "parent node must have a child")

    def test_to_html_should_return_html_of_parent_and_children_1(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text")
            ]
        )
        actual = parent.to_html()
        expected = "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>"
        self.assertEqual(actual, expected)

    def test_to_html_should_return_html_of_parent_and_children_2(self):
        child = ParentNode(
            "ul",
            [
                LeafNode("li", "list item")
            ]
        )
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text"),
                child
            ]
        )
        actual = parent.to_html()
        expected = "<p><b>bold text</b>normal text<i>italic text</i>normal text<ul><li>list item</li></ul></p>"
        self.assertEqual(actual, expected)
