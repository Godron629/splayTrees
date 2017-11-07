from random import shuffle
from math import log

import matplotlib.pyplot as plt

def simpleCalc(x1, x2, p1, p2):
    first = 1 + x2 - x1 + p2 - p1
    second = 3 * (x2 - x1)
    return [first, second]

def zigOrZagCalc(x1, x2, p1, p2, g1, g2):
    first = 2 + x2 - x1 + p2 - p1 + g2 - g1
    second = 3 * (x2 - x1)
    return [first, second]


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree(object):
    def __init__(self, root=None):
        self.root = root
        self.levels = []
        self.trackRotations = False
        self.simpleRanks = []  # [[1+x2-x1+p2-p1],[3(x2-x1)]]
        self.zigzigRanks = []
        self.zigzagRanks = []
        
    def insert(self, key, node=-1):
        """Recursively look through left or right subtree until correct spot is found
        - Check (if node == -1) so that we don't have to pass self.root into the function
        on a non-recursive call"""
        if node == -1:
            node = self.root
            
        if node is None:
            self.root = Node(key)
            return
            
        if key < node.key:
            if node.left is None:  # Found the keys' proper place
                node.left = Node(key)
                self.splay(node.left)
                return
            else:
                self.insert(key, node.left)  # Continue down the left subtree
        if key > node.key:
            if node.right is None:
                node.right = Node(key)
                self.splay(node.right)
                return
            else:
                self.insert(key, node.right) 
        return node
        
    def delete(self, key):
        """ Uses technique found on https://en.wikipedia.org/wiki/Splay_tree#Deletion:
        - The node to be deleted is splayed, and then deleted. This creates two sub-trees
        - The two sub-trees are then joined using a join() operation """
        if self.root.left is None and self.root.right is None:
            self.root = None
            return
        
        node = self.findParentNodeOfKey(key)
        
        if key < node.key:
            node = node.left
        elif key > node.key:
            node = node.right
        else:
            pass
            
        self.splay(node)
        
        lSub = SplayTree(self.root.left)
        rSub = SplayTree(self.root.right)
        
        self.root = None
        self.join(lSub, rSub)
        
    def join(self, lSub, rSub):
        """Splay the largest key in the left subtree, then make rSub the right child of lSub"""
        largest = lSub.getLargest()
        lSub.splay(largest)
        self.root = largest
        self.root.right = rSub.root
        
    def getLargest(self):
        """Return the largest node of tree
        - To get the largest node of a subtree, make a new Subtree() and call this"""
        node = self.root
        if node.right is None:
            return node
        while(node.right is not None):
            node = node.right
        return node
            
    def find(self, key, node=-1):
        """Recursively look through subtrees until key is found, then splay key to top
        - Check (if node == -1) so that we don't have to pass self.root as a param in a
        non-recursive call"""
        if node == -1:
            node = self.root
        
        if key == self.root.key or node is None: 
            return
        
        if key == node.key:
            self.splay(node)
            return
        
        if key < node.key:
            if node.left is not None:
                self.find(key, node.left)
            else:
                self.splay(node)
        else:
            if node.right is not None:
                self.find(key, node.right)
            else:
                self.splay(node)

    def splay(self, node):
        p = self.findParentNodeOfKey(node.key)
        g = self.findParentNodeOfKey(p.key)
        
        if node.key == self.root.key:
            return
        
        # Simple Rotation
        if p.key == g.key and p.key != node.key:  
            if self.trackRotations:  # For assignment
                p1 , x1 = self.getRanksForPlot(p, g, node, "simple")
                
            if node.key < p.key:
                p.left = node.right
                node.right = p
            if node.key > p.key:
                p.right = node.left
                node.left = p
            self.root = node
            
            if self.trackRotations: # For assignment
                p2, x2 = self.getRanksForPlot(p, g, node, "simple")
                self.simpleRanks.append(simpleCalc(x1, x2, p1, p2))
                
            self.splay(node)
            
        r = self.findParentNodeOfKey(g.key)
        
        # Zig Zig Left
        if node.key < p.key < g.key: 
            if self.trackRotations:
                p1, x1, g1 = self.getRanksForPlot(p, g, node, "zigzig")
                
            g.left = p.right
            p.left = node.right
            p.right = g
            node.right = p
            if g.key == self.root.key:
                self.root = node
            else:
                if r.key > node.key:
                    r.left = node
                else:
                    r.right = node
            
            if self.trackRotations:
                p2, x2, g2 = self.getRanksForPlot(p, g, node, "zigzig")
                self.zigzigRanks.append(zigOrZagCalc(x1, x2, p1, p2, g1, g2))
                
            self.splay(node)
            return
        
        # Zig Zig Right
        if node.key > p.key > g.key: 
            if self.trackRotations:
                p1, x1, g1 = self.getRanksForPlot(p, g, node, "zigzig")
                
            g.right = p.left
            p.right = node.left
            p.left = g
            node.left = p
            if g.key == self.root.key:
                self.root = node
            else:
                if r.key > node.key:
                    r.left = node
                else:
                    r.right = node
                    
            if self.trackRotations:
                p2, x2, g2 = self.getRanksForPlot(p, g, node, "zigzig")
                self.zigzigRanks.append(zigOrZagCalc(x1, x2, p1, p2, g1, g2))
                
            self.splay(node)
            return
        
        if p.key < node.key < g.key:  # RL Zig Zag 
            if self.trackRotations:
                p1, x1, g1 = self.getRanksForPlot(p, g, node, "zigzag")
                
            p.right = node.left
            g.left = node.right
            node.left = p
            node.right = g
            if g.key == self.root.key:
                self.root = node
            else:
                if r.key > node.key:
                    r.left = node
                else:
                    r.right = node
                    
            if self.trackRotations:
                p2, x2, g2 = self.getRanksForPlot(p, g, node, "zigzig")
                self.zigzagRanks.append(zigOrZagCalc(x1, x2, p1, p2, g1, g2))
                
            self.splay(node)
            return
                
        if p.key > node.key > g.key:  # LR Zig Zag
            if self.trackRotations:
                p1, x1, g1 = self.getRanksForPlot(p, g, node, "zigzag")
                
            p.left = node.right
            g.right = node.left
            node.right = p
            node.left = g
            if g.key == self.root.key:
                self.root = node
            else:
                if r.key > node.key:
                    r.left = node
                else:
                    r.right = node
                    
            if self.trackRotations:
                p2, x2, g2 = self.getRanksForPlot(p, g, node, "zigzig")
                self.zigzagRanks.append(zigOrZagCalc(x1, x2, p1, p2, g1, g2))
                
            self.splay(node)
            return
        
    def getRanksForPlot(self, p, g, node, rotationType):
        if rotationType == "simple":
            pRank = log(self.size(p), 2)
            xRank = log(self.size(node), 2)
            return pRank, xRank
        if rotationType in ["zigzig", "zigzag"]:
            pRank = log(self.size(p), 2)
            xRank = log(self.size(node), 2)
            gRank = log(self.size(g), 2)
            return pRank, xRank, gRank
        else:
            raise ValueError("rotationType: {} not supported".format(rotationType))
        
    def findParentNodeOfKey(self, key):
        """Find parent node of a key"""
        node = self.root
        parent = self.root
        while(node.key != key):
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return parent
            
    def height(self, node):
        """Return the height of a node"""
        if node is None:
            return -1
        return max(self.height(node.left), self.height(node.right)) + 1
    
    def size(self, node):
        """Return size of subtree rooted at x, including x"""
        if node is None:
            return 0
        return(self.size(node.left) + self.size(node.right) + 1)
    
    def iterativeHeight(self, root):
        """Compute the height of a node, iterative because I kept blowing the stack with recursion
        with trees above 10,000 nodes"""
        if root is None:
            return 0
        q = []
        q.append(root)
        height = 0
        
        while(True):
            nodeCount = len(q)
            if nodeCount == 0:
                return height
            height += 1
            while(nodeCount > 0):
                node = q[0]
                q.pop(0)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
                nodeCount -= 1
    
    def inOrderWalk(self, root=None, level=0):
        """Walk the tree in order(L - Root - R), updates class variable
        self.levels which is a 2D array of all the nodes and their (Level, Key)
        
        - Particular to the assignment, 'level' synonymous with 'Size, S(x)',
        AKA 'the number of nodes in the subtree rooted at x'"""
        if level == 0:
            root = self.root
            self.levels = []  # Since self.levels is acting as a global, lets not reuse last run
            
        if root:
            self.inOrderWalk(root.left, level+1)
            self.levels.append([level, root.key])
            self.inOrderWalk(root.right, level+1)
            
        if level == 0:  # Only printLevels if recursion has unwrapped
            self.printLevels()
            
    def printLevels(self):
        """Used by inOrder() so visualize tree"""
        
        def _findMaxLevel(levels):
            maxLevel = 0
            for node in levels:
                if node[0] > maxLevel:
                    maxLevel = node[0]
            return maxLevel
                    
        levels = self.levels
        maxLevel = _findMaxLevel(levels) 
        
        print "-----"
        for i in range(maxLevel+1):
            values = [x[1] for x in levels if x[0] == i]  # Group all nodes at ith level
            print "Level {}: {}".format(i, values)
            
                
if __name__ == "__main__":
    """Sub Question 2
    - Construct a splay tree with 100,000 nodes in random order 1,2,3,...100,000
    - Insert key 200,000 and bring 200,000 to the top
    - Compute the total cost of all rotations and compare with 1+3*log(100001, 2)
    - Repeat a few times
    """
    tree2 = SplayTree()
    
    x = range(1, 100001)
    shuffle(x)
    
    for i in x:
        tree2.insert(i)
        
    tree2.trackRotations = True
    tree2.insert(200000)
    
    # What is the total cost of operations?
    
    simpleFirst = [x[0] for x in tree2.simpleRanks]
    simple3x = [x[1] for x in tree2.simpleRanks]
    print "Simple First Sum: {}".format(sum(simpleFirst))
    print "Simple Sum 3x Sum: {}".format(sum(simple3x))
    
    zigzigFirst = [x[0] for x in tree2.zigzigRanks]
    zigzig3x = [x[1] for x in tree2.zigzigRanks]
    print "ZigZig First Sum: {}".format(sum(zigzigFirst))
    print "ZigZig Sum 3x Sum: {}".format(sum(zigzig3x))
    
    zigzagFirst = [x[0] for x in tree2.zigzagRanks]
    zigzag3x = [x[1] for x in tree2.zigzagRanks]
    print "ZigZag First Sum: {}".format(sum(zigzagFirst))
    print "ZigZag Sum 3x Sum: {}".format(sum(zigzag3x))
    
    print "Compare: {}".format(1 + 3*log(100001, 2))
    
    plt.plot(zigzig3x)
    plt.plot(zigzag3x)
    plt.plot(simple3x)
    
    plt.legend(["zigzigFirst", "zigzagFirst", "simpleFirst"], loc="upper left")
    
    plt.show()
    
        