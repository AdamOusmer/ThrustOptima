"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the LinkedList class.

The LinkedList class is a data structure that contains a list of nodes. Each node contains a data and a pointer to
the next node. The LinkedList class is used to store the patient's IDs and the _scans associated with it.

This linked list is a singly linked list, meaning that each node only has a pointer to the next node. The last node
points to None. Each Node also contains a key attribute that is used to identify the node. The key attribute is
used to link the the patient's ID to the _scans associated with it.

To make sure that the LinkedList class is used properly, the Node class is defined inside the LinkedList class.

The pointer attribute is reset both at the beginning and at the end of the function that uses it.
This is done to avoid any error when using the LinkedList class.
"""
import sys


class LinkedList:
    """
    Class containing a data structure to store the patient's IDs and the _scans associated with it.
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

            self._data = data
            self._next = next_node
            self._key = key

        @property
        def data(self):
            """
            Getter for the data attribute.
            :return: Data stored in the node.
            """
            return self._data

        @property
        def next(self):
            """
            Getter for the next attribute.
            :return: Pointer to the next node.
            """
            return self._next

        @property
        def key(self):
            """
            Getter for the key attribute.
            :return: key of the node.
            """
            return self._key

        def __eq__(self, other):
            """
            Overloading the == operator to compare two nodes.
            :param other: Node to compare with.
            :return: Boolean
            """

            if not isinstance(other, self.__class__):
                return False

            return self._data == other.data and self._key == other.key

        def __str__(self):
            """
            Overloading the str operator to print the node.
            :return: String
            """
            return f"Node:  {str(self._key)}: " + str(self._data)

        def __len__(self):
            """
            Overloading the sizeof operator to return the size of the node.
            :return: Size of the data stored in the Node.
            """
            return len(self._data)

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
        self._head = None if first_data is None else self._Node(data=first_data, key=first_key)
        self._size = 0 if self._head is None else 1
        self._pointer = self._head

        if data_tail is not None:
            for i in range(len(data_tail)):  # Adding the rest of the data to the list if there is any
                self._size += 1
                self.__add__(data_tail[i], str(data_tail_key[i]) if i < len(data_tail_key) else str(self._size))
                # If the key is not specified, then the key is the size of the list

    def find_tail(self):
        while self._pointer.next is not None:
            self._pointer = self._pointer.next

    def add(self, data, key: str = "None"):
        """
        Overloading the + operator to add a new node to the list.
        """

        self._pointer = self._head

        if self._head is None:
            self._head = self._Node(data=data, key=key if key != "None" else str(self._size + 1))
            self._size += 1
            return

        self.find_tail()

        self._pointer.next = self._Node(data=data, key=key if key is not None else str(self._size + 1))
        self._size += 1

        self._pointer = self._head

    def __contains__(self, item, arg: str = "None"):
        """
        :param item: item that needs to be found in the list
        :param arg: String that specify data or key. If None it searches for the key
        :return: boolean
        """
        self._pointer = self._head

        test_contain: bool = False

        if type(item) != str and (arg.lower() == "key" or arg.lower() == "None"):
            raise TypeError()

        while self._pointer is not None or test_contain is False:
            if arg.lower() == "data" and self._pointer.data == item:
                test_contain = True

            else:
                if item == self._pointer.key:
                    test_contain = True

        return test_contain

    def __delitem__(self, key: str = None):
        """
        Overloading the del operator to delete a node from the list.
        :param key:
        :return:
        """

        self._pointer = self._head

        if self._head is None:
            return

        if self._head.key == key:  # If the node to delete is the head
            self._head = self._head.next
            self._size -= 1
            return

        while self._pointer.next is not None:  # Check if the next of the node pointed is the node to delete
            if self._pointer.next.key == key:
                self._pointer.next = self._pointer.next.next
                self._size -= 1
                return
            self._pointer = self._pointer.next

        self._pointer = self._head
        print("The node does not exist", file=sys.stderr)

    def __getitem__(self, key: str = None):
        """
        Overloading the [] operator to get the data of a node.
        :param key: key of the node.
        :return: Data of the node. None if the node does not exist.
        """

        if key is None:
            return None

        self._pointer = self._head

        while self._pointer is not None:
            if self._pointer.key == key:
                self._pointer = self._head
                return self._pointer.data
            self._pointer = self._pointer.next

        self._pointer = self._head
        return None

    def __len__(self):
        """
        Overloading the sizeof operator to return the size of the list.
        :return: Size of the list.
        """
        return self._size

    def __eq__(self, other):
        """
        Overloading the == operator to compare two lists.
        :param other: List to compare with.
        :return: Boolean
        """

        if type(other) != LinkedList:  # Check if the data object is a LinkedList
            try:
                raise TypeError("Cannot compare a LinkedList with a non-LinkedList object.")
            except TypeError as e:
                print(e)
                return False

        if self._size != other.size:
            # Check if the two lists have the same size to
            # avoid unnecessary comparisons and error handling in the next step
            return False

        self._pointer = self._head  # Set the pointer to the head of the first list
        other.pointer = other.head

        while self._pointer is not None:
            if self._pointer != other.pointer:
                return False
            self._pointer = self._pointer.next
            other.pointer = other.pointer.next

        self._pointer = self._head  # Set the pointer to the head of the first list
        other.pointer = other.head

        return True

    def __str__(self, show_data: bool = False):
        """
        Overloading the str operator to print the list.
        :param show_data: Boolean to specify if the data of the nodes should be printed.
        :return: String with the list. If show_data is True, it will print the data of the nodes.
        """
        string: str = f"List{{\nSize:{self._size}\nHead: {self._head}\n Nodes: "

        self._pointer = self._head

        while self._pointer is not None:
            string += f"{self._pointer.key} | "
            if show_data:
                string += f"{self._pointer.data}\n"

        self._pointer = self._head

        return string + "\n}"

    @property
    def head(self):
        """
        Getter for the head attribute.
        :return: Head of the list.
        """
        return self._head


    @property
    def pointer(self):
        """
        Getter for the pointer attribute.
        :return: Pointer of the list.
        """
        return self._pointer


    @property
    def size(self):
        """
        Getter for the size attribute.
        :return: Size of the list.
        """
        return self._size
