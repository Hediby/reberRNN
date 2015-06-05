import numpy as np

class ReberGrammar(object):
    def __init__(self):
        self.chars='BTSXPVE.'

        graph = [[(1,5),('T','P'), (1, 1)] , 
                 [(1,2),('S','X'), (5, 1)],
                 [(3,5),('S','X'), (1, 5)],
                 [(6,),('E',), (1,)],
                 [(3,2),('V','P'), (1, 5)],
                 [(4,5),('V','T'), (1, 5) ],
                 [(7,),('.',), (1,) ]
                ]

        self.graph = [(o, l, np.array(w)/sum(map(float, w))) for o, l, w in graph]
        
    def generateSequences(self, minLength):
        while True:
            inchars = ['B']
            node = 0
            outchars = []    
            while node != 7:
                outnodes, letters, weights = self.graph[node]
                i = np.random.choice(range(len(outnodes)), p=weights)
                i = int(i)
                inchars.append(letters[i])
                outchars.append(letters)
                node = outnodes[i]
            if len(inchars) > minLength:
                return inchars, outchars
            
    def in_grammar(self, word):
        if word[0] != 'B':
            return False
        node = 0    
        for c in word[1:]:
            try:
                outnodes, letters, _ = self.graph[node]
            except:
                return False
            try:
                node = outnodes[letters.index(c)]
            except ValueError: # using exceptions for flow control in python is common
                return False
        return True    
    
    def get_char_one_hot(self,char):
        char_oh = np.zeros(8)
        for c in char:
            char_oh[self.chars.find(c)] = 1.
        return [char_oh]
    
    def sequenceToWord(self, sequence):
        """
        converts a sequence (one-hot) in a reber string
        """
        reberString = ''
        for s in sequence:
            index = np.where(s==1.)[0][0]
            reberString += self.chars[index]
        return reberString
    
    
    def get_one_example(self, minLength):
        inchars, outchars = self.generateSequences(minLength)
        inseq = []
        outseq= []
        for i,o in zip(inchars, outchars): 
            inpt = np.zeros(8)
            inpt[self.chars.find(i)] = 1.     
            outpt = np.zeros(8)
            for oo in o:
                outpt[self.chars.find(oo)] = 1.
            inseq.append(inpt)
            outseq.append(outpt)
        return inseq, outseq

    def get_n_examples(self, n, minLength=10):
        examples = []
        for i in xrange(n):
            examples.append(self.get_one_example(minLength))
        return examples

class EmbeddedReberGrammar():
    def __init__(self, grammar, emb_chars):

        self.grammar = grammar
        self.emb_chars = emb_chars
        self.graph = self.grammar.graph
        self.chars=self.grammar.chars
        self.sequenceToWord = self.grammar.sequenceToWord
        self.get_char_one_hot = self.grammar.get_char_one_hot
        
    def generateSequences(self, minLength):
        inchars, outchars = self.grammar.generateSequences(minLength)
        inchars, outchars = inchars[:-1], outchars[:-1]
        outter = np.random.choice(['T','P'])
        inchars = ['B'] + [outter] + inchars + [outter] + ['E','.']
        outchars = [('T', 'P')] + [('B',)] + outchars + [(outter,)] + [('E',), ('.',)]
        return inchars, outchars

    def get_one_example(self,minLength):
        inchars, outchars = self.generateSequences(minLength)
        inseq = []
        outseq= []
        for i,o in zip(inchars, outchars): 
            inpt = np.zeros(8)
            inpt[self.chars.find(i)] = 1.     
            outpt = np.zeros(8)
            for oo in o:
                outpt[self.chars.find(oo)] = 1.
            inseq.append(inpt)
            outseq.append(outpt)
        return inseq, outseq

    def get_n_examples(self, n, minLength=10):
        examples = []
        for i in xrange(n):
            examples.append(self.get_one_example(minLength))
        return examples
    
    def in_grammar(self,word):
        try:
            return word[0]=='B' and word[-1]=='.' and word[1] == word[-3] and word[1] in self.emb_chars and self.grammar.in_grammar(word[2:-3])
        except: 
            return False