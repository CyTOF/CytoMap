#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 16:29:22 2019

@author: anibaljt
"""

class Node:
    
    def __init__(self, data):
       self.data = data
       self.next = None

 
class LinkedList:
    
    def __init__(self):
        self.first = None
        self.last = None
 
    def get_node(self, index):
        current = self.first
        for i in range(index):
            if current is None:
                return None
            current = current.next
        return current
 
    
    def insert_after(self, ref_node, new_node):
        if ref_node.next is None:
            self.last = new_node
        else:
            new_node.next = ref_node.next
        ref_node.next = new_node
 
    def insert_before(self, ref_node, new_node):
        new_node.next = ref_node
      
    
 
    def insert_at_beginning(self, new_node):
        if self.first is None:
            self.first = new_node
            self.last = new_node
        else:
            self.insert_before(self.first, new_node)
 
    def insert_at_end(self, new_node):
        if self.last is None:
            self.last = new_node
            self.first = new_node
        else:
            self.insert_after(self.last, new_node)
 
    def remove(self, node):
        if node.prev is None:
            self.first = node.next
        else:
            node.prev.next = node.next
 

 
    def display(self):
        current = self.first
        while current:
            print(current.data, end = ' ')
            current = current.next
 
