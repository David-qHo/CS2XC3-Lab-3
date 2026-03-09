import random 

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
    def rotate_right(self):
        # Preconditions
        # self.is_red(self.left)
        # self.value > self.left.value 

        # Left node exists
        if self.left is not None:

            nx = self.left          # Get left node 
            self.left = nx.right    # Set current nodes left pointer to nx right 
            nx.right = self         # Set nx right pointer to current node 
            nx.colour = self.colour # Make nx same colour as current node
            self.colour = "R"       # Make current node red

            return nx 
        
        return self # Return original node if left node empty 

    # Rotate left if right leaning red link 
    def rotate_left(self):
        # self.is_red(self.right)
        # self.value < self.right.value 

        # Right node exists
        if self.right is not None: 
            nx = self.right         # Get right node 
            self.right = nx.left    # Set current nodes right pointer to nx left 
            nx.left = self          # Set nx left pointer to current node 
            nx.colour = self.colour # Make nx same colour as current node
            self.colour = "R"       # Make current node red

            return nx
        
        return self # Return original node if right node empty     



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

        # Root 
        if node.parent is None: 
            return node 
        
        # If leaf 
        if node.left is None and node.right is None: 
            return node.fix(node.parent)
        # From Algorithms, 4th Edition by Robert Sedgewick and Kevin Wayn

        # right child red, and left child is not
        # Rotate left 
        if node.right.is_red() and not node.left.is_red(): 
            node = node.rotate_left() 

        # Left child red, and left grandchild red (Long red chain)
        # Rotate right
        if node.left.is_red() and node.left.left.is_red(): 
            node = node.rotate_right()

        # 4 node so propagate up (Flip colours)
        if node.left.is_red() and node.right.is_red(): 
            # node is not red 
            node.colour = "R"
            node.left.colour = "B"
            node.right.colour = "B"

        node.fix(node.parent) 

        #You may alter code in this method if you wish, it's merely a guide.
        #if node.parent == None:
        #   node.make_black()
        
        # https://www.geeksforgeeks.org/dsa/insertion-in-red-black-tree/
        # parent red, and current node is red (initially) as new nodes are created as red
        # 
        # while node != None and node.parent != None and node.parent.is_red(): 
            # C1 right child red, and left child not 

            #TODO
        #    return 
        
        self.root.make_black()

        return
                    
        
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
    
    if value < root.value: 
        root.left = insert_bst(root.left,value)
    
    else: 
        root.right = insert_bst(root.right,value)

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
    rbt.insert(values[0])
    rbt.insert(values[1])
    for value in values: 
        #rbt.insert(value) 
        break
    #print(rbt)

    return rbt


l = create_random_list(5,30)
# print(f"bst: {create_random_bst(l)}")
# print(f"rbt: {create_random_rbt(l)}")

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
    

    for i in range(n): 
        rl = create_random_list(10000,2^14) # Max value 16384
        bst = create_random_bst(rl)         # Generaete random bst
        rbt = create_random_rbt(rl)         # Generate random rbt

        bstHeight += bst.get_height() 
        rbtHeight += rbt.get_height()

    # Compute average height difference between rbt and bst take absolute value 
    avgDiff = abs(rbtHeight - bstHeight) / n 





    return 