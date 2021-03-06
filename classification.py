import numpy
import math
import pandas
import random

# These are suggested helper functions
# You can structure your code differently, but if you have
# trouble getting started, this might be a good starting point

# Create the decision tree recursively
def make_node(previous_ys, xs, ys, columns):
    # WARNING: lists are passed by reference in python
    # If you are planning to remove items, it's better 
    # to create a copy first

    #so basically this makes a copy of columns and saves it into local variable columns
    #so now any changes we make to columns won't change the thing that got passed in
    columns = columns[:]

    node = {}

    # First, check the three termination criteria:
    
    # If there are no rows (xs and ys are empty): 
    #      Return a node that classifies as the majority class of the parent

    #only checking if one is empty because if either one is empty, the other will be too
    if len(ys) == 0:
        node["type"] = "class"
        node["class"] = majority(previous_ys)
        return node

    # If all ys are the same:
    #      Return a node that classifies as that class 
    if (same(ys)):
        node["type"] = "class"
        node["class"] = ys[0]
        return node
    
    # If there are no more columns left:
    #      Return a node that classifies as the majority class of the ys

    if (len(columns) == 0):
        node["type"] = "class"
        node["class"] = majority(ys)
        return node

    # Otherwise:
    # Compute the entropy of the current ys 

    currentEntropy = getEntropy(ys)
    bestColumn = None
    bestEntropy = math.inf

    # For each column:
    #     Perform a split on the values in that column 
    #     Calculate the entropy of each of the pieces
    #     Compute the overall entropy as the weighted sum 
    #     The gain of the column is the difference of the entropy before
    #        the split, and this new overall entropy 

    for col in columns:
        #list comprehension + convert to set and then to list to remove dupes
        #the list comprehension sets values to every value that we care about in a specific column
        values = list(set(x[col] for x in xs))
        sumEntropy = 0
        for value in values:
            # use zip xs ys to make tuples out of xs and ys, then for each pair, check if x[col] is value and if it is, save it into y
            subys = [y for (x, y) in zip(xs, ys) if x[col] == value]
            sumEntropy += len(subys) / len(ys) * getEntropy(subys)

        if sumEntropy < bestEntropy: 
            bestColumn = col
        
    # Select the column with the highest gain, then:
    # Split the data along the column values and recursively call 
    #    make_node for each piece 
    # Create a split-node that splits on this column, and has the result 
    #    of the recursive calls as children.

    values = list(set(x[bestColumn] for x in xs))
    node["type"] = "split"
    node["split"] = bestColumn
    node["children"] = {}



    columns.remove(bestColumn)

    for value in values:
        subxs = [x for (x, y) in zip(xs, ys) if x[col] == value]
        subys = [y for (x, y) in zip(xs, ys) if x[col] == value]
        
        node["children"][value] = make_node(ys, subxs, subys, columns)

        #print(value)

    return node

    

    
    

# Determine if all values in a list are the same 
# Useful for the second basecase above
def same(values):
    if not values: return True
    # if there are values:
    # pick the first, check if all other are the same 

    firstValue = values[0]
    for value in values:
        if value != firstValue: return False
    return True
    


    
# Determine how often each value shows up 
# in a list; this is useful for the entropy
# but also to determine which values is the 
# most common
def getCounts(values):

    #declare an empty dict called frequencies
    counts = {}
    for value in values:
        if value in counts:
            counts[value] = counts[value] + 1
        else:
            counts[value] = 1
    # placeholder return value 
    return counts
   

# Return the most common value from a list 
# Useful for base cases 1 and 3 above.
def majority(values):
    
    counts = getCounts(values)
    #this is weird but max can apparently take a function and use that to calculate which one is maximum
    return max(counts, key = counts.get)
    
    
# Calculate the entropy of a set of values 
# First count how often each value shows up 
# When you divide this value by the total number 
# of elements, you get the probability for that element 
# The entropy is the negation of the sum of p*log2(p) 
# for all these probabilities.
def getEntropy(values):

    #make variable "counts" that stores dict how many times each value shows up
    counts = getCounts(values)
    entropy = 0

    #for each item in the dict, set its count to itself, divided by the # of elements
    #then use that to calculate entropy
    for count in counts:
        counts[count] = counts[count] / len(values)
        
        entropy = entropy + counts[count] * math.log2(counts[count] )

    entropy = entropy * -1

    return entropy    


# This is the main decision tree class 
# DO NOT CHANGE THE FOLLOWING LINE
class DecisionTree:
# DO NOT CHANGE THE PRECEDING LINE
    def __init__(self, tree={}):
        self.tree = tree
    
    # DO NOT CHANGE THE FOLLOWING LINE    
    def fit(self, x, y):
    # DO NOT CHANGE THE PRECEDING LINE
    
        self.majority = majority(y)
        self.tree = make_node(y, x, y, list(range(len(x[0]))))
        
    # DO NOT CHANGE THE FOLLOWING LINE    
    def predict(self, x):
    # DO NOT CHANGE THE PRECEDING LINE    
        if not self.tree:
            return None

        # To classify using the tree:
        # Start with the root as the "current" node

        

        # As long as the current node is an interior node (type == "split"):
        #    get the value of the attribute the split is performed on 
        #    select the child corresponding to that value as the new current node 

        resultList = []
        for row in x:
            current = self.tree

            #print("this is row")
            #print(row)
            while (current != None and current["type"] == "split"):

                key = row[current["split"]]

                #print("this is current before picking")
                #print(current)
                current = current["children"][key]

            #print("this is current after loop")
            #print(current)
                
            if current == None:
                resultList.append(self.majority)
            else: 
                resultList.append(current["class"])

        
        # NOTE: In some cases, your tree may not have a child for a particular value 
        #       In that case, return the majority value (self.majority) from the training set 
        
        # IMPORTANT: You have to perform this classification *for each* element in x 
        # Note that the result is a list of predictions, one for each x-value
        return resultList
    
    # DO NOT CHANGE THE FOLLOWING LINE
    def to_dict(self):
    # DO NOT CHANGE THE PRECEDING LINE
        # change this if you store the tree in a different format
        return self.tree
       

def get_columns(rows, columns, single=False):
    if single:
        return [row[columns[0]] for row in rows]
    return [[row[c] for c in columns] for row in rows]

def main():
    random.seed(3110)
    randomList = []
    for i in range(0,50):
        n = random.randint(1,10)
        randomList.append(n)

    #print(randomList)
    #print(getCounts(randomList))
    #print(getEntropy(randomList))

    df = pandas.read_csv("testdata.csv")
    training = []
    validation = []
    for i,row in df.iterrows():
        if random.random() > 0.85:
            validation.append(row)
        else:
            training.append(row)

    columns = ["cat1", "cat2"]
    target = ["cls3"]

    tx = get_columns(training, columns)
    ty = get_columns(training, target, single=True)

    tree = DecisionTree()

    tree.fit(tx, ty)

    print()
    print(tree.to_dict())



    




if __name__ == '__main__':
    main()