from tree import tree as tree
from lxml import etree
import requests
from lxml import html
import json
import sys
import csv
import logging
import time

class NET(object):

    def __init__(self, url, source = "web"):

        f = open("output.csv", "wb")
        self.writer = csv.writer(f)
        self.tree = tree()
        self.full_matching = {} #helpful to create table
        
        #log configuration
        logging.basicConfig(filename = 'log.log', level = logging.INFO)

        if source == "web":
            try:
                page = requests.get(url)
            except requests.exceptions.RequestException as e:
                print e
                sys.exit(1)
            self.dom_tree = html.fromstring(page.content)
        else:
            self.dom_tree = etree.parse(url).getroot()

        print "======================Dom Tree========================"
        print self.dom_tree.getchildren()
        print "======================================================"
        print "\n\n"

        #TODO add other relevant logging info
        logging.info("url {0}".format(url))
        logging.info("dom tree size {0}".format(self.tree.get_size(self.dom_tree)))

    def net(self, Threshold=3):
        start = time.clock()
        self.traverse(self.dom_tree, Threshold)
        print "==================== Tree Travesal Time =============="
        print time.clock() - start
        print "======================================================"
        print "\n\n"


    #TODO: Use different heuristics, as mentioned in paper or find emperically
    def traverse(self, root, Threshold=25):

        if self.tree.get_depth(root) >= 3:
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
                print "------------TABLE-----------------"
                print table
                
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
                    if self.tree.tree_match(childF, childR, matched) >= Threshold and track_matches[childR]!=1:
                           #for matching in matched:
                           #     if matching[0].text.encode('utf-8') is not None and matching[1].text.encode('utf-8') is not None and matching[0].text.encode('utf-8').isspace() is False and matching[1].text.encode('utf-8').isspace () is False:
                           #         print "First item of matching", matching[0].text.encode('utf-8').strip(), "second item of matching", matching[1].text.encode('utf-8').strip()
                           # Keep track of multiple alignments of a node.
                           # matched has matching of only two trees
                           self.align_and_link(matched)
                           # After matching mark the nodes matched
                           track_matches[childR] = 1
                           track_matches[childF] = 1

    def print_dict(self, arg):
        for node in arg:
            print node.tag
            print "  "
        print "\n\n"


    def align_and_link(self, matching):
        
        self.print_dict(self.full_matching)
        print self.full_matching

        for matched in matching:
            if self.full_matching.has_key(matched[0]) is True:
                self.full_matching[matched[0]].append(matched[1])
            else:
                self.full_matching[matched[0]] = []
                self.full_matching[matched[0]].append(matched[1])

        self.print_dict(self.full_matching)
        

#TODO url don't work for some special character . eg., &, you need to input as \&
# command line argument sequence url, source (only specify in case of web otherwise it's fine)

if __name__ == "__main__":
    
    net = NET('file:////home/mitesh/Documents/web data extraction/pynet/tests/resources/test.html', source="local")

    """
    print sys.argv
    url, source = sys.argv[1:]
    print "url:",url, " source:",source
    net = NET(url, source)
    """

    net.net()
    print net.full_matching

