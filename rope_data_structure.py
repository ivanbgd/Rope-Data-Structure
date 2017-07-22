import sys
from collections import deque

"""
*** Rope Data Structure ***

Implementation of a data structure that can store a string and efficiently cut a part
(a substring) of this string and insert it in a different position.
This implementation only processes a given string.
It doesn't support inserting of new characters in the string. 

https://en.wikipedia.org/wiki/Rope_(data_structure)

Uses Splay tree to implement the Rope data structure

Nodes don't have keys. They only have values. And the value is a lowercase English letter.
That means that one node contains and represents a single letter.
This data structure is about strings. The string represents (is) contents of a text document.
In a string, letters are in order, of course. The order is represented by their rank. That's why we use
order statistics to locate a node when searching for it (performing a "find" operation).
The rank can be seen as their index, and we'll use 0-based indexing.
The size of a node doesn't have anything to do with its rank. Also, when a node is splayed, its rank doesn't
change; only its size changes.
One has to think in terms of node rank, and not in terms of node key, as usual!
We could also add the field "rank" to Node objects.
But, that's not needed. In-order traversal gives all characters in order

This is Python v2.7.
"""

"""
MIT License
Copyright (c) 2017 Ivan Lazarevic
"""

class Node(object):

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.size = 1

    def printNode(self):
        print "Value: {}, Size: {}; Parent: {}, Left child: {}, Right child: {}".format(self.value, self.size, self.parent, self.left, self.right)

    def __str__(self):
        return "({}, {})".format(self.value, self.size)

    def __repr__(self):
        return "Value: {}; Size: {}".format(self.value, self.size)



class SplayTree(object):

    def __init__(self):
        """Creates an empty splay tree."""
        self.root = None
        self.size = 0

    def inOrder(self):                                          # Iterative
        current = self.root
        if not current:
            return "".join([])
        self.result = []                                        # strings are immutable objects in python, therefore appending to them always creates a new string object, which is way too slow
        stack = []                                              # stack contains nodes
        while True:
            while current:
                stack.append(current)
                current = current.left
            if stack:
                current = stack.pop()
                self.result.append(current.value)
                current = current.right
            else:
                return "".join(self.result)

    def levelOrder(self):                                       # Breadth First Search
        root = self.root
        if not root:
            return []
        self.result = []
        queue = deque([root])                                   # queue contains nodes
        while queue:
            current = queue.popleft()
            self.result.append(current)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return self.result

    def _rotateRight(self, node):
        """Input: A node object that we want to rotate right.
           Returns nothing.
           Doesn't splay any node.
        """
        parent = node.parent
        Y = node.left
        if not Y:
            return None                                         # we can't rotate the node with nothing!
        B = Y.right
        Y.parent = parent
        if parent:
            if node == parent.left:                             # node is left child
                parent.left = Y
            else:                                               # node is right child
                parent.right = Y
        else:
            self.root = Y

        node.parent = Y
        Y.right = node
        if B:
            B.parent = node
        node.left = B

        node.size = (node.left.size if node.left else 0) + (node.right.size if node.right else 0) + 1
        Y.size = (Y.left.size if Y.left else 0) + (Y.right.size if Y.right else 0) + 1

    def _rotateLeft(self, node):
        """Input: A node object that we want to rotate left.
           Returns nothing.
           Doesn't splay any node.
        """
        parent = node.parent
        X = node.right
        if not X:
            return None                                         # we can't rotate the node with nothing!
        B = X.left
        X.parent = parent
        if parent:
            if node == parent.left:                             # node is left child
                parent.left = X
            else:                                               # node is right child
                parent.right = X
        else:
            self.root = X

        node.parent = X
        X.left = node
        if B:
            B.parent = node
        node.right = B

        node.size = (node.left.size if node.left else 0) + (node.right.size if node.right else 0) + 1
        X.size = (X.left.size if X.left else 0) + (X.right.size if X.right else 0) + 1

    def _splay(self, node):
        """
        Splays node to the top of the tree, making it new root of the tree.
        When we splay a node, it will keep its rank; but, it will have a new size.
        Returns nothing.
        """
        if not node:
            return

        parent = node.parent

        while parent:

            left = node.left
            right = node.right
            grandParent = parent.parent

            if not grandParent:
                # Zig
                if node == parent.left:
                    self._rotateRight(parent)
                else:
                    self._rotateLeft(parent)

            elif node == parent.left:
                if parent == grandParent.left:
                    # Zig-zig
                    self._rotateRight(grandParent)
                    self._rotateRight(parent)
                else:
                    # Zig-zag (parent == grandParent.right)
                    self._rotateRight(parent)
                    self._rotateLeft(grandParent)

            elif node == parent.right:
                if parent == grandParent.right:
                    # Zig-zig
                    self._rotateLeft(grandParent)
                    self._rotateLeft(parent)
                else:
                    # Zig-zag (parent == grandParent.left)
                    self._rotateLeft(parent)
                    self._rotateRight(grandParent)

            parent = node.parent

    def orderStatisticZeroBasedRanking(self, k):
        """
        Input: Integer number k - the rank of a node (0 <= k < size of the whole tree).
        Output: The k-th smallest element in the tree (a node object). Counting starts from 0.
        This is a public method, which splays the found node to the top of the tree.
        """
        assert 0 <= k < self.size, "0 <= k < size of the whole tree"
        node = self.root
        while node:
            left, right = node.left, node.right
            s = left.size if left else 0
            if k == s:
                break
            elif k < s:
                if left:
                    node = left
                    continue
                break
            else:
                if right:
                    k = k - s - 1
                    node = right
                    continue
                break
        self._splay(node)
        return node

    """We don't use key. We instead use rank as the position at which to insert a letter (node).
    """
    def insert(self, rank, value):
        """Input: rank is a numerical value (0 <= rank <= size of the whole tree); value is a lowercase English letter.
           This is a general splay tree method, that works in general case.
           Adds a node with letter "value" to the tree (string), at the position "rank". Numbering is 0-based.
           Splays the node up to the top of the tree.
           But, if we insert more than one character at one time (a string), it will also work. It will accept a string, and put it in a node.
           Returns nothing.
           Goes down from root to a leaf only once, and also goes up only once.
        """
        assert 0 <= rank <= self.size, "0 <= rank <= size of the whole tree"

        node = Node(value)
        
        # Inserting at the end of the whole text.
        if rank == self.size and self.size > 0:
            last = self.orderStatisticZeroBasedRanking(rank-1)  # Or, subtreeMaximum(self.root)
            node.left = last
            node.size = last.size + 1
            last.parent = node
            self.size += 1                                      # Tree size
            self.root = node
            return

        # Inserting in the middle (or at the beginning).
        if self.size == 0:
            # The tree is empty.
            self.size += 1                                      # Tree size
            self.root = node
            return
        right = self.orderStatisticZeroBasedRanking(rank)       # This will be right node of the newly inserted node.
        node.right = right
        node.left = right.left
        right.parent = node
        right.left = None
        right.size = (right.right.size if right.right else 0) + 1
        node.size = (node.left.size if node.left else 0) + (node.right.size if node.right else 0) + 1
        self.size += 1                                          # Tree size
        self.root = node

    def insertSpecific(self, value):
        """Input: value is a lowercase English letter.
           This is a specific method, that doesn't work in general case of a splay tree.
           Namely, we first insert entire string and then perform operations on it.
           We will never insert a new character in the string again.
           Adds a node with letter "value" to the tree, as the new root of the tree.
           Returns nothing.
        """
        node = Node(value)
        if self.root:
            self.root.parent = node
        node.left = self.root
        node.size = (node.left.size if node.left else 0) + 1
        self.root = node
        self.size += 1

    def subtreeMaximum(self, node):
        """
        Input: Node object in the tree.
        Returns the node object with maximum rank in the subtree rooted at node.
        Splays the found node to the top of the tree.
        """
        if not node:
            return None
        while node.right:
            node = node.right
        self._splay(node)
        return node



def merge(tree1, tree2):
    """Merges two Splay trees, tree1 and tree2, using the last element (of highest rank) in tree1 (left string) as the node for merging, into a new Splay tree.
    CONSTRAINTS: None.
    INPUTS: tree1, tree2.
    OUTPUT (the return value of this function) is tree1, with all the elements of both trees.
    USAGE: After this function, we can delete tree2.
    """
    if not tree1 or not tree1.size:
        return tree2
    if not tree2 or not tree2.size:
        return tree1
    root2 = tree2.root
    root1 = tree1.subtreeMaximum(tree1.root)
    root2.parent = root1
    root1.right = root2
    root1.size = (root1.left.size if root1.left else 0) + (root1.right.size if root1.right else 0) + 1
    tree1.size = root1.size
    return tree1


def split(tree, rank):
    """
    Splits Splay tree into two trees.
    Input: A Splay tree; rank of a node (counting starts from 0; 0 <= rank < size of the whole tree).
    Output: Two Splay trees, one with elements with rank <= "rank", the other with elements with rank > "rank".
    """
    root1 = tree.orderStatisticZeroBasedRanking(rank)
    root2 = root1.right
    root1.right = None
    root1.size = (root1.left.size if root1.left else 0) + (root1.right.size if root1.right else 0) + 1
    tree1 = SplayTree()
    tree1.root = root1                                          # insertTree()
    tree1.size = root1.size
    tree2 = SplayTree()        
    if root2:
        root2.parent = None
        tree2.root = root2                                      # insertTree()
        tree2.size = root2.size
    return tree1, tree2


def process(tree, i, j, k):
    """This is cut-and-paste function.
       For i and j, counting starts from 0; for k, counting starts from 1.
       We paste the substring after the k-th symbol of the remaining string (after cutting).
       If k == 0, we insert the substring at the beginning.
    """
    middle, right = split(tree, j)
    if i > 0:
        left, middle = split(middle, i - 1)
    else:
        left = None
    left = merge(left, right)
    if k > 0:
        left, right = split(left, k - 1)
    else:
        right = left
        left = None
    tree = merge(merge(left, middle), right)
    return tree


def printTree(tree, verbose = False):
    """If boolean verbose is True, it will print all nodes, in level order (BFS).
    """
    print
    print "In order:", tree.inOrder()
    if verbose:
        print "Nodes (in level order (BFS)):"
        nodes = tree.levelOrder()
        for node in nodes:
            node.printNode()
    print


"""
Example usage:
Input a string S from a line.
The next line contains number of operations that we want to perform on the string, numOps.
The following numOps lines contain triples of integers (i, j, k).
For i and j, counting starts from 0; for k, counting starts from 1.
The code will cut the substring S[i..j] from S and insert it after the k-th character of
the remaining string. If k == 0, it inserts the substring at the beginning.
"""
	
tree = SplayTree()
rope = sys.stdin.readline().strip()
for i in xrange(len(rope)):
    #tree.insert(i, rope[i])
    tree.insertSpecific(rope[i])
#printTree(tree, True)
numOps = int(sys.stdin.readline())
for _ in xrange(numOps):
    i, j, k = map(int, sys.stdin.readline().strip().split())
    tree = process(tree, i, j, k)
#printTree(tree, True)
print tree.inOrder()