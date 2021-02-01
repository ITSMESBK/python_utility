# =========================================================================================
# !/usr/bin/env python3
# Filename: simple_linkedlist.py
# Description:Implementation of Simple Linked List 
# Author: Bharathkumar Sivakumar <BHARATH SBK @ITSMESBK>
# Python Environment - Python3
# Usage: To be used as a alternate way to store a data instead of list | Linked list 
# ===========================================================================================

# Node class 
class Node: 
	
	# Function to initialise the node object 
	def __init__(self, data): 
		self.data = data # Assign data 
		self.next = None # Initialize next as null 

# Linked List class 
class LinkedList: 
	def __init__(self): 
		self.head = None # Initialize head as None 
	
	# Get a list of values and push each value to node
	def compute_list(self,input_list):
		[llist.push_data_to_node(value) for value in input_list]#Iterate over list 

	# This function insert a new node at the 
	# beginning of the linked list 
	def push_data_to_node(self, new_data): 
	
		# Create a new Node 
		new_node = Node(new_data) 

		# 3. Make next of new Node as head 
		new_node.next = self.head 

		# 4. Move the head to point to new Node 
		self.head = new_node 
	
	# This Function checks whether the value 
	# x present in the linked list 
	def get_traverse_data(self): 
		# Initialize current to head 
		current = self.head 

		# loop till current not equal to None 
		while current != None: 
			print(current.data)
			current = current.next

# Code execution starts here 
if __name__ == '__main__': 

	#input_list = [1,2,3,4,5] #Sample Input
	llist = LinkedList() 
	llist.compute_list(input_list)
	llist.get_traverse_data()