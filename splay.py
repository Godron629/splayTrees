from copy import deepcopy

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None
        self.header = Node(None)
        self.levels = []
        
    @classmethod
    def height(node):
        """Return the height of a node"""
        if node is None:
            return -1
        return max(height(node.left), height(node.right)) + 1
        
    def inOrderWalk(self, root, level=0):
        """Walk the tree in order(L - Root - R), updates class variable
        self.levels which is a 2D array of all the nodes and their (Level, Key)
        
        - Particular to the assignment, 'level' is synonymous with 'Size, S(x)',
        AKA 'the number of nodes in the subtree rooted at x'"""
        if level == 0:
            self.levels = []  # Since self.levels is acting as a global, lets not reuse last run
        levels = self.levels
        node = root
        if node:
            self.inOrderWalk(node.left, level+1)
            self.levels.append([level, node.key])
            self.inOrderWalk(node.right, level+1)
            
        if level == 0:  # Only printLevels if recursion has unwrapped
            self._printLevels()
            
    def _printLevels(self):
        """Used by inOrder() so visualize tree"""
        
        def __findMaxLevel(levels):
            maxLevel = 0
            for node in levels:
                if node[0] > maxLevel:
                    maxLevel = node[0]
            return maxLevel
                    
        def __sortByLevel(levels):
            return sorted(levels, key=lambda l: l[0])
        
        levels = self.levels
        maxLevel = __findMaxLevel(levels) 
        levels = __sortByLevel(levels)
        
        print "-----"
        for i in range(maxLevel+1):
            values = [x[1] for x in levels if x[0] == i]  # Group all nodes at ith level
            print "Level {}: {}".format(i, values)
            
    def findParent(self, key):
        node = self.root
        parent = self.root
        while(node.key != key):
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return parent
        
    def rrRotate(self, k2):
        """
            k2             k1
           /  \           /  \
          k1   Z   -->   X    k2
         /  \                /  \
        X    Y              Y    Z
        """
        k1 = k2.left
        k2.left = k1.right
        k1.right = k2
        return k1
    
    def llRotate(self, k2):
        """
            k2                k1
           /  \              /  \
          X    k1    -->    k2    Z
              /  \         /  \
             Y    Z       X    Y
        """
        k1 = k2.right
        k2.right = k1.left
        k1.left = k2
        return k1
    
    def insert(self, key):
        if (self.root is None):  # Empty tree
            self.root = Node(key)
            return

        # Check if key is already in the tree
        self.splay(key) 
        if self.root.key == key:
            return

        newNode = Node(key)
        if key < self.root.key:
            newNode.left = self.root.left
            newNode.right = self.root
            self.root.left = None
            self.root = newNode
        else:
            newNode.right = self.root.right
            newNode.left = self.root
            self.root.right = None
            self.root = newNode

    def delete(self, key):
        self.splay(key)  
        
        if key != self.root.key:
            print "Key not found in tree..."

        # Delete the root
        if self.root.left is None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x

    def find(self, key):
        if self.isEmpty():
            return None
        self.splay(key)
        if self.root.key != key:
            return None
        return self.root.key

    def isEmpty(self):
        if self.root is None:
            return True
        return False
    
    def splay(self, key):
        leftTreeMax = rightTreeMin = self.header
        root = self.root
        self.header.left = self.header.right = None
        while True:
            if key < root.key:
                if root.left is None:
                    break
                if key < root.left.key:
                    root = self.rrRotate(root)
                    if root.left == None:
                        break
                rightTreeMin.left = root  
                rightTreeMin = root
                root = root.left
            elif key > root.key:
                if root.right is None:
                    break
                if key > root.right.key:
                    #root = self.llRotate(root)
                    if root.right is None:
                        break
                leftTreeMax.right = root
                leftTreeMax = root
                root = root.right
            else:
                break
        leftTreeMax.right = root.left
        rightTreeMin.left = root.right
        root.left = self.header.right
        root.right = self.header.left
        self.root = root
                
if __name__ == "__main__":
    tree = SplayTree()    
    
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.inOrderWalk(tree.root)
    
    tree.find(1)
    tree.inOrderWalk(tree.root)
    
    tree.find(4)
    tree.inOrderWalk(tree.root)
    
        
        
        