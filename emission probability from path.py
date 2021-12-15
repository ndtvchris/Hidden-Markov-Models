#!/usr/bin/env python
# coding: utf-8

# # CLASS PROBFROMPATH
# ---
# This class computes the probability of emitting a certain sequence given a path of states. The algorithm functions by finding the indices of every state in the path, and then matching them up to the emission probability at that state.
# 
# ### FUNCTIONS
# 
#     init - class constructor
#     findStates - finds indices of a given pattern
#     findProb - finds probability of an emission string given a path of states
#     

# In[13]:


class probFromPath:
    '''
    Class for finding probability of emitting a sequence given a path of states
    '''

    def __init__(self, infile):
        '''
        Class constructor
        
        Parameters
            infile - file to read in
            
        Attributes
            self.observables - observables
            self.path - path of states taken
            self.AX/AY/AZ/BX/BY/BZ - transmission probabilities at each state
        '''

        with open(infile) as file:
            holder = []
            self.observables = file.readline().rstrip()
            self.stateEmission = {}
            for line in file:
                checker = line.split()
                
                # parses in emission probabilities and sets them to member values
                try:
                    if checker[0].rstrip().isalpha() and len(checker[0]) == len(self.observables):
                        self.path = checker[0]
                    elif checker[0] not in self.observables and checker[1].find('.') == -1:
                        self.states = checker
                    elif checker[0] in self.observables and checker[1] in self.observables:
                        self.emissions = checker
                    elif checker[0].isalpha and checker[1].find('.') != -1:
                        [holder.append(checker[i]) for i in range(1, len(checker))]
                        self.stateEmission[checker[0]] = holder
                        holder = []
                    
                except IndexError:
                    continue

    def findStates(self, pattern):
        '''
        Function for finding indices of a pattern
        
        Parameters
            pattern - pattern to look for
            
        Returns
            A generator object containing the indices at where the pattern is found
        '''
        i = self.path.find(pattern)
        while i != -1:
            yield i
            i = self.path.find(pattern, i + 1)

    def findProb(self):
        '''
        Function that calculates the probability of emitting a sequence given the path
        '''
        # initialization of local variables
        pathTotal = 1.0
        indices = set()
        
        # list comprehension to initialize list of indices
        for state in self.states:
            
            [indices.add(i) for i in self.findStates(state)]
            #at each found state, see what's emitted
            for x in range(len(self.observables)):
                if x in indices:
                    indec = self.observables[x]
                    proba =  float(self.stateEmission[state][self.emissions.index(indec)])
                    pathTotal *= proba
            indices.clear()
        

       
        
        with open('p20out.txt', 'w') as out:
            out.write(str(pathTotal))
        


pp = probFromPath('20.txt')
pp.findProb()
print(pp.emissions)
print(pp.states)
print(pp.stateEmission)


# # MAIN
# ---
# This is the main function for initialization and execution

# In[2]:


def main(infile):
    '''
    This is the main function. I make an object that performs the calculation.
    '''

    pfp = probFromPath(infile)
    pfp.findProb()
    
if __name__ == '__main__':
    main('20.txt')
    


# # INSPECTIONS
# ---
# ### Richard
# - expand init docstring to include list of class attributes as its hard to see how many there are **TAKEN**
