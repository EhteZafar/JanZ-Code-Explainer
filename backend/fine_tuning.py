"""
Domain-Specific Fine-Tuning Module
Implements logical fine-tuning through prompt engineering and few-shot learning
"""

import re
from typing import List, Dict, Optional


# System prompt for domain-specific code explanation
SYSTEM_PROMPT = """You are an expert programming instructor and code analyst with deep knowledge of:
- Data structures and algorithms
- Software design patterns
- Language-specific idioms and best practices
- Performance optimization
- Common pitfalls and edge cases

Your explanations are:
- Structured and methodical
- Pedagogically sound (teach, don't just describe)
- Technically accurate
- Appropriate for the audience level
- Focused on WHY, not just WHAT

When explaining code:
1. Start with high-level purpose
2. Break down into logical components
3. Analyze complexity and efficiency
4. Highlight best practices
5. Note potential issues or improvements"""


# Output format instructions
OUTPUT_FORMAT = """
Format your explanation as follows:

## Overview
[1-2 sentence summary of what the code does]

## Detailed Breakdown
[Step-by-step analysis of each significant part]

## Complexity Analysis
- Time Complexity: O(?)
- Space Complexity: O(?)

## Key Concepts
[Important programming concepts demonstrated]

## Best Practices & Improvements
[What's done well, what could be better]
"""


# Few-shot learning examples - curated high-quality code-explanation pairs
FEW_SHOT_EXAMPLES = [
    {
        "language": "python",
        "category": "algorithms",
        "code": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "explanation": """## Overview
Implements binary search algorithm to find a target value's index in a sorted array, returning -1 if not found.

## Detailed Breakdown
1. **Initialization** (line 2): Set search boundaries
   - `left = 0`: Start of array
   - `right = len(arr) - 1`: End of array

2. **Search Loop** (line 3): Continue while search space exists
   - Condition `left <= right` ensures we don't miss single elements

3. **Middle Point** (line 4): Calculate midpoint
   - Uses `//` (floor division) to get integer index
   - Avoids overflow compared to `(left + right) / 2`

4. **Comparison Logic** (lines 5-10):
   - **Match found**: Return index immediately
   - **Target larger**: Search right half (left = mid + 1)
   - **Target smaller**: Search left half (right = mid - 1)

5. **Not Found** (line 11): Return -1 after exhausting search space

## Complexity Analysis
- **Time Complexity**: O(log n) - halves search space each iteration
- **Space Complexity**: O(1) - only uses a few variables

## Key Concepts
- **Binary Search**: Divide and conquer on sorted data
- **Loop Invariants**: Search space always contains target if present
- **Integer Division**: Prevents index overflow

## Best Practices & Improvements
✅ Correct boundary handling (inclusive bounds)
✅ Efficient comparison logic
⚠️ Assumes array is sorted (precondition)
💡 Could add validation: if not is_sorted(arr): raise ValueError"""
    },
    {
        "language": "javascript",
        "category": "async",
        "code": """async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error('User not found');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}""",
        "explanation": """## Overview
Asynchronous function that fetches user data from an API endpoint with error handling.

## Detailed Breakdown
1. **Async Function Declaration**: Enables use of `await` keyword
   - Returns a Promise that resolves to user data or null

2. **Try-Catch Block**: Wraps potentially failing code
   - Catches network errors, parsing errors, and custom errors

3. **Fetch Request** (line 3):
   - Makes HTTP GET request to `/api/users/${userId}`
   - Template literal constructs dynamic URL
   - `await` pauses execution until response received

4. **Response Validation** (line 4-6):
   - Checks `response.ok` (status 200-299)
   - Throws custom error if request failed
   - Prevents silent failures

5. **JSON Parsing** (line 7):
   - Converts response body to JavaScript object
   - Also requires `await` as it's asynchronous

6. **Error Handling** (line 9-11):
   - Logs error for debugging
   - Returns null instead of throwing (graceful degradation)

## Complexity Analysis
- **Time Complexity**: O(n) where n is response size (JSON parsing)
- **Space Complexity**: O(n) to store response data

## Key Concepts
- **Async/Await**: Modern JavaScript asynchronous patterns
- **Promise Handling**: Cleaner than callbacks
- **Error Boundaries**: Try-catch for async operations
- **Graceful Degradation**: Return null on failure

## Best Practices & Improvements
✅ Uses modern async/await syntax
✅ Validates response before parsing
✅ Includes error handling
⚠️ Returns null on error (consider throwing for caller to handle)
💡 Could add retry logic for network failures
💡 Could add request timeout"""
    },
    {
        "language": "python",
        "category": "data-structures",
        "code": """class LRUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.capacity = capacity
        self.order = []
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)""",
        "explanation": """## Overview
Implements an LRU (Least Recently Used) cache with fixed capacity that evicts least recently accessed items when full.

## Detailed Breakdown
1. **Initialization**:
   - `cache`: Dictionary for O(1) key-value lookups
   - `capacity`: Maximum number of items to store
   - `order`: List tracking access order (most recent at end)

2. **Get Operation** (lines 7-12):
   - Return -1 if key doesn't exist
   - If found, move key to end of order (mark as recently used)
   - Return cached value

3. **Put Operation** (lines 14-21):
   - **Case 1**: Key exists → remove from old position, will re-add at end
   - **Case 2**: Cache full → evict least recently used (order[0])
   - **Case 3**: Normal insert → add to cache and order
   - Always append to end of order (most recent)

## Complexity Analysis
- **Time Complexity**: 
  - Get: O(n) due to list.remove()
  - Put: O(n) due to list.remove()
- **Space Complexity**: O(capacity) for storage

## Key Concepts
- **LRU Cache**: Caching strategy evicting least recently used items
- **Dictionary + List**: Combines fast lookup with order tracking
- **Cache Eviction**: Automatically manages memory

## Best Practices & Improvements
✅ Clear class structure
✅ Handles edge cases (key exists, capacity reached)
⚠️ list.remove() is O(n), not optimal for large caches
💡 Use OrderedDict or doubly-linked list + hashmap for O(1) operations
💡 Could add thread safety with locks"""
    }
]


# Language detection patterns
LANGUAGE_PATTERNS = {
    "python": [r"def\s+\w+\(", r"import\s+\w+", r":\s*$", r"elif\s+", r"print\("],
    "javascript": [r"function\s+\w+\(", r"const\s+\w+\s*=", r"=>\s*{", r"async\s+", r"await\s+"],
    "typescript": [r":\s*\w+(\[\]|\<)", r"interface\s+\w+", r"type\s+\w+\s*="],
    "java": [r"public\s+(class|static)", r"void\s+\w+\(", r"System\.out", r"@Override"],
    "cpp": [r"#include\s*<", r"std::", r"int\s+main\(", r"cout\s*<<"],
    "c": [r"#include\s*<", r"int\s+main\(", r"printf\(", r"scanf\("],
    "go": [r"func\s+\w+\(", r"package\s+", r":=\s+", r"fmt\."],
    "rust": [r"fn\s+\w+\(", r"let\s+\w+", r"impl\s+", r"pub\s+"],
}


def detect_language(code: str) -> str:
    """
    Detect programming language from code syntax.
    
    Args:
        code: Source code string
        
    Returns:
        Detected language name or 'unknown'
    """
    code_lower = code.lower()
    scores = {}
    
    for language, patterns in LANGUAGE_PATTERNS.items():
        score = sum(1 for pattern in patterns if re.search(pattern, code, re.MULTILINE | re.IGNORECASE))
        if score > 0:
            scores[language] = score
    
    if not scores:
        return "unknown"
    
    # Return language with highest score
    return max(scores.items(), key=lambda x: x[1])[0]


def select_relevant_examples(code: str, num_examples: int = 2) -> List[Dict]:
    """
    Select few-shot examples most relevant to the input code.
    
    Args:
        code: User's code to explain
        num_examples: Number of examples to return
        
    Returns:
        List of relevant example dictionaries
    """
    # Detect language of input code
    language = detect_language(code)
    
    # Prioritize same-language examples
    same_language = [ex for ex in FEW_SHOT_EXAMPLES if ex['language'] == language]
    other_language = [ex for ex in FEW_SHOT_EXAMPLES if ex['language'] != language]
    
    # Combine: prefer same language, fallback to others
    selected = same_language[:num_examples]
    
    if len(selected) < num_examples:
        selected.extend(other_language[:num_examples - len(selected)])
    
    return selected[:num_examples]


def build_few_shot_prompt(code: str, num_examples: int = 2) -> str:
    """
    Build prompt with few-shot examples.
    
    Args:
        code: User's code to explain
        num_examples: Number of examples to include
        
    Returns:
        Complete prompt string with examples
    """
    examples = select_relevant_examples(code, num_examples)
    language = detect_language(code)
    
    # Build few-shot section
    few_shot_text = "\n\n".join([
        f"Example {i+1}:\n\nCode:\n```{ex['language']}\n{ex['code']}\n```\n\nExplanation:\n{ex['explanation']}"
        for i, ex in enumerate(examples)
    ])
    
    # Construct complete prompt
    prompt = f"""{SYSTEM_PROMPT}

{OUTPUT_FORMAT}

Here are examples of high-quality code explanations:

{few_shot_text}

Now, explain the following code in a similar comprehensive style:

```{language if language != 'unknown' else ''}
{code}
```

Provide a detailed explanation following the format shown in the examples above."""
    
    return prompt


def validate_explanation_quality(explanation: str) -> Dict:
    """
    Validate that explanation meets quality standards.
    
    Args:
        explanation: Generated explanation text
        
    Returns:
        Dictionary with validation results
    """
    required_sections = [
        "## Overview",
        "## Detailed Breakdown",
        "## Complexity Analysis",
        "## Key Concepts"
    ]
    
    quality_metrics = {
        "has_overview": "## Overview" in explanation,
        "has_breakdown": "## Detailed Breakdown" in explanation,
        "has_complexity": "## Complexity Analysis" in explanation,
        "has_concepts": "## Key Concepts" in explanation,
        "has_improvements": "## Best Practices" in explanation or "## Improvements" in explanation,
        "length_adequate": len(explanation) > 300,
        "has_code_references": "`" in explanation,
        "well_structured": explanation.count("##") >= 4
    }
    
    score = sum(quality_metrics.values()) / len(quality_metrics)
    
    return {
        "valid": score >= 0.75,  # At least 75% of metrics met
        "score": score,
        "metrics": quality_metrics,
        "missing_sections": [section for section in required_sections if section not in explanation]
    }


def get_language_specific_context(language: str) -> str:
    """
    Get additional context specific to programming language.
    
    Args:
        language: Programming language name
        
    Returns:
        Language-specific context string
    """
    contexts = {
        "python": "Focus on Pythonic idioms, duck typing, and common standard library usage.",
        "javascript": "Highlight async patterns, closures, and modern ES6+ features.",
        "java": "Emphasize OOP principles, type safety, and common design patterns.",
        "cpp": "Note memory management, RAII, and performance considerations.",
        "c": "Focus on pointer usage, memory management, and undefined behavior risks.",
        "go": "Highlight goroutines, channels, and Go's simplicity philosophy.",
        "rust": "Emphasize ownership, borrowing, and memory safety guarantees."
    }
    
    return contexts.get(language, "Provide clear, accurate explanation of code functionality.")


# Export main functions
__all__ = [
    'build_few_shot_prompt',
    'detect_language',
    'validate_explanation_quality',
    'select_relevant_examples',
    'get_language_specific_context',
    'SYSTEM_PROMPT',
    'OUTPUT_FORMAT'
]
