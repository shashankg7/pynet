from lxml import etree
from StringIO import StringIO
from tree import tree as tr
import requests
from lxml import html
import json
import sys
import csv


class NET(object):
    def __init__(self, url, source= "web"):
        if source == "web":
            page = requests.get(url)
            self.tree = html.fromstring(page.content)
            self.tre = tr()
            self.full_matching = {}
            #print self.tre.get_size(self.tree)
            f = open("output.csv", "wb")
            self.writer = csv.writer(f)

        else:
            self.tree = etree.parse(url).getroot()
            self.tre = tr()
            self.full_matching = {}
            f = open("output.csv", "wb")
            self.writer = csv.writer(f)


    def net(self, Threshold=25):
        self.traverse(self.tree, Threshold)


    def traverse(self, root, Threshold=25):
        # Using simple heuristic for base condition
        # TO-DO: Use different heuristics, as mentioned in paper or find
        #        emperically
        if self.tre.get_depth(root) >= 3:
            for child in root.getchildren():
                self.traverse(child, Threshold)
            self.full_matching = {}
            self.match(root, Threshold)
            # Create a table structure to write in a file the data
            table = []
            for k,v in self.full_matching.iteritems():
                if len(v)!=0:
                    v.append(k)
                    temp = []
                    if v is not None:
                        for e in reversed(v):
                            if e.text and e.text.strip():
                                   print e.text.strip()
                                   temp.append(e.text.encode('utf-8').strip())
                    if len(temp)!=0:
                        table.append(temp)
            if len(table)!=0:
                #print zip(*table)
                # It is not a balanced structure(every list is of different size) so creating a balance
                N = max(map(lambda x:len(x), table))
                print N, len(table)
                final_output = [['']*N]*len(table)
                for i in range(len(table)):
                    for j in range(len(table[i])):
                        final_output[i] = table[i][j]
                #print final_output
                self.writer.writerows(zip(*table))


    def match(self, node, Threshold):
        matched = []
        # Boolean vector to keep track of which nodes are matched to avoid
        # duplicate matching
        track_matches = {}
        children = node.getchildren()
        for child in children:
            track_matches[child] = 0
        for childF in children:
            for childR in children:
                if childF != childR:
                    # Keep matching of two trees
                    matched = []
                    if self.tre.tree_match(childF, childR, matched) >= Threshold and track_matches[childR]!=1:
                           #for matching in matched:
                           #     if matching[0].text.encode('utf-8') is not None and matching[1].text.encode('utf-8') is not None and matching[0].text.encode('utf-8').isspace() is False and matching[1].text.encode('utf-8').isspace () is False:
                           #         print "First item of matching", matching[0].text.encode('utf-8').strip(), "second item of matching", matching[1].text.encode('utf-8').strip()
                           # Keep track of multiple alignments of a node.
                           # matched has matching of only two trees
                           self.align_and_link(matched)
                           # After matching mark the nodes matched
                           track_matches[childR] = 1
                           track_matches[childF] = 1


    def align_and_link(self, matching):
        for matched in matching:
            if self.full_matching.has_key(matched[0]) is True:
                self.full_matching[matched[0]].append(matched[1])
            else:
                self.full_matching[matched[0]] = []
                self.full_matching[matched[0]].append(matched[1])

if __name__ == "__main__":
    # For testing passing local html file. Local or remote html controlled by
    # source argument
    #net = NET('file:///home/shashank/Research/Auto_Data_Extrct/net/tests/test.html', source="local")
    url, source = sys.argv[1:]
    print url, source
    net = NET(url, source)
    net.net()


