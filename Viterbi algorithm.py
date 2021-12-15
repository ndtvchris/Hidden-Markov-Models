#!/usr/bin/env python
# coding: utf-8

# # CLASS VITERBI
# ---
# This class is an implementation of the Viterbi algorithm. This implementation scores the max of two probabilities at each state for each emission and uses that to move forward in the calculations.
# 
# ### FUNCTIONS
# 
#     init - class constructor
#     parseFile - parses file to yield relevant data
#     pathTrace - performs the Viterbi algorithm to find largest probability of any path that can emit the given                   sequence
#     backTrace - backtracks to find the best sequence of states that emits the observable

# In[1]:


class viterbi:
    '''
    Class for performing the Viterbi algorithm
    '''

    def __init__(self, infile):
        '''
        Class constructor
        
        Parameters
            infile - file to read from
        '''
        self.stateEmission = {}  # holds emissions probs for each state
        self.stateTransmission = {}  # holds transmission probs for each state
        self.emissions = []  # emissions organized by index based on data
        self.transmissions = []  # transmissions organized by index based on data
        self.endState = ''  # from where the end node got the best prob
        self.observables = '' # string of observables
        self.prevProbs = {} # holds previous probabilities for next calculation
        self.bestParent = {} # records from which 'parent' state the best probability came from
        self.parseFile(infile)  

    def parseFile(self, infile):
        '''
        This function parses in the data file to obtain usable data
        
        Parameters
            infile - file to parse from
        '''
        holdList = []
        with open(infile) as file:
            self.observables = file.readline().rstrip()
            
            for line in file:
                checker = line.split()
                try:
                    # if the first letter read is in observables and not yet in emissions, put them in
                    if self.observables.find(checker[0]) != -1 and checker[0] not in self.emissions:
                        [self.emissions.append(checker[i]) for i in range(len(checker))]
                    # 1st instance of letter followed by a decimal means transmission
                    elif checker[0].isalpha() and checker[1].find('.') != -1 and len(self.stateTransmission) < len(self.transmissions):
                        [holdList.append(float(checker[i])) for i in range(1, len(checker))]
                        self.stateTransmission[checker[0]] = holdList
                        holdList = []
                    # 2nd instance of letter followed by decimal and transmits full means that it's emissions
                    elif checker[0].isalpha() and checker[1].find('.') != -1 and len(self.stateEmission) < len(self.transmissions):
                        [holdList.append(float(checker[i])) for i in range(1, len(checker))]
                        self.stateEmission[checker[0]] = holdList
                        holdList = []
                        # reads in for transmission possibilities
                    elif checker[0].isalpha() and checker[0] not in self.emissions and checker[0] not in self.transmissions:
                        [self.transmissions.append(checker[i]) for i in range(len(checker))]
                        self.transmissions = sorted(set(self.transmissions))

                except IndexError:
                    continue
            
            # dict comprehension for initializing these dictionaries
            self.prevProbs = {k: 0.5 for k in self.transmissions}
            self.bestParent = {k: [] for k in self.transmissions}

    def pathTrace(self):
        '''
        This function finds the best sequence of states that can emit a given observable sequence
        '''
        maxProb = 0
        newProbs = {k : 0 for k in self.transmissions}
        
        # for every emission index
        for index in range(len(self.observables)):
            hold = 0
            
            # if it's the first emission, must do a different calculation
            if index == 0:
                for state in self.transmissions:
                    emitProb = self.stateEmission[state][self.emissions.index(self.observables[index])]
                    prevProb = self.prevProbs[state]
                    self.prevProbs[state] = emitProb * prevProb
            
            # otherwise it's all the same
            else:
                
                currentBest = '' # current best parent state
                
                #calculates probabilities for each state at a given emission index
                for state in self.transmissions:
                    total = 0  
                    emitProb = self.stateEmission[state][self.emissions.index(self.observables[index])]
                    
                    # calculates total probability using previous state and transmission probabilities
                    for key in self.stateTransmission:

                        prevProb = self.prevProbs[key]
                        transProb = self.stateTransmission[key][self.transmissions.index(state)]
                        hold = emitProb * prevProb * transProb
                        
                        #if the current calculated probability is the largest so far, update the currentBest
                        if hold > total:
                            total = hold
                            newProbs[state] = total
                            currentBest = key
                    self.bestParent[state].append(currentBest)
                    
                # updates the previous probabilities for next set of calculations
                for key in self.prevProbs:
                    self.prevProbs[key] = newProbs[key]
                newProbs = {k: 0 for k in self.transmissions}
                
                # finds the ending state
                if index == len(self.observables) - 1:
                    for state in self.prevProbs:

                        if self.prevProbs[state] > maxProb:
                            maxProb = self.prevProbs[state]
                            self.endState = state

                            
    def backTrace(self):
        '''
        This function synthesizes the path by backtracking
        '''
        writeList = []
        writeList.append(self.endState)  
        current = self.endState
        # from the end state, steps backwards and chooses the proper state to insert
        for x in range(len(self.bestParent[self.endState]) - 1, -1, -1):
            writeList.insert(0, self.bestParent[current][x])
            current = self.bestParent[current][x]

        with open('p21out.txt', 'w') as out:
            out.write(''.join(writeList))




# # MAIN
# ---
# This is the main function for instantiation and execution

# In[2]:


def main(infile):   
    '''
    This is the main function. I make an object then do viterbi.
    '''
    v = viterbi(infile)
    v.pathTrace()
    v.backTrace()
    
    
if __name__ == '__main__':
    main('rosalind_ba10c_847_2_dataset.txt')


# # INSPECTIONS
# Immaad Mir
# - The way you parse your file is not the most readable code
# - Other then your parse file method everything is super easy to read and follow
# 
# Chris Condon
# - Agreed that file reader is not the friendliest, but understandable since the infile format is a nightmare as well.
# - Good use of dictionaries/dict comprehensions to store states
# - Perhaps using the max() function to find the highest probability for each timepoint could be a bit more efficient? **WILL CONSIDER**
# 
# Quin Lamothe
# - Might not need to do a dict comprehension to zero out values **CONSIDERED**
# 
# Richard
# - mention that finalState is the state with max prob at the end **TAKEN**
