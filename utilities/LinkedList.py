"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the LinkedList class.

The LinkedList class is a data structure that contains a list of nodes. Each node contains a data and a pointer to
the next node. The LinkedList class is used to store the patient's IDs and the scans associated with it.

This linked list is a singly linked list, meaning that each node only has a pointer to the next node. The last node
points to None. Each Node also contains a key attribute that is used to identify the node. The key attribute is
used to link the the patient's ID to the scans associated with it.

To make sure that the LinkedList class is used properly, the Node class is defined inside the LinkedList class.

The pointer attribute is reset both at the beginning and at the end of the function that uses it.
This is done to avoid any error when using the LinkedList class.
"""
import sys


class LinkedList:
    """
    Class containing a data structure to store the patient's IDs and the scans associated with it.
    """

    # Class Node starts here
    class _EmptyKey(Exception):
        def __init__(self, message: str = "The key cannot be empty."):
            super().__init__(message)

    class _Node:
        """
        Internal class that contain the definition of the Node for the link list.
        """

        def __init__(self, data=None, next_node=None, key: str = "None"):
            """
            Constructor for the Node class.
            :param data: Data to be stored in the node.
            :param next_node: Pointer to the next node.
            """

            self.data = data
            self.next = next_node
            self.key = key

        @property
        def data(self):
            """
            Getter for the data attribute.
            :return: Data stored in the node.
            """
            return self.data

        @data.setter
        def data(self, data):
            """
            Setter for the data attribute.
            :param data: Data to be stored in the node.
            """
            if data is None:
                raise ValueError("Data cannot be None. Delete the node instead.")
            self.data = data

        @property
        def next(self):
            """
            Getter for the next attribute.
            :return: Pointer to the next node.
            """
            return self.next

        @next.setter
        def next(self, next_node):
            """
            Setter for the next attribute.
            :param next_node: Pointer to the next node.
            """
            self.next = next_node

        @property
        def key(self):
            """
            Getter for the key attribute.
            :return: key of the node.
            """
            return self.key

        @key.setter
        def key(self, key):
            """
            Setter for the key attribute.
            :param key: key of the node.
            """
            self.key = key

        def __eq__(self, other):
            """
            Overloading the == operator to compare two nodes.
            :param other: Node to compare with.
            :return: Boolean
            """

            if not isinstance(other, self.__class__):
                return False

            return self.data == other.data and self.key == other.key

        def __str__(self):
            """
            Overloading the str operator to print the node.
            :return: String
            """
            return f"Node:  {str(self.key)}: " + str(self.data)

        def __sizeof__(self):
            """
            Overloading the sizeof operator to return the size of the node.
            :return: Size of the data stored in the Node.
            """
            return self.data.__sizeof__()

        # Class Node ends here

    # Class LinkedList starts here

    def __init__(self, first_data=None, first_key: str = "None", data_tail: tuple = None,
                 data_tail_key: tuple = "None"):
        """
        Constructor for the OrderSets class.
        :param first_data: Data to be stored in the first node.
        :param first_key: key of the first node.
        :param data_tail: Data to be stored in the rest of the nodes.
        :param data_tail_key: key of the rest of the nodes. Using str(i) if not String.
        """

        # Attributes definition
        self.head = None if first_data is None else self._Node(data=first_data, key=first_key)
        self.size = 0 if self.head is None else 1
        self.pointer = self.head

        for i in range(len(data_tail)):  # Adding the rest of the data to the list if there is any
            self.size += 1
            self.__add__(data_tail[i], str(data_tail_key[i]) if i < len(data_tail_key) else str(self.size))
            # If the key is not specified, then the key is the size of the list

    def find_tail(self):
        while self.pointer.next is not None:
            self.pointer = self.pointer.next

    def __add__(self, other, key: str = "None"):
        """
        Overloading the + operator to add a new node to the list.
        """

        self.pointer = self.head

        if self.head is None:
            self.head = self._Node(data=other, key=key if key is not None else str(self.size + 1))
            self.size += 1
            return

        self.find_tail()

        self.pointer.next = self._Node(data=other, key=key if key is not None else str(self.size + 1))
        self.size += 1

        self.pointer = self.head

    def __contains__(self, item, arg: str = "None"):
        """
        :param item: item that needs to be found in the list
        :param arg: String that specify data or key. If None it searches for the key
        :return: boolean
        """
        self.pointer = self.head

        test_contain: bool = False

        if type(item) != str and (arg.lower() == "key" or arg.lower() == "None"):
            raise TypeError()

        while self.pointer is not None or test_contain is False:
            if arg.lower() == "data" and self.pointer.data == item:
                test_contain = True

            else:
                if item == self.pointer.key:
                    test_contain = True

        return test_contain

    def __delitem__(self, key: str = None):
        """
        Overloading the del operator to delete a node from the list.
        :param key:
        :return:
        """

        self.pointer = self.head

        if self.head is None:
            return

        if self.head.key == key:  # If the node to delete is the head
            self.head = self.head.next
            self.size -= 1
            return

        while self.pointer.next is not None:  # Check if the next of the node pointed is the node to delete
            if self.pointer.next.key == key:
                self.pointer.next = self.pointer.next.next
                self.size -= 1
                return
            self.pointer = self.pointer.next

        self.pointer = self.head
        print("The node does not exist", file=sys.stderr)

    def __getitem__(self, key: str = None):
        """
        Overloading the [] operator to get the data of a node.
        :param key: key of the node.
        :return: Data of the node. None if the node does not exist.
        """

        if key is None:
            return None

        self.pointer = self.head

        while self.pointer is not None:
            if self.pointer.key == key:
                self.pointer = self.head
                return self.pointer.data
            self.pointer = self.pointer.next

        self.pointer = self.head
        return None

    def __sizeof__(self):
        """
        Overloading the sizeof operator to return the size of the list.
        """
        return self.size

    def __eq__(self, other):
        """
        Overloading the == operator to compare two lists.
        :param other:
        :return:
        """

        if type(other) != LinkedList:  # Check if the other object is a LinkedList
            try:
                raise TypeError("Cannot compare a LinkedList with a non-LinkedList object.")
            except TypeError as e:
                print(e)
                return False

        if self.size != other.size:
            # Check if the two lists have the same size to
            # avoid unnecessary comparisons and error handling in the next step
            return False

        self.pointer = self.head  # Set the pointer to the head of the first list
        other.pointer = other.head

        while self.pointer is not None:
            if self.pointer != other.pointer:
                return False
            self.pointer = self.pointer.next
            other.pointer = other.pointer.next

        self.pointer = self.head  # Set the pointer to the head of the first list
        other.pointer = other.head

        return True

    def __str__(self, show_data: bool = False):
        """
        Overloading the str operator to print the list.
        :return: String with the .
        """
        string: str = f"List{{\nSize:{self.size}\nHead: {self.head}\n Nodes: "

        self.pointer = self.head

        while self.pointer is not None:
            string += f"{self.pointer.key} | "
            if show_data:
                string += f"{self.pointer.data}\n"

        self.pointer = self.head
        
        return string + "\n}"

    @property
    def head(self):
        """
        Getter for the head attribute.
        :return: Head of the list.
        """
        return self.head

    @head.setter
    def head(self, head):
        """
        Setter for the head attribute.
        :param head: Head of the list.
        """
        self.head = head

    @property
    def pointer(self):
        """
        Getter for the pointer attribute.
        :return: Pointer of the list.
        """
        return self.pointer

    @pointer.setter
    def pointer(self, pointer):
        """
        Setter for the pointer attribute.
        :param pointer: Pointer of the list.
        """
        self.pointer = pointer

    @property
    def size(self):
        """
        Getter for the size attribute.
        :return: Size of the list.
        """
        return self.size

    @size.setter
    def size(self, size):
        """
        Setter for the size attribute.
        :param size: Size of the list.
        """
        self.size = size
