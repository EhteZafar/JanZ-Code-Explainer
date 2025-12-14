"""
Sample Dataset: Curated code-explanation pairs for RAG system
Covers multiple languages, algorithms, and common patterns
"""

CODE_EXPLANATION_DATASET = [
    # Python - Algorithms
    {
        "id": "py_quicksort",
        "language": "python",
        "category": "algorithms",
        "subcategory": "sorting",
        "difficulty": "intermediate",
        "code": """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)""",
        "explanation": """## Overview
Implements quicksort algorithm using divide-and-conquer recursion with list comprehensions.

## Detailed Breakdown
1. **Base Case** (line 2-3): Arrays with ≤1 element are already sorted
2. **Pivot Selection** (line 4): Chooses middle element to reduce worst-case probability
3. **Partitioning** (lines 5-7): Divides array into three parts using list comprehensions
   - `left`: Elements less than pivot
   - `middle`: Elements equal to pivot (handles duplicates)
   - `right`: Elements greater than pivot
4. **Recursive Sorting** (line 8): Recursively sort left and right, concatenate with middle

## Complexity Analysis
- **Time Complexity**: O(n log n) average, O(n²) worst case
- **Space Complexity**: O(n) due to list creation

## Key Concepts
- Divide and conquer strategy
- In-place vs out-of-place sorting
- Pivot selection importance
- List comprehensions in Python

## Best Practices & Improvements
✅ Handles duplicates correctly with `middle` partition
✅ Clean, readable Python code
⚠️ Not in-place (uses O(n) extra space)
💡 Could use three-way partitioning for better duplicate handling
💡 Could add random pivot selection"""
    },
    
    # JavaScript - Async/Promises
    {
        "id": "js_retry_fetch",
        "language": "javascript",
        "category": "async",
        "subcategory": "error-handling",
        "difficulty": "intermediate",
        "code": """async function fetchWithRetry(url, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await fetch(url);
            if (response.ok) return response.json();
            throw new Error(`HTTP ${response.status}`);
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
    }
}""",
        "explanation": """## Overview
Implements fetch with exponential backoff retry logic for resilient HTTP requests.

## Detailed Breakdown
1. **Retry Loop** (line 2): Attempts up to `maxRetries` times
2. **Fetch Attempt** (line 3-5):
   - Makes HTTP request
   - Checks `response.ok` (status 200-299)
   - Throws error if request failed
3. **Error Handling** (line 7-9):
   - Catches both network errors and HTTP errors
   - Rethrows on final attempt
   - Otherwise, waits before retry
4. **Exponential Backoff** (line 9):
   - Wait time increases each attempt: 1s, 2s, 3s...
   - Uses `setTimeout` wrapped in Promise for async delay

## Complexity Analysis
- **Time Complexity**: O(n) where n is max retries
- **Space Complexity**: O(1)

## Key Concepts
- Async/await error handling
- Exponential backoff strategy
- Promise-based delays
- Resilient API calls

## Best Practices & Improvements
✅ Automatic retry for transient failures
✅ Exponential backoff reduces server load
✅ Configurable retry count
💡 Could add jitter to backoff (randomness)
💡 Could distinguish between retryable/non-retryable errors
💡 Could add timeout per request"""
    },
    
    # Python - Data Structures
    {
        "id": "py_trie",
        "language": "python",
        "category": "data-structures",
        "subcategory": "trees",
        "difficulty": "advanced",
        "code": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end""",
        "explanation": """## Overview
Implements Trie (prefix tree) data structure for efficient string storage and prefix matching.

## Detailed Breakdown
1. **TrieNode Class**: Represents each node in the trie
   - `children`: Dictionary mapping characters to child nodes
   - `is_end`: Boolean marking word endings
   
2. **Trie Class**: Main data structure
   - `root`: Empty root node (doesn't store a character)

3. **Insert Operation** (lines 10-16):
   - Traverse tree character by character
   - Create nodes for missing characters
   - Mark final node as word end

4. **Search Operation** (lines 18-24):
   - Follow path character by character
   - Return False if path doesn't exist
   - Return `is_end` to distinguish "car" from "carpet"

## Complexity Analysis
- **Insert Time**: O(m) where m is word length
- **Search Time**: O(m)
- **Space**: O(ALPHABET_SIZE * N * M) where N is number of words

## Key Concepts
- Trie data structure (prefix tree)
- Dictionary for dynamic children
- Path-based storage
- Prefix matching

## Best Practices & Improvements
✅ Clean class structure
✅ O(m) operations independent of number of words
✅ Efficient prefix matching
💡 Could add `startsWith()` method for prefix queries
💡 Could add `delete()` operation
💡 Could store word counts for autocomplete ranking"""
    },
    
    # Java - OOP
    {
        "id": "java_singleton",
        "language": "java",
        "category": "design-patterns",
        "subcategory": "creational",
        "difficulty": "intermediate",
        "code": """public class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    private Connection connection;
    
    private DatabaseConnection() {
        // Initialize connection
        this.connection = DriverManager.getConnection(DB_URL);
    }
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}""",
        "explanation": """## Overview
Implements thread-safe Singleton pattern using double-checked locking for database connection.

## Detailed Breakdown
1. **Private Static Instance** (line 2):
   - `volatile` ensures visibility across threads
   - Prevents memory reordering issues

2. **Private Constructor** (line 5-8):
   - Prevents direct instantiation
   - Initializes database connection

3. **getInstance() Method** (line 10-18):
   - **First Check** (line 11): Fast path for existing instance
   - **Synchronized Block** (line 12): Only one thread enters
   - **Second Check** (line 13): Prevents double initialization
   - Creates instance if still null

## Complexity Analysis
- **Time Complexity**: O(1) after initialization
- **Space Complexity**: O(1)

## Key Concepts
- Singleton design pattern
- Thread safety in Java
- Double-checked locking
- Volatile keyword
- Lazy initialization

## Best Practices & Improvements
✅ Thread-safe implementation
✅ Lazy initialization (only creates when needed)
✅ Volatile prevents memory visibility issues
⚠️ Consider using enum singleton for simpler thread safety
💡 Could use initialization-on-demand holder idiom
💡 Could add connection pooling"""
    },
    
    # Python - Dynamic Programming
    {
        "id": "py_coin_change",
        "language": "python",
        "category": "algorithms",
        "subcategory": "dynamic-programming",
        "difficulty": "intermediate",
        "code": """def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1""",
        "explanation": """## Overview
Solves coin change problem using dynamic programming: find minimum coins needed for amount.

## Detailed Breakdown
1. **DP Array Initialization** (line 2-3):
   - `dp[i]` = minimum coins needed for amount i
   - Initialize with infinity (impossible)
   - Base case: `dp[0] = 0` (0 coins for 0 amount)

2. **Nested Loops** (lines 5-7):
   - Outer: iterate through each coin denomination
   - Inner: iterate through amounts from `coin` to `amount`
   - Build solution bottom-up

3. **DP Transition** (line 7):
   - Choice: use current coin or don't
   - `dp[x - coin] + 1`: using this coin
   - Take minimum of current value and new option

4. **Result** (line 9):
   - Return `dp[amount]` if possible
   - Return -1 if amount cannot be made

## Complexity Analysis
- **Time Complexity**: O(amount * coins)
- **Space Complexity**: O(amount)

## Key Concepts
- Dynamic programming
- Bottom-up approach
- Optimal substructure
- Unbounded knapsack variant

## Best Practices & Improvements
✅ Efficient DP solution
✅ Handles impossible cases
✅ Optimal time/space tradeoff
💡 Could add path reconstruction (which coins used)
💡 Could optimize space with 2D array for counting solutions"""
    },
    
    # JavaScript - Closures
    {
        "id": "js_counter_closure",
        "language": "javascript",
        "category": "concepts",
        "subcategory": "closures",
        "difficulty": "beginner",
        "code": """function createCounter(initialValue = 0) {
    let count = initialValue;
    
    return {
        increment: () => ++count,
        decrement: () => --count,
        getValue: () => count,
        reset: () => count = initialValue
    };
}

const counter = createCounter(10);
console.log(counter.increment()); // 11
console.log(counter.getValue());  // 11""",
        "explanation": """## Overview
Demonstrates JavaScript closures by creating a counter with private state and public methods.

## Detailed Breakdown
1. **Factory Function** (line 1):
   - Creates new counter instance
   - Takes optional initial value

2. **Private Variable** (line 2):
   - `count` is private, not accessible outside
   - Encapsulated in function scope

3. **Returned Object** (lines 4-9):
   - Public interface with four methods
   - Each method is a closure over `count`
   - Can read and modify private variable

4. **Closure Behavior**:
   - Methods "remember" their creation environment
   - Each counter instance has its own `count`
   - `count` persists across method calls

5. **Usage** (lines 11-13):
   - Create counter with initial value 10
   - Methods access and modify private state

## Complexity Analysis
- **Time Complexity**: O(1) per operation
- **Space Complexity**: O(1) per counter instance

## Key Concepts
- Closures in JavaScript
- Private variables (encapsulation)
- Factory pattern
- Lexical scoping
- Higher-order functions

## Best Practices & Improvements
✅ Data encapsulation without classes
✅ Clean public API
✅ No external dependencies
💡 Could add getters/setters for validation
💡 Could emit events on state changes
💡 Modern alternative: use ES6 classes with # private fields"""
    },
    
    # Python - Recursion
    {
        "id": "py_permutations",
        "language": "python",
        "category": "algorithms",
        "subcategory": "backtracking",
        "difficulty": "intermediate",
        "code": """def permutations(nums):
    result = []
    
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    
    backtrack([], nums)
    return result""",
        "explanation": """## Overview
Generates all permutations of a list using backtracking recursion.

## Detailed Breakdown
1. **Main Function** (line 1-2):
   - `result`: stores all permutations
   - Sets up recursive backtracking

2. **Backtrack Helper** (line 4):
   - `current`: permutation being built
   - `remaining`: elements not yet used

3. **Base Case** (line 5-7):
   - When no remaining elements, permutation is complete
   - Append copy of `current` (not reference!)
   - Return to try other branches

4. **Recursive Case** (lines 9-12):
   - Try each remaining element in current position
   - **Choose**: Add element to current (line 10)
   - **Explore**: Recurse with updated state (line 11)
   - **Unchoose**: Backtrack by removing element (line 12)

5. **Call and Return** (lines 14-15):
   - Start with empty current, all nums remaining
   - Return collected results

## Complexity Analysis
- **Time Complexity**: O(n! * n) - n! permutations, O(n) to copy each
- **Space Complexity**: O(n! * n) for results + O(n) recursion depth

## Key Concepts
- Backtracking algorithm
- Recursion tree
- State space exploration
- Deep vs shallow copy importance

## Best Practices & Improvements
✅ Clean backtracking structure (choose, explore, unchoose)
✅ Handles duplicates correctly with list slicing
✅ Returns all solutions
⚠️ List slicing creates copies (O(n) each call)
💡 Could use swapping for O(1) state changes
💡 Could add pruning for constraints
💡 Could handle duplicate elements (permutations with duplicates)"""
    },
    
    # Java - Streams
    {
        "id": "java_stream_processing",
        "language": "java",
        "category": "functional",
        "subcategory": "streams",
        "difficulty": "intermediate",
        "code": """List<String> result = employees.stream()
    .filter(e -> e.getSalary() > 50000)
    .filter(e -> e.getDepartment().equals("Engineering"))
    .map(Employee::getName)
    .sorted()
    .collect(Collectors.toList());""",
        "explanation": """## Overview
Uses Java Streams API to filter, transform, and collect employee data in a functional pipeline.

## Detailed Breakdown
1. **Stream Creation** (line 1):
   - Converts collection to stream for functional operations
   - Enables lazy evaluation and potential parallelization

2. **First Filter** (line 2):
   - Keeps only employees with salary > 50000
   - Lambda predicate: `e -> boolean`

3. **Second Filter** (line 3):
   - Further filters for Engineering department
   - Filters chain: only items passing both remain

4. **Map Transformation** (line 4):
   - Transforms `Employee` objects to `String` names
   - Method reference `Employee::getName` equivalent to `e -> e.getName()`

5. **Sorting** (line 5):
   - Sorts names alphabetically
   - Uses natural String ordering

6. **Collection** (line 6):
   - Terminal operation: triggers pipeline execution
   - Collects results into List

## Complexity Analysis
- **Time Complexity**: O(n log n) due to sorting
- **Space Complexity**: O(n) for result list

## Key Concepts
- Java Streams API
- Functional programming in Java
- Lazy evaluation
- Method references
- Collector pattern

## Best Practices & Improvements
✅ Declarative code (what, not how)
✅ Chain of transformations
✅ Immutable operations
✅ Readable pipeline
💡 Could parallelize: `parallelStream()` for large datasets
💡 Could add null checks with `Objects::nonNull`
💡 Could use `Collectors.toUnmodifiableList()` for immutability"""
    },

    # Python - Generators
    {
        "id": "py_fibonacci_generator",
        "language": "python",
        "category": "concepts",
        "subcategory": "generators",
        "difficulty": "intermediate",
        "code": """def fibonacci_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Usage
for num in fibonacci_generator(10):
    print(num)""",
        "explanation": """## Overview
Implements memory-efficient Fibonacci sequence generator using Python's yield keyword.

## Detailed Breakdown
1. **Generator Function** (line 1):
   - Defined like regular function but uses `yield`
   - Returns generator object, not value directly

2. **Initialization** (line 2-3):
   - Two variables for Fibonacci sequence
   - Counter for limiting output

3. **Generator Loop** (line 4-7):
   - **Yield** (line 5): Returns current value, pauses execution
   - **Update** (line 6): Simultaneous assignment for next Fibonacci numbers
   - **Increment** (line 7): Count yielded values

4. **Iteration** (line 10-11):
   - For loop automatically calls `next()` on generator
   - Generator resumes from last yield
   - Stops when function exits

## Complexity Analysis
- **Time Complexity**: O(1) per iteration
- **Space Complexity**: O(1) - only stores 2 numbers at a time

## Key Concepts
- Generators in Python
- Lazy evaluation
- Memory efficiency
- Yield vs return
- Iterator protocol

## Best Practices & Improvements
✅ Memory-efficient (vs building list)
✅ Infinite sequences possible
✅ State maintained between yields
✅ Clean, readable code
💡 Could make infinite: remove `count` and `n` parameter
💡 Could add caching for repeated calls
💡 Could use `yield from` for composing generators"""
    },

    # C++ - Smart Pointers
    {
        "id": "cpp_unique_ptr",
        "language": "cpp",
        "category": "memory-management",
        "subcategory": "smart-pointers",
        "difficulty": "intermediate",
        "code": """#include <memory>

class Resource {
    int* data;
public:
    Resource(int size) : data(new int[size]) {}
    ~Resource() { delete[] data; }
};

std::unique_ptr<Resource> createResource() {
    return std::make_unique<Resource>(100);
}

int main() {
    auto resource = createResource();
    // Automatically deleted when out of scope
    return 0;
}""",
        "explanation": """## Overview
Demonstrates C++ unique_ptr for automatic memory management and RAII principle.

## Detailed Breakdown
1. **Resource Class** (lines 3-8):
   - Manages dynamic array
   - Constructor allocates memory
   - Destructor deallocates (RAII cleanup)

2. **Factory Function** (lines 10-12):
   - Creates and returns unique_ptr
   - `make_unique`: safe, exception-safe construction
   - Ownership transferred to caller

3. **Main Function** (lines 14-18):
   - `auto` deduces type as `std::unique_ptr<Resource>`
   - No manual delete needed
   - Destructor called automatically at scope exit

4. **Ownership Semantics**:
   - unique_ptr cannot be copied (exclusive ownership)
   - Can be moved (transfer ownership)
   - Prevents memory leaks and double-deletion

## Complexity Analysis
- **Time Complexity**: O(1) for pointer operations
- **Space Complexity**: O(1) for pointer, O(n) for Resource data

## Key Concepts
- RAII (Resource Acquisition Is Initialization)
- Smart pointers in C++11/14/17
- Exclusive ownership
- Move semantics
- Automatic memory management

## Best Practices & Improvements
✅ No manual memory management
✅ Exception-safe
✅ Clear ownership semantics
✅ Zero overhead vs raw pointer
💡 Use std::shared_ptr for shared ownership
💡 Use std::weak_ptr to break circular references
💡 Prefer make_unique over new for exception safety"""
    }
]


def get_dataset():
    """Return the complete dataset."""
    return CODE_EXPLANATION_DATASET


def get_dataset_stats():
    """Get statistics about the dataset."""
    total = len(CODE_EXPLANATION_DATASET)
    
    languages = {}
    categories = {}
    difficulties = {}
    
    for doc in CODE_EXPLANATION_DATASET:
        lang = doc.get('language', 'unknown')
        cat = doc.get('category', 'unknown')
        diff = doc.get('difficulty', 'unknown')
        
        languages[lang] = languages.get(lang, 0) + 1
        categories[cat] = categories.get(cat, 0) + 1
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    return {
        "total_examples": total,
        "languages": languages,
        "categories": categories,
        "difficulties": difficulties
    }


if __name__ == "__main__":
    # Display dataset statistics
    stats = get_dataset_stats()
    print("=" * 60)
    print("CODE EXPLANATION DATASET STATISTICS")
    print("=" * 60)
    print(f"\nTotal Examples: {stats['total_examples']}")
    
    print("\nLanguages:")
    for lang, count in sorted(stats['languages'].items()):
        print(f"  - {lang}: {count}")
    
    print("\nCategories:")
    for cat, count in sorted(stats['categories'].items()):
        print(f"  - {cat}: {count}")
    
    print("\nDifficulties:")
    for diff, count in sorted(stats['difficulties'].items()):
        print(f"  - {diff}: {count}")
    print()
