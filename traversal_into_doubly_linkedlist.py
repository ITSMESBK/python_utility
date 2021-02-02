# =========================================================================================
# !/usr/bin/env python3
# Filename: traversal_into_doubly_linkedlist.py
# Description:Implementation of doubly Linked List | Previous reference / Next Reference  
# Author: Bharathkumar Sivakumar <BHARATH SBK @ITSMESBK>
# Python Environment - Python3
# Usage: To be used as a alternate way to store a data instead of list | Linked list 
# ===========================================================================================

class Node:
	def __init__(self, data):
		self.data = data
		self.nref = None
		self.pref = None

class DoublyLinkedList:
	def __init__(self):
		self.head = None

	def insert_in_emptylist(self, data):
		if self.head is None:
			new_node = Node(data)
			self.head = new_node
		else:
			print("list is not empty")
	
	def insert_at_start(self, data):
		if self.head is None:
			new_node = Node(data)
			self.head = new_node
			print("node inserted")
			return
		new_node = Node(data)
		new_node.nref = self.head
		self.head.pref = new_node
		self.head = new_node

	def insert_at_end(self, data):
		if self.head is None:
			new_node = Node(data)
			self.head = new_node
			return
		n = self.head
		while n.nref is not None:
			n = n.nref
		new_node = Node(data)
		n.nref = new_node
		new_node.pref = n
	
	def insert_after_data(self, x, data):
		if self.head is None:
			print("List is empty")
			return
		else:
			n = self.head
			while n is not None:
				if n.data == x:
					break
				n = n.nref
			if n is None:
				print("data not in the list")
			else:
				new_node = Node(data)
				new_node.pref = n
				new_node.nref = n.nref
				if n.nref is not None:
					n.nref.prev = new_node
				n.nref = new_node

	def insert_before_data(self, x, data):
		if self.head is None:
			print("List is empty")
			return
		else:
			n = self.head
			while n is not None:
				if n.data == x:
					break
				n = n.nref
			if n is None:
				print("data not in the list")
			else:
				new_node = Node(data)
				new_node.nref = n
				new_node.pref = n.pref
				if n.pref is not None:
					n.pref.nref = new_node
				n.pref = new_node            
	
	def traverse_list(self):
		if self.head is None:
			print("List has no element")
			return
		else:
			n = self.head
			while n is not None:
				print(n.data , " ")
				n = n.nref

	def delete_at_start(self):
		if self.head is None:
			print("The list has no element to delete")
			return 
		if self.head.nref is None:
			self.head = None
			return
		self.head = self.head.nref
		self.start_prev = None

	def delete_at_end(self):
		if self.head is None:
			print("The list has no element to delete")
			return 
		if self.head.nref is None:
			self.head = None
			return
		n = self.head
		while n.nref is not None:
			n = n.nref
		n.pref.nref = None 
	
	def delete_element_by_value(self, x):
		if self.head is None:
			print("The list has no element to delete")
			return 
		if self.head.nref is None:
			if self.head.data == x:
				self.head = None
			else:
				print("data not found")
			return 

		if self.head.data == x:
			self.head = self.head.nref
			self.head.pref = None
			return

		n = self.head
		while n.nref is not None:
			if n.data == x:
				break
			n = n.nref
		if n.nref is not None:
			n.pref.nref = n.nref
			n.nref.pref = n.pref
		else:
			if n.data == x:
				n.pref.nref = None
			else:
				print("Element not found")   

# Code execution starts here 
if __name__ == '__main__': 

	#input_list = [1,2,3,4,5] #Sample Input
	llist = DoublyLinkedList() 
	llist.insert_in_emptylist(50)
	llist.traverse_list()
	llist.insert_at_start(10)
	llist.insert_at_start(5)
	llist.insert_at_start(18)
	llist.insert_after_data(50, 65)
	llist.insert_before_data(23,45)
	llist.delete_at_start()
	llist.delete_at_end()
	llist.delete_element_by_value(65)