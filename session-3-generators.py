# Generators - I like to call them "lazy lists"
# 1. Generators are functions that return an iterable sequence of items. It is also an iterator.
# 2. They are defined like regular functions but use the yield statement to return data.
# 3. Each time next() is called on the generator, the generator resumes execution from where it called yield.
# 4. Generators can be used to generate large sequences of data efficiently. (e.g., infinite sequences)
# 5. Generators are memory efficient as they do not store the entire sequence in memory.
# 6. Generators are single-threaded and do not support parallel processing.


#%%
# An iterator is an object that implements the iterator protocol, which consists of the methods __iter__() and __next__().
# An iterable is an object that implements the __iter__() method, which returns an iterator object.


# A list is an iterable but not an iterator
my_list = [1, 2, 3]

# Using iter() to get an iterator from the iterable
my_iterator = iter(my_list)

# Using next() to get elements from the iterator
print(next(my_iterator))  # Output: 1

#%%


def simple_count():
    yield 1
    yield 2
    yield 3

for number in simple_count():
    print(number)
# %%

def infinite_count(start=0):
    while True:
        yield start
        start += 1

# Use `next()` to fetch values one by one
counter = infinite_count()
print(next(counter))  # Output: 0
print(next(counter))  # Output: 1

#%%

import random

# Generate a huge list of random numbers
huge_list = [random.randint(1, 100) for _ in range(10**7)]

# Using a generator to calculate the sum of squares without creating an intermediate list
def square_gen(sequence):
    for number in sequence:
        yield number ** 2

# Sum of squares using a generator (memory efficient)
gen_sum_of_squares = sum(square_gen(huge_list))

# Equivalent approach with a list comprehension (memory intensive)
list_sum_of_squares = sum([number ** 2 for number in huge_list])

# %%

import random

def random_numbers(low, high):
    while True:
        yield random.randint(low, high)

# Generate random numbers between 1 and 10
rand_gen = random_numbers(1, 10)

# Fetch and print 5 random numbers
for i in range(5):
    r = next(rand_gen)
    print(r)


#%% Generator for large sequence

def large_sequence(n):
    for i in range(n):
        yield i ** 2

# Using generator to handle large sequence
n = 10**6
gen_result = sum(large_sequence(n))

# Equivalent list comprehension (requires more memory)
list_result = sum([i ** 2 for i in range(n)])




