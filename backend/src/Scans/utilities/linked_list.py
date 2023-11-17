"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the LinkedList class.

The LinkedList class is a data structure that contains a list of nodes. Each node contains a data and a pointer to
the _next node. The LinkedList class is used to store the patient's IDs and the _scans associated with it.

This linked list is a singly linked list, meaning that each node only has a pointer to the _next node. The last node
points to None. Each Node also contains a key attribute that is used to identify the node. The key attribute is
used to link the the patient's ID to the _scans associated with it.

To make sure that the LinkedList class is used properly, the Node class is defined inside the LinkedList class.

All functions that need a iteration through the LinkedList is done using a temporary pointer initialized to the head of
the list.
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

        def __init__(self, data=None, next_node=None, key: str = "None", range: tuple = (-1, -1)):
            """
            Constructor for the Node class.
            :param data: Data to be stored in the node.
            :param next_node: Pointer to the _next node.
            :param key: key of the node.
            """

            self._data = data
            self._next = next_node
            self._key: str = key
            self._range: tuple = range

        def clear_data_out_of_range(self):
            """
            Function to clear the data out of the range specified by the user.
            """

            self._data = [data for data in self._data if self._range[0] <= data.InstanceNumber <= self._range[1]]

        def add_to_data_list(self, data):
            """
            Function to add data to the data stored in the node. The data is added to the end of the list.
            :param data: Data to be added to the data stored in the node.
            """
            self._data.append(data)

        def order_data_dicom_time(self):
            """
            Function to order the data stored in the node by the time the data was taken.
            """
            self._data.sort(key=lambda x: x.AcquisitionTime)

        def modify_data(self, data):
            """
            Function to modify the data stored in the node.
            :param data: Data to be stored in the node.
            """
            self._data = data

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
            Getter for the _next attribute.
            :return: Pointer to the _next node.
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

        def __ne__(self, other):
            """
            Overloading the != operator to compare two Node.
            :param other:
            :return:
            """
            return not self.__eq__(other)

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
        self._size: int = 0 if self._head is None else 1

        if data_tail is not None:
            for i in range(len(data_tail)):  # Adding the rest of the data to the list if there is any
                self._size += 1
                self.add(data_tail[i], str(data_tail_key[i]) if i < len(data_tail_key) else str(self._size))
                # If the key is not specified, then the key is the size of the list

    def find_tail(self):
        pointer = self._head

        while pointer.next is not None:
            pointer = pointer.next

    def add(self, data, key: str = "None"):
        """
        Adding data to the end of the list.
        :param data: Data to be stored in the node.
        :param key: key of the node.
        """

        pointer = self._head

        if self._head is None:
            self._head = self._Node(data=data, key=key if key != "None" else str(self._size + 1))
            self._size += 1
            return

        self.find_tail()

        pointer._next = self._Node(data=data, key=key if key is not None else str(self._size + 1))
        self._size += 1

    def add_to_data(self, data, key: str = "None"):
        """
        Adding data to a node based on the key.
        :param data: Data to be added to the data stored in the node.
        :param key: key of the node.
        """
        pointer = self._head

        if self._head is None:
            raise IndexError("The list is empty")

        if self._head.key == key:
            self._head.add_to_data_list(data)
            return

        while pointer is not None:
            if pointer.key == key:
                pointer.add_to_data_list(data)
                return
            pointer = pointer.next

    def modify_data(self, data, key: str = "None"):
        """
        Modifying the data stored in a node based on the key.
        :param data: Data to be stored in the node.
        :param key: key of the node.
        """

        pointer = self._head

        if self._head is None:
            raise IndexError("The list is empty")

        while pointer is not None:
            if pointer.key == key:
                pointer.modify_data(data)
                return
            pointer = pointer.next

    def get_node(self, key: str = "None"):
        """
        Getting a node based on the key.
        :param key: key of the node.
        :return: Node
        """

        pointer = self._head

        if self._head is None:
            raise IndexError("The list is empty")

        if self._head.key == key:
            return self._head

        while pointer is not None:
            if pointer.key == key:
                pointer = self._head
                return pointer
            pointer = pointer.next

    def get_keys(self):
        """
        Function that return an array with all the keys of each Node contained in the LinkedList
        :return: array of strings
        """

        if self._head is None:
            return None

        pointer = self._head

        arr = []

        while pointer is not None:
            arr.append(pointer.key)
            pointer = pointer.next

        return arr

    def order_data_dicom_time(self):
        """
        Function to order the data stored in the node by the time the data was taken.
        """
        pointer = self._head

        while pointer is not None:
            pointer.order_data_dicom_time()
            pointer = pointer.next


    def order_node_data_dicom_time(self, key):
        """
        Function to order the data stored in the node by the time the data was taken.
        """
        pointer = self._head

        while pointer is not None:
            if pointer.key == key:
                pointer.order_data_dicom_time()
                return

            pointer = pointer.next


    def clear_data_out_of_range(self, clear_all: bool = False, key: str = None):
        """
        Function to clear the data out of the range specified by the user.
        :param clear_all: Boolean to specify if all the data in every node of the Linked List should be cleared.
        :param key: key of the node to clear.
        """

        pointer = self._head

        while pointer is not None:

            if clear_all or pointer.key == key:
                pointer.clear_data_out_of_range()
            pointer = pointer.next


    def __contains__(self, item, arg: str = "None"):
        """
        Overloading the in operator to check if an item is in the list.
        :param item: item that needs to be found in the list
        :param arg: String that specify data or key. If None it searches for the key
        :return: boolean
        """
        pointer = self._head

        test_contain: bool = False

        if type(item) != str and (arg.lower() == "key" or arg.lower() == "None"):
            raise TypeError()

        while pointer is not None or test_contain is False:
            if arg.lower() == "data" and pointer.data == item:
                test_contain = True

            else:
                if item == pointer.key:
                    test_contain = True

        return test_contain

    def __next__(self):
        """
        Overloading the next operator to iterate through the list.
        :return: Iterator
        """
        pointer = self._head

        if pointer is None:
            raise StopIteration
        else:
            pointer = pointer.next
            return pointer

    def __delitem__(self, key: str = None):
        """
        Overloading the del operator to delete a node from the list.
        :param key:
        :return:
        """

        pointer = self._head

        if self._head is None:
            return

        if self._head.key == key:  # If the node to delete is the head
            self._head = self._head.next
            self._size -= 1
            return

        while pointer.next is not None:  # Check if the _next of the node pointed is the node to delete
            if pointer.next.key == key:
                pointer.next = pointer.next.next
                self._size -= 1
                return
            pointer = pointer.next

        print("The node does not exist", file=sys.stderr)

    def __getitem__(self, key: str = None):
        """
        Overloading the [] operator to get the data of a node.
        :param key: key of the node.
        :return: Data of the node. None if the node does not exist.
        """

        if key is None:
            return None

        pointer = self._head

        while pointer is not None:
            if pointer.key == key:
                pointer = self._head
                return pointer.data
            pointer = pointer.next

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
            # avoid unnecessary comparisons and error handling in the _next step
            return False

        pointer = self._head  # Set the pointer to the head of the first list
        other.pointer = other.head

        while pointer is not None:
            if pointer != other.pointer:
                return False
            pointer = pointer.next
            other.pointer = other.pointer.next

        pointer = self._head  # Set the pointer to the head of the first list
        other.pointer = other.head

        return True

    def __ne__(self, other):
        """
        Overloading the != operator to compare two lists.
        :param other:
        :return:
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        Overloading the str operator to print the list.
        :return: String with the list. If show_data is True, it will print the data of the nodes.
        """
        if self._head is None:
            return "List{\t\nSize: 0\nHead: None\n Nodes: None\n}"

        string: str = f"List{{\n\tSize:{self._size}\n\tHead: {self._head}\n\tNodes: "

        pointer = self._head

        while pointer is not None:
            string += f"{pointer.key} | "
            string += f"{pointer.data}\n"
            pointer = pointer.next

        return string + "\n}"

    def __repr__(self):
        """
        Overloading the repr operator to print the list.
        :return: String with the list.
        """
        if self._head is None:
            return "List{\t\nSize: 0\nHead: None\n Nodes: None\n}"

        string: str = f"List{{\n\tSize:{self._size}\n\tNodes: "

        pointer = self._head

        while pointer is not None:
            string += f"{pointer.key} - {len(pointer)}| "
            pointer = pointer.next

        return string + "\n}"

    def __iter__(self):
        """
        Overloading the iter operator to iterate through the list.
        :return: Iterator of the list.
        """
        return self

    @property
    def head(self):
        """
        Getter for the head attribute.
        :return: Head of the list.
        """
        return self._head

    @property
    def size(self):
        """
        Getter for the size attribute.
        :return: Size of the list.
        """
        return self._size
