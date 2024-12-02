# Generators - I like to call them "lazy lists"
# 1. Generators are functions that return an iterable sequence of items. It is also an iterator.
# 2. They are defined like regular functions but use the yield statement to return data.
# 3. Each time next() is called on the generator, the generator resumes execution from where it called yield.
# 4. Generators can be used to generate large sequences of data efficiently. (e.g., infinite sequences)
# 5. Generators are memory efficient as they do not store the entire sequence in memory.
# 6. Generators are single-threaded and do not support parallel processing.


#%%

a = [1, 2, 3, 4, 5]

a_iterator = iter(a)

print(next(a_iterator))
print(next(a_iterator))

# %%

for e in a_iterator:
    print(e)
# %%


def simple_count():
    yield 1
    yield 2
    yield 3
# %%

gen_a = simple_count()

print(next(gen_a))

# %%

next(gen_a)

#%%
n = 10**7
#%%
# Equivalent list comprehension (requires more memory)
list_result = sum([i ** 2 for i in range(n)])

#%%

list = [i ** 2 for i in range(n)]

#%%
list_result = sum(list)



# %%
def large_sequence(n):
    previous_result = 0
    for i in range(n):
        previous_result = i ** 2 + previous_result
        yield previous_result

# Using generator to handle large sequence

gen_result = large_sequence(n)
gen_result


# %%
