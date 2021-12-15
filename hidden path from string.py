#!/usr/bin/env python
# coding: utf-8

# # CLASS HIDDENPATH
# ---
# This class computes the probability of traversing along a certain path. The algorithm finds the total number of state changes and uses it as an exponent along with the given transmission probabilities.
# 
# ### FUNCTIONS
# 
#     init - class constructor
#     findTwos - finds all indices of where the state change occurs
#     pathCalc - finds the overall probability for the given path

# In[1]:


import itertools


class hiddenPath:

    def __init__(self, infile):
        '''
        Class constructor

        Parameters
            infile - file to read from

        Attributes
            self.path - observables
            self.AA/AB/BA/BB - transmission probabilities between states
        '''
        holdList = []
        self.stateTransmissions = {}
        self.totalProb = 1.0
        with open(infile) as file:
            self.path = file.readline().rstrip()

            for line in file:
                checker = line.split()
                # accounts for IndexErrors and tries to find the probabilities
                try:
                    # if the checker is a letter, read it in and store prob
                    if checker[0].isalpha and checker[1].find('.') == -1:
                        self.states = checker
                    elif checker[0].isalpha and checker[1].find('.') != -1:
                        [holdList.append(checker[i]) for i in range(1, len(checker))]
                        self.stateTransmissions[checker[0]] = holdList
                        holdList = []
                except IndexError:
                    continue

    def findTwos(self, pattern):
        '''
        This function looks for all instances of pattern

        Parameter
            pattern - pattern to find
        '''
        i = self.path.find(pattern)
        # returns a generator object to save memory
        while i != -1:
            yield i
            i = self.path.find(pattern, i + 1)

    def pathCalc(self):
        '''
        This function finds the probability for a given path
        '''
        combos = [''.join(w) for w in (itertools.product(self.states, repeat=2))]
        holder = []

        for combo in combos:
            # finds all instances of the 2mer
            [holder.append(i) for i in self.findTwos(combo)]
            # for each 2mer, get transmission prob
            tProb = self.stateTransmissions[combo[0]][self.states.index(combo[1])]
            self.totalProb *= float(tProb) ** len(holder)
            holder.clear()
        '''
        # finds total probabilities for each state change
        numAA = self.AA ** len([holder.append(i) for i in self.findTwos('AA')])
        holder.clear()
        numAB = self.AB ** len([holder.append(i) for i in self.findTwos('AB')])
        holder.clear()
        numBA = self.BA ** len([holder.append(i) for i in self.findTwos('BA')])
        holder.clear()
        numBB = self.BB ** len([holder.append(i) for i in self.findTwos('BB')])
        holder.clear()
        '''

        with open('p19out.txt', 'w') as out:
            out.write(str(self.totalProb * 1 / len(self.states)))







# # MAIN
# ---
# This is the main function for instantiation and execution

# In[2]:


def main(infile):
    '''
    This is the main function. I make an object then do the math.
    '''
    hp = hiddenPath(infile)
    hp.pathCalc()
    
if __name__ == '__main__':
    main('19.txt')


# # INSPECTIONS
# ---
# ### RICHARD
# - expand init docstring to mention all member values **TAKEN**
