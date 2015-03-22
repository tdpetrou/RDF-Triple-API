'''
Created on Mar 19, 2015

@author: TPetrou
'''

from nltk.parse import stanford
import os, sys
import operator
# java_path = r"C:\Program Files\Java\jdk1.8.0_31\bin\java.exe"
# os.environ['JAVAHOME'] = java_path
os.environ['STANFORD_PARSER'] = r'/users/ted/stanford nlp/stanford-parser-full-2015-01-30'
os.environ['STANFORD_MODELS'] = r'/users/ted/stanford nlp/stanford-parser-full-2015-01-30'



class RDF_Triple():
    
    def __init__(self):
        self.clear_data()
        
    
    def clear_data(self):
        self.parser = stanford.StanfordParser(model_path=r"/users/ted/stanford nlp/stanford-parser-full-2015-01-30/stanford-parser-3.5.1-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        self.first_NP = ''
        self.first_VP = ''
        self.subject = ''
        self.predicate = ''
        self.object = ''
        
        self.predicate_parent = None
        self.predicate_depth = 0
        self.predicate_list = [] 
        self.predicate_sibling_trees = []


    def find_NP(self, t):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label() == 'NP':
                if self.first_NP == '': 
                    self.first_NP = t
            elif t.label() == 'VP':
                if self.first_VP == '':
                    self.first_VP = t
            for child in t:
                self.find_NP(child)

    
    def find_subject(self, t):
        if self.subject != '':
            return
        try:
            t.label()
        except AttributeError:
#             print 'here', t
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN':
                if self.subject == '': 
                    self.subject = t.leaves()[0]
            else:
#                 print '(', t.label()
                for child in t:
                    self.find_subject(child)
#                 print ') end'
    
    
    def find_predicate(self, t, parent=None, depth=0):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            if t.label()[:2] == 'VB':
                self.predicate_list.append((t.leaves()[0], depth, parent))
                
            for child in t:
#                 if t.label() != 'S':
#                     '''  
#                     need to check that this makes sense. 
#                     Seems correct to not look into new sentences.
#                     More likely to happen in long sentences
#                     '''
                self.find_predicate(child, parent=t, depth=depth+1)
                
                
    def find_deepest_predicate(self):
#         print self.predicate_list
        return max(self.predicate_list, key=operator.itemgetter(1))


    def print_tree(self, t, depth=0):
        try:
            t.label()
        except AttributeError:
            print t, 'depth', depth
            pass
        else:
            # Now we know that t.node is defined
            print '(', t.label() , 'depth', depth
            for child in t:
                self.print_tree(child, depth+1)
            print ') '
    
    
    def find_object(self):
        for t in self.predicate_parent:
            if self.object == '':
                self.find_object_NP_PP(t, t.label())
           
    
    def find_object_NP_PP(self, t, phrase_type):
        '''
        finds the object given its a NP or PP or ADJP
        '''
        if self.object != '':
            return
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN' and phrase_type in ['NP', 'PP']:
                if self.object == '': 
                    self.object = t.leaves()[0]
            elif t.label()[:2] == 'JJ' and phrase_type == 'ADJP':
                if self.object == '': 
                    self.object = t.leaves()[0]
            else:
                for child in t:
                    self.find_object_NP_PP(child, phrase_type)
                    
                    
    def main(self, sentence):
        self.clear_data()
        test_tree = self.parser.raw_parse(sentence)
        self.find_NP(test_tree[0])
        self.find_subject(self.first_NP)
        self.find_predicate(self.first_VP)
        if self.subject == '':
            self.subject = self.first_NP.leaves()[0]
        self.predicate, self.predicate_depth, self.predicate_parent = self.find_deepest_predicate()
#         print self.subject
#         print self.predicate
#         print 'pred parent is', self.predicate_parent
        
#         self.find_predicate_siblings(self.predicate_parent)
#         for t in self.predicate_sibling_trees:
#         for t in self.predicate_parent:
#             print "\n"
#             print t.label()
#             print t 
#             print "\n"
        self.find_object()
#         print self.object
        
        

if __name__ == '__main__':
    try:
        sentence = sys.argv[1]
    except IndexError:
        print "Enter in your sentence"
        sentence = 'A rare black squirrel has become a regular visitor to a suburban garden'
        print "Heres an example"
        print sentence

    # sentence = 'The boy dunked the basketball'
#     sentence = 'They also made the substance able to last longer in the bloodstream, which led to more stable blood sugar levels and less frequent injections.'
#     sentence = 'The main parts of this Department are grimacing masks, terracotta statues and stelae of major interest for the Semitic epigraphy, the stele of the priest and the child being the most famous.'
    rdf = RDF_Triple()
    rdf.main(sentence)
    print (rdf.subject, rdf.predicate, rdf.object)