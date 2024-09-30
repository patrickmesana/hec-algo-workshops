#%%
from draw_tree import draw_tree 

def insert_min_heap(heap, element):
    if len(heap) == 0:
        heap.append(element)
        return heap
    
    heap.append(element)

    child_index = len(heap) - 1
    parent_index = (child_index+1) // 2 - 1

    while heap[child_index] < heap[parent_index] and parent_index >= 0:
        tmp_element = heap[parent_index]
        heap[parent_index] = heap[child_index]
        heap[child_index] = tmp_element

        child_index = parent_index
        parent_index = (child_index+1) // 2 - 1

    return heap

#%%
h1 = []


#%%
insert_min_heap(h1, 5)

# %%
insert_min_heap(h1, 3)
# %%
draw_tree(h1)
# %%
insert_min_heap(h1, 7)
draw_tree(h1)
# %%
insert_min_heap(h1, 1)
draw_tree(h1)
# %%
