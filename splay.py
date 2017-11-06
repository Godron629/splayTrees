class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree(object):
    def __init__(self, root=None):
        self.root = root
        self.levels = []
        
    def insert(self, node, key):
        """Recursively look through left or right subtree until correct spot is found"""
        if node is None:
            self.root = Node(key)
            return
            
        if key < node.key:
            if node.left is None:  # Found the keys' proper place
                node.left = Node(key)
                self.splay(node.left)
                return
            else:
                insert(node.left, key)  # Continue down the left subtree
        if key > node.key:
            if node.right is None:
                node.right = Node(key)
                self.splay(node.right)
                return
            else:
                insert(node.right, key) 
        return node
        
    def delete(self, key):
        """ Uses technique found on https://en.wikipedia.org/wiki/Splay_tree#Deletion:
        - The node to be deleted is splayed, and then deleted. This creates two sub-trees
        - The two sub-trees are then joined using a join() operation """
        node = self.findParentNodeOfKey(key)
        if key < node.key:
            node = node.left
        else:
            node = node.right
            
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
            
    def find(self, node, key):
        """Recursively look through subtrees until key is found, then splay key to top"""
        if key == self.root.key or node is None: 
            return
        
        if key == node.key:
            self.splay(node)
            return
        
        if key < node.key:
            if node.left is not None:
                self.find(node.left, key)
            else:
                self.splay(node)
        else:
            if node.right is not None:
                self.find(node.right, key)
            else:
                self.splay(node)

    def splay(self, node):
        p = self.findParentNodeOfKey(node.key)
        g = self.findParentNodeOfKey(p.key)
        
        if node.key == self.root.key:
            return
        
        if p.key == g.key and p.key != node.key:  # Simple Rotation
            if node.key < p.key:
                p.left = node.right
                node.right = p
            if node.key > p.key:
                p.right = node.left
                node.left = p
            self.root = node
            self.splay(node)
            
        r = self.findParentNodeOfKey(g.key)
        
        if node.key < p.key < g.key:  # Zig Zig Left
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
            self.splay(node)
            return
        
        if node.key > p.key > g.key:  # Zig Zig Right
            g.right = p.left
            p.right = node.left
            p.left = g
            node.left = p
            if g.key == self.root.key:
                self.root = node
            else:
                if r.data > node.data:
                    r.left = node
                else:
                    r.right = node
            self.splay(node)
            return
        
        if p.key < node.key < g.key:  # RL Zig Zag 
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
            self.splay(node)
            return
                
        if p.key > node.key > g.key:  # LR Zig Zag
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
            self.splay(node)
            return
        
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
    tree = SplayTree()    
    
    for i in range(1, 100000):
        tree.insert(tree.root, i)
    
    tree.inOrderWalk(tree.root)
    
        