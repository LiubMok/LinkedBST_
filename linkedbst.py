"""
File: linkedbst.py
Author: Ken Lambert
"""
import math
import time
import random

from binary_search_tree.abstractcollection import AbstractCollection
from binary_search_tree.bstnode import BSTNode
from Stack.linkedstack import LinkedStack
import sys

sys.setrecursionlimit(10000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            return 1 + max([
                height1(top.left) if top.left else 0,
                height1(top.right) if top.right else 0
            ])

        return height1(self._root)

    def __count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self.__count_nodes(node.left) + self.__count_nodes(node.right)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * math.log2(self.__count_nodes(self._root) + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        result = []
        for element in self.inorder():
            if low <= element <= high:
                result.append(element)
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        ellemnts = [self.remove(i) for i in self.inorder()]

        def recursive(elements):
            if len(elements) == 0:
                return None
            mid = len(elements) // 2
            node = BSTNode(elements[mid])
            node.left = recursive(elements[:mid])
            node.right = recursive(elements[mid + 1:])

            return node

        self._root = recursive(ellemnts)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for element in self.inorder():
            if element > item:
                return element
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        previous = None
        for element in self.inorder():
            if element >= item:
                return previous
            previous = element
        return previous

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        def open_file(_path):
            result = []
            with open(_path, 'r', encoding='utf-8') as file:
                for line in file:
                    result.append(line.strip('\n'))
            return result

        def start_time():
            return time.process_time()

        def finish_time():
            return time.process_time()

        def list_find(words, random_wods):
            start = start_time()
            for word in random_wods:
                for word_ in words:
                    if word == word_:
                        break
            finish = finish_time()
            return finish - start

        def find_binary_order_tree(words: list, random_words):
            tree = LinkedBST()
            for word in words:
                tree.add(word)
            start = start_time()
            for r_word in random_words:
                tree.find(r_word)
            finish = finish_time()
            return finish - start

        def find_binary_not_order_tree(words: list, random_words):
            random.shuffle(words)
            tree = LinkedBST()
            for word in words:
                tree.add(word)
            start = start_time()
            for r_word in random_words:
                tree.find(r_word)
            finish = finish_time()
            return finish - start

        def find_binary_balanced_tree(words: list, random_words):
            tree = LinkedBST()
            for word in words:
                tree.add(word)
            tree.rebalance()
            start = start_time()
            for r_word in random_words:
                tree.find(r_word)
            finish = finish_time()
            return finish - start

        def main():
            whole_words = open_file(path)
            # random_words = random.sample(whole_words, 10000)
            random_words = random.sample(whole_words, 1000)
            result = ''
            result += f'1)sorted list: ' \
                      f'{list_find(whole_words, random_words)}' + '\n'
            result += f'2)ordered list transfered in tree: {find_binary_order_tree(whole_words, random_words)}' + '\n'
            result += f'3)randomly filed tree: {find_binary_not_order_tree(whole_words, random_words)}' + '\n'
            result += f'4)balanced tree: {find_binary_balanced_tree(whole_words, random_words)}'

            return result

        # return list_find(open_file(path), random.sample(open_file(path), 10000))
        return main()


if __name__ == '__main__':
    lbst = LinkedBST()
    # print(lbst.demo_bst('words.txt'))
    print(lbst.demo_bst('shorter_words'))
