# What is the purpose of a heap?
# Find the max or min element quickly
# How?
# Maintain the heap property : parent is greater than child
# What is the time complexity of heap operations?
# Insertion: O(log n)
# Deletion: O(log n)
# Heapify: O(n)

#%%
from draw_tree import draw_tree 

#%% Basic implementation using only functions

def heap_min_insert(heap, element):

    if len(heap) == 0:
        heap.append(element)
        return heap
    

    heap.append(element)


    child_index = len(heap) - 1
    parent_index = (child_index+1) // 2 - 1
    # parent_index = (child_index - 1) // 2

    # Swapping position if parent is smaller than child (Heapifying up)
    while  heap[parent_index] > heap[child_index]:

        heap[parent_index], heap[child_index] = heap[child_index], heap[parent_index]

        child_index = parent_index
        parent_index = (child_index+1) // 2 - 1


        if parent_index < 0:
            break


    return heap
    

h1 = []

h1 = heap_min_insert(h1, 6)

# draw_tree(h1)

h1 = heap_min_insert(h1, 4)

# draw_tree(h1)

h1 = heap_min_insert(h1, 3)

# draw_tree(h1)

h1 = heap_min_insert(h1, 2)

draw_tree(h1)
# %%

from random import randint

random_integers = [randint(0, 100) for _ in range(15)]

h2 = []
for el in random_integers:
    heap_min_insert(h2, el)

draw_tree(h2)

# %%
def heap_min_delete(heap):
    if len(heap) == 0:
        return None  # No elements to delete

    # Replace the root with the last element
    root_value = heap[0]
    last_element = heap.pop()  # Remove the last element from the heap

    if len(heap) > 0:
        heap[0] = last_element  # Move the last element to the root
        heapify_down(heap, 0)   # Restore the min-heap property

    return root_value


def heapify_down(heap, index):
    child_index_left = 2 * index + 1
    child_index_right = 2 * index + 2
    smallest_index = index

    # Check if the left child exists and is smaller than the current element
    if child_index_left < len(heap) and heap[child_index_left] < heap[smallest_index]:
        smallest_index = child_index_left

    # Same for the right
    if child_index_right < len(heap) and heap[child_index_right] < heap[smallest_index]:
        smallest_index = child_index_right

    # If the smallest element is not the current element, swap and continue heapifying down
    if smallest_index != index:
        heap[index], heap[smallest_index] = heap[smallest_index], heap[index]
        heapify_down(heap, smallest_index)



# Delete the root (min element)
min_value = heap_min_delete(h2)

# Draw the heap after deletion
draw_tree(h2)
# %% Object Oriented Version

from abc import ABC, abstractmethod

class Heap(ABC):
    def __init__(self):
        self.heap = []

    def insert(self, element):
        """Insert an element into the heap."""
        self.heap.append(element)
        child_index = len(self.heap) - 1
        self._heapify_up(child_index)

    def delete_root(self):
        """Delete and return the root element from the heap (min or max depending on the heap type)."""
        if len(self.heap) == 0:
            return None  # No elements to delete

        # Replace the root with the last element
        root_element = self.heap[0]
        last_element = self.heap.pop()

        if len(self.heap) > 0:
            self.heap[0] = last_element  # Move the last element to the root
            self._heapify_down(0)  # Restore the heap property

        return root_element

    @abstractmethod
    def compare(self, parent, child):
        """Abstract method for comparing parent and child elements. 
        Must be implemented in subclasses (min-heap or max-heap).
        Returns True if parent should be swapped with the child."""
        pass

    def _heapify_up(self, index):
        """Restore the heap property by heapifying up."""
        parent_index = (index - 1) // 2

        while index > 0 and self.compare(self.heap[parent_index], self.heap[index]):
            # Swap parent and child
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            # Move up to the parent node
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        """Restore the heap property by heapifying down."""
        child_index_left = 2 * index + 1
        child_index_right = 2 * index + 2
        smallest_or_largest = index

        # Compare with the left child
        if child_index_left < len(self.heap) and self.compare(self.heap[smallest_or_largest], self.heap[child_index_left]):
            smallest_or_largest = child_index_left

        # Compare with the right child
        if child_index_right < len(self.heap) and self.compare(self.heap[smallest_or_largest], self.heap[child_index_right]):
            smallest_or_largest = child_index_right

        # If the smallest or largest is not the current index, swap and continue heapifying down
        if smallest_or_largest != index:
            self.heap[index], self.heap[smallest_or_largest] = self.heap[smallest_or_largest], self.heap[index]
            self._heapify_down(smallest_or_largest)

    def get_root(self):
        """Get the root element without deleting it (min or max depending on heap type)."""
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    def size(self):
        """Return the current size of the heap."""
        return len(self.heap)

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def draw(self):
        """Use the external draw_tree function to visualize the heap."""
        draw_tree(self.heap)

class MinHeap(Heap):
    def compare(self, parent, child):
        """In a min-heap, the parent must be smaller than the child. Return True if a swap is needed."""
        return parent > child
    
# Example usage of the MinHeap class

heap = MinHeap()

# Insert elements into the heap
heap.insert(6)
heap.insert(4)
heap.insert(3)
heap.insert(2)


heap.draw()

# Delete the minimum element (root)
min_element = heap.delete_root()


# Draw the heap after deletion
heap.draw()
# %%
