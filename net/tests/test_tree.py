from net.tree import tree_match
from lxml import etree
import unittest

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

class TestTreeMatch(unittest.TestCase):

    def test_tree_match(self):
        tree1 = etree.XML(s1)
        tree2 = etree.XML(s2)
        self.assertEquals(7, tree_match(tree1, tree2))

