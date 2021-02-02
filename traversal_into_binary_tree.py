# =========================================================================================
# !/usr/bin/env python3
# Filename: traversal_into_binarytree.py
# Description:Implementation of binarytree |   
# Author: Bharathkumar Sivakumar <BHARATH SBK @ITSMESBK>
# Python Environment - Python3
# Usage: To be used as a solution for multi paragdim problems  
# ===========================================================================================
'''
LINKEDLIST

data(1) -> data(2) -> data(3) -> data(4) -> data(5) -> data(6) -> data(7)

BINARY TREE

                 Node(1)                                                  
                /
            Node(2)
           /    \
          /      Node(3)
  RootNode(4)
          \      Node(5)
           \    /
            Node(6)
                \
                 Node(7)

------ ------ ------
key    List   Tree
------ ------ ------
1      1      3
2      2      2
3      3      3
4      4      1
5      5      3
6      6      2
7      7      3
------ ------ ------
avg    4      2.43
------ ------ ------

Binary Search Tree has better time complexity than linked list in case of searching an element .

Average time taken in case of BST will be: ---> O(log n) .

But if BST is left or right skewed then it will take ---> O(n).

That is a very rare scenario.

Now in linked list search will take ---> O(n ) in average or worst scenario.

So for fast searching and in few insertion scenarios BST is preffered over linked list

'''
#INORDER | PRE-ORDER | POST-ORDER
class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()

# Inorder traversal
# Left -> Root -> Right
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res

# Preorder traversal
# Root -> Left ->Right
    def PreorderTraversal(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.PreorderTraversal(root.left)
            res = res + self.PreorderTraversal(root.right)
        return res

# Postorder traversal
# Left ->Right -> Root
    def PostorderTraversal(self, root):
        res = []
        if root:
            res = self.PostorderTraversal(root.left)
            res = res + self.PostorderTraversal(root.right)
            res.append(root.data)
        return res        

# Code execution starts here 
if __name__ == '__main__': 
    root = Node(27)
    root.insert(14)
    root.insert(35)
    root.insert(10)
    root.insert(19)
    root.insert(31)
    root.insert(42)
    print(root.inorderTraversal(root))
    print(root.PreorderTraversal(root))
    print(root.PostorderTraversal(root))

