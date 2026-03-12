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
