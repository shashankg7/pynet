from pynet.net import tree
from lxml import etree
import unittest

#TODO create multiple trees and their answer.
s1 = """<root>
            <b>
                <d></d>
                <e></e>
            </b>
            <c>
                <f></f>
            </c>
            <b>
                <e></e>
                <d></d>
            </b>
            <c>
                <g>
                    <h></h>
                    <i></i>
                    <j></j>
                </g>
            </c>
        </root>
"""

s2 = """<root>
            <b>
                <d></d>
                <e></e>
            </b>
            <c>
                <g>
                    <h></h>
                </g>
                <f></f>
            </c>
        </root>
"""
ans12 = ["root", "b", "d", "e", "c", "f", "g", "h"]

# Space between only open-closed tag. #readability
s3 = """<c><b><a> </a></b></c>"""
s4 = """<c><a> </a><b> </b></c> """
ans34 = ["c", "a"]
ans13 = []
ans14 = []

class TestTreeMatch(unittest.TestCase):

    def test_tree_match(self):
        tree1 = etree.XML(s1)
        tree2 = etree.XML(s2)
        t = tree()
        ans = ["root", "b", "d", "e", "c", "f", "g", "h"]
        ret = []
        self.assertEquals(7, t.tree_match(tree1, tree2, ret))
        for tags, a in zip(ret, ans):
            self.assertEqual( tags[0].tag, a)

if __name__ == "__main__":
    unittest.main()
