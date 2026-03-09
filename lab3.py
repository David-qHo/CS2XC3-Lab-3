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

    def fix(self, node):

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


        #You may alter code in this method if you wish, it's merely a guide.
        #if node.parent == None:
        #   node.make_black()
        

        #while node != None and node.parent != None and node.parent.is_red(): 
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
