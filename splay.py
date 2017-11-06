class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None
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
        self.find(self.root, key)
        if self.root.left is None and self.root.right is not None and self.root.right.left is None:
            self.root = self.root.right
        if self.root.right is None and self.root.left is not None and self.root.left.right is None:
            self.root = self.root.left
        if self.root.key == key and self.root.left is not None:
            node = self.root.left
            while(node.right is not None):
                node = node.right
            parent = self.findParent(node.key)
            node.right = parent.right
            self.root = node  #????? Make this work!
            #parent.right = node.left
            #self.root.key = node.key
            return
        if self.root.key == key and self.root.right is not None:
            node = self.root.right
            while(node.left is not None):
                node = node.left
            parent = self.findParent(node.key)
            parent.left = node.right
            self.root.key = node.key
            return
        if self.root.key == key:
            self.root = None
        else:
            return
                
            
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
        
        if p.key < node.key < g.key:  # Zig Zag 
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
                
        if p.key > node.key > g.key:  # Zig Zag
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
    
    tree.insert(tree.root, 1)
    tree.insert(tree.root, 2)
    tree.insert(tree.root, 3)
    tree.insert(tree.root, 4)
    tree.insert(tree.root, 8)
    tree.insert(tree.root, 9)
    
    tree.delete(2)
    tree.inOrderWalk(tree.root)
    tree.delete(4)
    tree.inOrderWalk(tree.root)
    
        
        
        