import random 
import sys 
import math 
import matplotlib.pyplot as plt
sys.setrecursionlimit(100000)

class RBNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = "R"

    def get_uncle(self):
        return

    def is_leaf(self):
        return self.left == None and self.right == None

    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def is_red(self):
        return self.colour == "R"

    def is_black(self):
        return not self.is_red()

    def make_black(self):
        self.colour = "B"

    def make_red(self):
        self.colour = "R"

    def get_brother(self):
        if self.parent.right == self:
            return self.parent.left
        return self.parent.right

    def get_uncle(self):
        return self.parent.get_brother()

    def uncle_is_black(self):
        if self.get_uncle() == None:
            return True
        return self.get_uncle().is_black()

    def __str__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def __repr__(self):
         return "(" + str(self.value) + "," + self.colour + ")"

    # Make a left leaning red link lean right (temporarily)
    # Move left child to position of self 
    def rotate_right(self):
        # Preconditions
        # self.is_red(self.left)
        # self.value > self.left.value 
        
        nx = self.left
        if nx != None:
        
            #  Make self left tree nx right tree
            self.left = nx.right
            if nx.right != None: # Change parent of nx.right
                nx.right.parent = self
                
            # Make nx parent self.parent 
            nx.parent = self.parent
            if self.parent != None:
                # Update new parent child pointers
                if self.is_left_child():
                    self.parent.left = nx
                else:
                    self.parent.right = nx
            
            # Make self nx right child and self parent 
            nx.right = self
            self.parent = nx
            return nx
        
        else: 
            return self 

    # Rotate left if right leaning red link 
    # Move right child to position of self 
    def rotate_left(self):
        # self.is_red(self.right)
        # self.value < self.right.value 
        nx = self.right
        if nx != None:

            # Make self right point to nx left 
            self.right = nx.left

            # Update nx left parent 
            if nx.left != None:
                nx.left.parent = self

            # Make nx parent self 
            nx.parent = self.parent
            if self.parent:
                # Update child pointers of nx parent 
                if self.is_left_child():
                    self.parent.left = nx
                else:
                    self.parent.right = nx

            # Make self nx left child
            # Update self parent     
            nx.left = self
            self.parent = nx

            return nx
        
        else:
            return self

class RBTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
                self.fix(node.left)
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
                self.fix(node.right)
            else:
                self.__insert(node.right, value)

    # Go up the tree from this node, and fix it 
    # The node given is always a leaf (I think) 
    # Don't fix the tree every height, you have to go up the tree and fix it 
    # node inserted is initialized as red
    def fix(self, node):
        # print(f"fixing: {node}")
      

        #You may alter code in this method if you wish, it's merely a guide.
        # Root 
        if node.parent == None:
            node.make_black()
        
        # https://www.geeksforgeeks.org/dsa/insertion-in-red-black-tree/
        # parent red, and current node is red (initially) as new nodes are created as red
        # 
        while node != None and node.parent != None and node.parent.is_red(): 

            parent = node.parent 
            gp = parent.parent 

            if gp is None: 
                break ## this is the root 

            if parent.is_left_child(): 
                uncle = gp.right 

                # C1: Uncle is red (parent also red)
                # Flip colours
                if uncle != None and uncle.is_red(): 
                    parent.make_black() 
                    uncle.make_black() 
                    gp.make_red() 
                    node = gp # Move pointe up tree 
                    # if node.parent != None: 
                    #     parent = node.parent 
                    #     gp = parent.parent

                else: # Uncle is None or uncle is black
                    
                    # Red right child, red parent 
                    if node.is_right_child(): 
                        node = parent 
                        newNode = node.rotate_left()
                        if newNode != None and newNode.parent is None: 
                            self.root = newNode

                        parent = node.parent # Node is now in parents position, so update parent

                        # if parent != None: 
                        #     gp = parent.parent  

                    if parent != None: 
                        parent.make_black() 
                    
                    # New root 
                    elif parent is None: 
                        self.root = node
                        break
                    
                    if parent != None and gp != None:
                        gp.make_red() 
                        newNode = gp.rotate_right()
                        if newNode != None and newNode.parent is None: 
                            self.root = newNode

            else: 
                uncle = gp.left 

                if uncle != None and uncle.is_red(): 
                    parent.make_black() 
                    uncle.make_black() 
                    gp.make_red() 
                    node = gp # Move up tree

                else: 
                    if node.is_left_child(): 
                        node = parent 
                        newNode = node.rotate_right() 
                        if newNode != None and newNode.parent is None: 
                            self.root = newNode
                        parent = node.parent # Not sure if needed

                    if parent != None: 
                        parent.make_black()
                    
                    elif parent is None: 
                        self.root = node

                    gp.make_red() 
                    newNode = gp.rotate_left() 
                    if newNode != None and newNode.parent is None: 
                            self.root = newNode


        
        self.root.make_black()

        
    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"


# Insertion into a bst, doesn't balance height
def insert_bst(root,value): 
    
    if root is None:
        return RBNode(value)
    
    curr = root 
    while curr != None:
        prev = curr
        if value < curr.value: 
            curr = curr.left

        else: 
            curr = curr.right 

    if value < prev.value: 
        prev.left = RBNode(value) 
    
    else: 
        prev.right = RBNode(value)

    return root 

# create random lists of size `length` up to `max_value`
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]

# create bst based on list of values provided 
def create_random_bst(values): 
    n = len(values)          # number of elements to be inserted 

    bst = RBTree()           # Reuse RBTree class, but don't use its insertion methods
    root = RBNode(values[0]) # Root is first value 
    bst.root = root          # Set tree root to root 

    for i in range(1,n): 
        insert_bst(root,values[i]) # Insert value into the bst 


    # print(bst) 

    return bst


# Create rbt based on list of values provided 
def create_random_rbt(values): 

    rbt = RBTree() 
    for value in values: 
        rbt.insert(value) 
        # print(f"Inserting {value}: {rbt}")



    return rbt


def swap(L, i, j):
    L[i], L[j] = L[j], L[i]


def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L


# Run an experiment where you create RBTs and BSTs based of randomly generated lists of numbers of length
#   10,000.
# n - number of BSTs/RBTs  
def experiment1(n): 
    # Create RBTs and BSTs based on `n` randomly generated lists of numbers of length 10000
    # Calculate the average difference in height between the two
    #   - abs(Total RBT height - Total BST height) / number of trees
    # Note on whether you think there is a case where you would prefer a BST over an RBT
    # What is your ins8nct on the performance of a BST insert to a RBT insert for trees of similar heights?


    # Generate n lists of size 10000, 
    bstHeight = 0
    rbtHeight = 0
    max_value = 100000
    length = 10000
    

    for i in range(n): 
        rl = create_random_list(length,max_value) # Max value 16384
        bst = create_random_bst(rl)         # Generaete random bst
        rbt = create_random_rbt(rl)         # Generate random rbt

        bstHeight += bst.get_height() 
        rbtHeight += rbt.get_height()

    # Compute average height difference between rbt and bst take absolute value 
    avgDiff = (bstHeight - rbtHeight) / n 



    return avgDiff

# max_swaps = 46051
# Want 100 lists, so skip -> 461
def experiment2(): 
    length = 10000
    max_value = 100000
    max_swaps = 150 #int(length * math.log(length) / 2)
    # nearSortedLists = []
    num_swaps = []
    height_diff = []

    # For every number of swaps 
    for x in range(0,max_swaps,math.ceil(max_swaps/100)): # want 100 arrays 
        num_swaps.append(x) # Store number of swaps 

        # nearSortedLists = []
        bstHeight = 0
        rbtHeight = 0
        avgDiff = 0
        n = 10 # number of lists to generate 
        # Generate 100 lists 
        for _ in range(n): 
            L = create_near_sorted_list(length,max_value,x)  # Generate random list for given num_swaps 
            bstHeight += create_random_bst(L).get_height()  # Calculate bstHeight
            rbtHeight += create_random_rbt(L).get_height()  # Calculate rbtHeight 

        print("Finished iteration")

        avgDiff = (bstHeight - rbtHeight) / n 

        height_diff.append(avgDiff) 

    plt.plot(num_swaps, height_diff, color='blue')
    
    plt.xlabel("Swaps")
    plt.ylabel("Height diff")
    plt.title("Average height diff b/w RBT and BST")
    plt.legend()
    plt.show()


    return 



# ************** XC3 Tree Implementation *******************
class XC3Node:
    def __init__(self, degree):
        self.degree = degree
        self.children = []
        self._build_tree()

    def _build_tree(self):
        for j in range(1, self.degree + 1):
            child_degree = (j - 2) if j > 2 else 0
            self.children.append(XC3Node(child_degree))

    def get_num_nodes(self):
        return 1 + sum(child.get_num_nodes() for child in self.children)

    def get_height(self):
        if not self.children:
            return 1
        return 1 + max(child.get_height() for child in self.children)




def experiment3_4():
    for i in range(26):
        tree = XC3Node(i)
        nodes = tree.get_num_nodes()
        height = tree.get_height()
        print("--------------------------")
        print("Degree: " + str(i))
        print("Number of nodes: " + str(nodes))
        print("Height: " + str(height))
        print("--------------------------")
    
    return

# *** RUN EXPERIMENTS ** 
# print(experiment1(100))
# experiment2()
experiment3_4()

