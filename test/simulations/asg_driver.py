#! /usr/bin/env python

import string;
import csv;
import xml.etree.ElementTree as ET;
import sys

from ASGsim import *;

root = sys.argv[1]
num_leafs = int(sys.argv[2])
seed = int(sys.argv[3])

whens = [5000];
how_manys = [num_leafs];

# first 3 parameters are: resample_rate, selection_rate, mutation_rate
myASG = ASG(0.00001, 0.01, 0.0001, whens, how_manys, growth_rate = 0.005);

print("Building ASG...");
myASG.buildASG(random_seed=seed);
print("Assigning types...");
myASG.assign_types();
print("Marking genealogy...");
myASG.mark_true_genealogy();
    
# myASG.Graphviz("GV_test.png");
print("Creating Newick tree...");
annot, Newick = myASG.FigTree();

# Write the annotations to FT_test.tsv
f = open(root+".tsv", "wb");
annot_writer = csv.writer(f, delimiter='\t');
annot_writer.writerow(("leaf", "taxa", "type", "mut", "time"));
annot_writer.writerows(annot);
f.close();

# Write the tree out
f = open(root+".nwk", "wb");
f.write(Newick);
f.close();

# Write out the PhyloXML representation
#pxml = myASG.PhyloXML();

#pxml.write("PXML_test.xml");

# Write out the NeXML representation
#nxml = myASG.NeXML();
#nxml.write("NeXML_test.xml");
