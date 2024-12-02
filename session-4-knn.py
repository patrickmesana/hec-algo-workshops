#%%

# k-Nearest Neighbors (kNN) Implementation in Python with Visualization

# This script contains two implementations of the kNN algorithm:
# 1. Naive implementation
# 2. KD-tree implementation with pre-sorted dimensions

# We will use a synthetic 2D dataset and use matplotlib to visualize
# the decision boundaries to explain how kNN works.

import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
from dataclasses import dataclass

# Generate a synthetic 2D dataset
def generate_dataset(num_points):
    dataset = []
    for _ in range(num_points):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        # Define labels based on a simple function for visualization
        label = 1 if x * y >= 0 else 0  # Label 1 if x and y have the same sign
        dataset.append({'point': (x, y), 'label': label})
    return dataset

# Euclidean distance between two points in 2D
def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# ------------------------------------------------------------
# 1. Naive kNN Implementation
# ------------------------------------------------------------

def naive_knn(training_data, query_point, k):
    distances = []
    # Compute distance from the query point to all training data
    for data in training_data:
        distance = euclidean_distance(query_point, data['point'])
        distances.append({'distance': distance, 'label': data['label']})
    
    # Sort the distances
    distances.sort(key=lambda x: x['distance'])  # O(N log N)
    
    # Get the labels of the k nearest neighbors
    k_nearest_labels = [distances[i]['label'] for i in range(k)]
    
    # Majority vote
    prediction = max(set(k_nearest_labels), key=k_nearest_labels.count)
    return prediction

# Complexity Analysis:
# For each query:
# - Computing distances: O(N)
# - Sorting distances: O(N log N)
# Total complexity per query: O(N log N)

# ------------------------------------------------------------
# 2. KD-tree kNN Implementation with Pre-sorted Dimensions
# ------------------------------------------------------------

@dataclass
class KDNode:
    point: tuple
    label: int
    axis: int
    left: 'KDNode' = None
    right: 'KDNode' = None

# Build KD-tree with pre-sorted dimensions
def build_kdtree(points_by_axis, depth=0, dims_nbr=2):
    if not points_by_axis[0]:
        return None

    axis = depth % dims_nbr
    points_sorted_axis = points_by_axis[axis]
    median_idx = len(points_sorted_axis) // 2
    median_point = points_sorted_axis[median_idx]

    # Partition the data into left and right subsets
    left_points_by_axis = [[] for _ in range(dims_nbr)]
    right_points_by_axis = [[] for _ in range(dims_nbr)]

    for dim in range(dims_nbr):
        points_sorted = points_by_axis[dim]
        left_points = []
        right_points = []
        for point in points_sorted:
            if point['point'][axis] < median_point['point'][axis]:
                left_points.append(point)
            elif point['point'][axis] > median_point['point'][axis]:
                right_points.append(point)
            else:
                if point != median_point:
                    # Handle duplicates (equal to median point)
                    # Distribute evenly to maintain balance
                    if dim == axis:
                        index = points_sorted.index(point)
                        if index < median_idx:
                            left_points.append(point)
                        else:
                            right_points.append(point)
                    else:
                        # For other axes, we decide based on the median point's coordinate
                        if point['point'][dim] < median_point['point'][dim]:
                            left_points.append(point)
                        else:
                            right_points.append(point)
        left_points_by_axis[dim] = left_points
        right_points_by_axis[dim] = right_points

    return KDNode(
        point=median_point['point'],
        label=median_point['label'],
        axis=axis,
        left=build_kdtree(left_points_by_axis, depth + 1, dims_nbr),
        right=build_kdtree(right_points_by_axis, depth + 1, dims_nbr)
    )

# KD-tree kNN search remains the same
def kdtree_knn(root, query_point, k):
    # Helper function to search the KD-tree
    def search_knn(node, depth=0):
        if node is None:
            return
        
        axis = node.axis
        next_branch = None
        opposite_branch = None
        
        # Decide which branch to search
        if query_point[axis] < node.point[axis]:
            next_branch = node.left
            opposite_branch = node.right
        else:
            next_branch = node.right
            opposite_branch = node.left
        
        # Search the next branch
        search_knn(next_branch, depth + 1)
        
        # Update best points
        distance = euclidean_distance(query_point, node.point)
        if len(best_points) < k:
            best_points.append({'distance': distance, 'label': node.label})
            best_points.sort(key=lambda x: x['distance'])
        elif distance < best_points[-1]['distance']:
            best_points[-1] = {'distance': distance, 'label': node.label}
            best_points.sort(key=lambda x: x['distance'])
        
        # Check if we need to search the opposite branch
        if len(best_points) < k or abs(query_point[axis] - node.point[axis]) < best_points[-1]['distance']:
            search_knn(opposite_branch, depth + 1)
    
    best_points = []
    search_knn(root)
    k_nearest_labels = [item['label'] for item in best_points]
    prediction = max(set(k_nearest_labels), key=k_nearest_labels.count)
    return prediction

# Complexity Analysis:
# - Building the KD-tree: O(N log N) due to pre-sorting and partitioning
# - Each query: O(log N)
# Total complexity per query after building the tree: O(log N)

# ------------------------------------------------------------
# Visualization Functions
# ------------------------------------------------------------

# Plot the dataset
def plot_dataset(training_data):
    x0 = [data['point'][0] for data in training_data if data['label'] == 0]
    y0 = [data['point'][1] for data in training_data if data['label'] == 0]
    x1 = [data['point'][0] for data in training_data if data['label'] == 1]
    y1 = [data['point'][1] for data in training_data if data['label'] == 1]
    
    plt.scatter(x0, y0, c='red', label='Class 0', alpha=0.5)
    plt.scatter(x1, y1, c='blue', label='Class 1', alpha=0.5)
    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Synthetic 2D Dataset')
    plt.show()

# Plot decision boundaries
def plot_decision_boundary(training_data, k, algorithm='naive'):
    # Create a mesh grid
    h = 0.2
    x_min, x_max = -10, 10
    y_min, y_max = -10, 10
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # Flatten the grid to pass to the classifier
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    
    # Predict labels for each point in the grid
    Z = []
    if algorithm == 'naive':
        for point in grid_points:
            label = naive_knn(training_data, point, k)
            Z.append(label)
    elif algorithm == 'kdtree':
        # Pre-sort the dataset
        points_by_axis = []
        for dim in range(2):
            sorted_points = sorted(training_data, key=lambda x: x['point'][dim])
            points_by_axis.append(sorted_points)
        kd_tree = build_kdtree(points_by_axis)
        for point in grid_points:
            label = kdtree_knn(kd_tree, point, k)
            Z.append(label)
    else:
        raise ValueError("Algorithm must be 'naive' or 'kdtree'")
    
    Z = np.array(Z).reshape(xx.shape)
    
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.coolwarm)
    x0 = [data['point'][0] for data in training_data if data['label'] == 0]
    y0 = [data['point'][1] for data in training_data if data['label'] == 0]
    x1 = [data['point'][0] for data in training_data if data['label'] == 1]
    y1 = [data['point'][1] for data in training_data if data['label'] == 1]
    
    plt.scatter(x0, y0, c='red', label='Class 0', edgecolor='k')
    plt.scatter(x1, y1, c='blue', label='Class 1', edgecolor='k')
    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'kNN Decision Boundary (k={k}, Algorithm={algorithm})')
    plt.show()



#%%
# Generate dataset
num_training_points = 200  # Adjust this number to scale the dataset
training_data = generate_dataset(num_training_points)

# Visualize the dataset
plot_dataset(training_data)


#%%
# Set k value
k = 5  # Number of nearest neighbors

#%%
# Plot decision boundary using naive kNN
print("Plotting decision boundary using naive kNN...")
start_time = time.time()
plot_decision_boundary(training_data, k, algorithm='naive')
naive_plot_time = time.time() - start_time
print(f"Naive kNN Plot Time: {naive_plot_time:.2f} seconds\n")


#%%
# Plot decision boundary using KD-tree kNN
print("Plotting decision boundary using KD-tree kNN...")
start_time = time.time()
plot_decision_boundary(training_data, k, algorithm='kdtree')
kdtree_plot_time = time.time() - start_time
print(f"KD-tree kNN Plot Time: {kdtree_plot_time:.2f} seconds\n")

