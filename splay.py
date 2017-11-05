import sys

sys.setrecursionlimit(15000)
levels = []

def height(node):
    if node is None:
        return -1
    return max(height(node.left), height(node.right)) + 1

def printLevels():
    maxLevel = 0
    for thing in levels:
        if thing[0] > maxLevel:
            maxLevel = thing[0]
        
    thing = sorted(levels, key=lambda l: l[0])
    for i in range(maxLevel+1):
        values = [x[1] for x in thing if x[0] == i]
        print "Level {}: {}".format(i, values)
        

def inOrder(root, level=0):
    if root:
        inOrder(root.left, level+1)
        levels.append([level, root.key])
        inOrder(root.right, level+1)

class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None

    def equals(self, node):
        return self.key == node.key

class SplayTree:
    def __init__(self):
        self.root = None
        self.header = Node(None) #For splay()

    def insert(self, key):
        if (self.root == None):
            self.root = Node(key)
            return

        self.splay(key)
        if self.root.key == key:
            # If the key is already there in the tree, don't do anything.
            return

        n = Node(key)
        if key < self.root.key:
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
        self.root = n

    def remove(self, key):
        self.splay(key)
        if key != self.root.key:
            raise ValueError("Key not found")

        # Now delete the root.
        if self.root.left== None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x

    def find(self, key):
        if self.root == None:
            return None
        self.splay(key)
        if self.root.key != key:
            return None
        return self.root.key

    def isEmpty(self):
        return self.root == None
    
    def splay(self, key):
        l = r = self.header
        t = self.root
        self.header.left = self.header.right = None
        while True:
            if key < t.key:
                if t.left == None:
                    break
                if key < t.left.key:
                    y = t.left
                    t.left = y.right
                    y.right = t
                    t = y
                    if t.left == None:
                        break
                r.left = t
                r = t
                t = t.left
            elif key > t.key:
                if t.right == None:
                    break
                if key > t.right.key:
                    y = t.right
                    t.right = y.left
                    y.left = t
                    t = y
                    if t.right == None:
                        break
                l.right = t
                l = t
                t = t.right
            else:
                break
        l.right = t.left
        r.left = t.right
        t.left = self.header.right
        t.right = self.header.left
        self.root = t
                
if __name__ == "__main__":
    tree = SplayTree()    
    for i in range(10001):
        tree.insert(i)
        
    #inOrder(tree.root)
    #printLevels()
    levels = []
    
        
        
        