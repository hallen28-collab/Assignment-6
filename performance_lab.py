# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

def most_frequent(numbers):
    if not numbers:
        return None

    counts = {}
    best_value = numbers[0]
    best_count = 0
    for n in numbers:
        counts[n] = counts.get(n, 0) + 1
        if counts[n] > best_count:
            best_count = counts[n]
            best_value = n
    return best_value

'''
- Best-case: O(n). Even if every element is the same, we still have to look at
  each one once to know that.
- Worst-case: O(n). One pass; each dictionary get/set is O(1) on average.
  (Hash collisions could degrade a single operation to O(n), but that is
  extremely rare with Python's integer hashing.)
- Average-case: O(n).
- Space complexity: O(k), where k is the number of distinct values (O(n) in the
  worst case when all values are unique; O(1) if all values are the same).
- Why this approach? A dictionary lets me count each value in constant time, so
  I only need a single pass. The naive alternative (for each element, count how
  many times it appears using list.count) is O(n^2). I also track the best
  value as I go, so I don't need a second pass over the dictionary.
- Could it be optimized? Not in time: any correct solution must read every
  element, so O(n) is optimal. Space could be reduced to O(1) with the
  Boyer-Moore voting algorithm, but that only works when a strict majority
  element is guaranteed, which isn't promised here. Trade-off: less memory,
  but a much narrower set of inputs it can handle
'''

# 🔍 Problem 2: Remove Duplicates While Preserving Order

# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()
    result = []
    for n in nums:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result


"""
- Best-case: O(n). Even if every element is the same, we still have to look at
  each one once to know that.
- Worst-case: O(n). One pass; each dictionary get/set is O(1) on average.
  (Hash collisions could degrade a single operation to O(n), but that is
  extremely rare with Python's integer hashing.)
- Average-case: O(n).
- Space complexity: O(k), where k is the number of distinct values (O(n) in the
  worst case when all values are unique; O(1) if all values are the same).
- Why this approach? A dictionary lets me count each value in constant time, so
  I only need a single pass. The naive alternative (for each element, count how
  many times it appears using list.count) is O(n^2). I also track the best
  value as I go, so I don't need a second pass over the dictionary.
- Could it be optimized? Not in time: any correct solution must read every
  element, so O(n) is optimal. Space could be reduced to O(1) with the
  Boyer-Moore voting algorithm, but that only works when a strict majority
  element is guaranteed, which isn't promised here. Trade-off: less memory,
  but a much narrower set of inputs it can handle
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

def find_pairs(nums, target):
    seen = set()
    pairs = []
    for n in nums:
        complement = target - n
        if complement in seen:
            pairs.append((min(n, complement), max(n, complement)))
        seen.add(n)
    return pairs

def find_pairs_brute_force(nums, target):
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((min(nums[i], nums[j]), max(nums[i], nums[j])))
    return pairs

"""
Time and Space Analysis for problem 3:
- Best-case: O(n) for the optimized version (always one full pass). The brute
  force version is O(n^2) in every case: it always checks all n(n-1)/2 pairs.
- Worst-case: O(n). Each iteration does one O(1) average set lookup and add.
- Average-case: O(n).
- Space complexity: O(n) for the seen set, plus the output list (up to n/2
  pairs). Brute force uses only O(1) extra space beyond the output.
- Why this approach? If a + b = target then b = target - a, so I ask "have I
  already seen the complement?" instead of comparing against every other
  number. Since the input has no duplicates, each valid pair is found exactly
  once (when its second number is reached), so there are no repeated pairs.
- Could it be optimized? Time is already optimal at O(n). Sorting plus a
  two-pointer scan is O(n log n) time but O(1) extra space, which is better
  when memory is tight. Trade-off: slower time for less memory, and it needs
  a sorted copy (or mutates the input).
 
OPTIMIZE ONE: performance and space comparison (brute force vs. optimized).
Measured with test_optimization_comparison() at the bottom of this file, using
random lists of unique integers:
  n = 2,000   brute force: ~0.080 s    optimized: ~0.0003 s
  n = 4,000   brute force: ~0.32 s     optimized: ~0.0006 s
  n = 8,000   brute force: ~1.27 s     optimized: ~0.0012 s
Doubling n roughly quadruples the brute force time (quadratic) but only about
doubles the optimized time (linear). Space: brute force uses O(1) extra; the
optimized version uses O(n) for the set, which is only a few hundred KB for
8,000 integers. This is the same kind of fix as the GTA Online loading bug.
"""


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n):
    capacity = 2
    storage = [None] * capacity
    size = 0

    for i in range(n):
        if size == capacity:
            new_capacity = capacity * 2
            new_storage = [None] * new_capacity
            for j in range(size):
                new_storage[j] = storage[j]
            print(f"Resize! Capacity {capacity} -> {new_capacity}"
                  f"(copied {size} items before adding item #{i + 1})")
            storage = new_storage
            capacity = new_capacity
        storage[size] = i
        size += 1

    return storage[:size]

"""
Time and Space Analysis for problem 4:
- When do resizes happen? When the list is full and we try to add another item.
  With initial capacity 2, that is when adding items #3, #5, #9, #17, ... (the
  list holds 2, 4, 8, 16, ... items). That is only about log2(n) resizes total.
- What is the worst-case for a single append? O(n): the append that triggers a
  resize has to copy all n existing items into the new list.
- What is the amortized time per append overall? O(1). The total copy work for
  n appends is 2 + 4 + 8 + ... which is less than 2n, so total work is O(n),
  and O(n) / n appends = O(1) per append on average.
- Space complexity: O(n). Capacity is at most 2x the number of items, and the
  old list briefly exists alongside the new one during a copy (still O(n)).
- Why does doubling reduce the cost overall? Each resize costs twice as much as
  the last, but resizes become exponentially rarer, so the copying cost
  spreads out to a constant amount per append. Growing by a fixed amount
  (e.g., +10 slots) would resize every 10 appends and copy ~n items each time,
  giving O(n^2) total work and O(n) amortized per append.
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    totals = []
    running = 0
    for n in nums:
        running += n
        totals.append(running)
    return totals

"""
Time and Space Analysis for problem 5:
- Best-case: O(n). Even all zeros requires visiting every element. (An empty
  list is trivially O(1).)
- Worst-case: O(n). One pass with one addition and one append per element
  (append is amortized O(1), see problem 4).
- Average-case: O(n).
- Space complexity: O(n) for the output list; O(1) auxiliary beyond that.
- Why this approach? Each total is the previous total plus the current number,
  so I carry the sum forward instead of re-adding from the start. The naive
  approach, sum(nums[:i+1]) at every index, is O(n^2).
- Could it be optimized? Time can't beat O(n) since every element is read and
  every output is written. itertools.accumulate does the same thing in C, so
  it is faster in practice with the same Big-O. Updating the input in place
  would cut extra space to O(1), but it would mutate (lose) the original
  list. Trade-off: memory vs. preserving the caller's data.
"""

import io
import random
import time
from contextlib import redirect_stdout
 
 
def test_most_frequent():
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3
    assert most_frequent([7]) == 7                       
    assert most_frequent([]) is None                     
    assert most_frequent([5, 5, 5, 5]) == 5              
    assert most_frequent([1, 2, 1, 2]) in (1, 2)         
    assert most_frequent([-1, -1, 2, 3]) == -1           
    assert most_frequent([1, 2, 3, 4]) in (1, 2, 3, 4)    
 
def test_remove_duplicates():
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]
    assert remove_duplicates([]) == []
    assert remove_duplicates([1]) == [1]
    assert remove_duplicates([2, 2, 2, 2]) == [2]
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]         
    assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]   
 
 
def test_find_pairs():
    assert sorted(find_pairs([1, 2, 3, 4], 5)) == [(1, 4), (2, 3)]
    assert find_pairs([], 5) == []                       
    assert find_pairs([5], 10) == []                     
    assert find_pairs([1, 2, 3], 100) == []              
    assert find_pairs([5, 1, 2], 10) == []               
    assert sorted(find_pairs([-1, 1, 2, -2], 0)) == [(-2, 2), (-1, 1)]  
    assert sorted(find_pairs([0, 5], 5)) == [(0, 5)]     
    data = random.sample(range(-500, 500), 200)          
    assert sorted(find_pairs(data, 10)) == sorted(find_pairs_brute_force(data, 10))
 
 
def test_add_n_items():
    buf = io.StringIO()
    with redirect_stdout(buf):
        assert add_n_items(6) == [0, 1, 2, 3, 4, 5]
    assert buf.getvalue().count("Resize!") == 2 
    for n, expected in [(0, 0), (2, 0), (3, 1), (5, 2), (9, 3)]:
        buf = io.StringIO()
        with redirect_stdout(buf):
            add_n_items(n)
        assert buf.getvalue().count("Resize!") == expected
 
 
def test_running_total():
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert running_total([]) == []
    assert running_total([5]) == [5]
    assert running_total([0, 0, 0]) == [0, 0, 0]
    assert running_total([-1, -2, -3]) == [-1, -3, -6]   
    assert running_total([3, -3, 3]) == [3, 0, 3]        
 
 
def test_optimization_comparison():
    print("\nProblem 3 timing (seconds): brute force vs. optimized")
    for n in (2000, 4000, 8000):
        data = random.sample(range(10 * n), n)
        target = 10 * n
 
        start = time.perf_counter()
        find_pairs_brute_force(data, target)
        brute = time.perf_counter() - start
 
        start = time.perf_counter()
        find_pairs(data, target)
        fast = time.perf_counter() - start
 
        print(f"  n={n:>5}  brute force: {brute:.4f}  optimized: {fast:.5f}")
 
 
if __name__ == "__main__":
    test_most_frequent()
    test_remove_duplicates()
    test_find_pairs()
    test_add_n_items()
    test_running_total()
    print("All tests passed!")
    add_n_items(6)  
    test_optimization_comparison()