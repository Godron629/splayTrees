class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree(object):
    def __init__(self, root=None):
        self.root = root
        self.levels = []
        
    def height(self, node):
        """Return the height of a node"""
        if node is None:
            return -1
        return max(self.height(node.left), self.height(node.right)) + 1
        
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
            self.printLevels()
            
    def printLevels(self):
        """Used by inOrder() so visualize tree"""
        
        def _findMaxLevel(levels):
            maxLevel = 0
            for node in levels:
                if node[0] > maxLevel:
                    maxLevel = node[0]
            return maxLevel
                    
        def _sortByLevel(levels):
            return sorted(levels, key=lambda l: l[0])
        
        levels = self.levels
        maxLevel = _findMaxLevel(levels) 
        levels = _sortByLevel(levels)
        
        print "-----"
        for i in range(maxLevel+1):
            values = [x[1] for x in levels if x[0] == i]  # Group all nodes at ith level
            print "Level {}: {}".format(i, values)
            
    def findParent(self, key):
        node = self.root
        parent = self.root
        while(node.key != key):
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return parent
        
    def insert(self, node, key):
        if node is None:
            self.root = Node(key)
            return
            
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
                self.splay(node.left)
                return
            else:
                insert(node.left, key)
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
        node = self.findParent(key)
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
        node = self.root
        if node.right is None:
            return node
        while(node.right is not None):
            node = node.right
        return node
            
    def find(self, node, key):
        if key == self.root.key or node is None:
            return
        if key == node.key:
            self.splay(node)
            return
        if key < node.key:
            if node.left is not None:
                self.find(node.left, key)
            else: self.splay(node)
        else:
            if node.right is not None:
                self.find(node.right, key)
            else:
                self.splay(node)

    def isEmpty(self):
        if self.root is None:
            return True
        return False
    
    def splay(self, node):
        p = self.findParent(node.key)
        g = self.findParent(p.key)
        
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
            
        r = self.findParent(g.key)
        
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
            
            
                
if __name__ == "__main__":
    tree = SplayTree()    
    
    for i in range(1, 10):
        tree.insert(tree.root, i)
    
    tree.inOrderWalk(tree.root)
    
    tree.find(tree.root, 2)
    tree.inOrderWalk(tree.root)
    tree.find(tree.root, 4)
    tree.inOrderWalk(tree.root)
    
        
        
        