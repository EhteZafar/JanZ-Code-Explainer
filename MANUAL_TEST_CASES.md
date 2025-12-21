# 🧪 Manual Test Cases - AI Code Explainer

Complete test cases for manually testing both **Basic Mode** and **RAG Mode** endpoints.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Basic Mode Tests](#basic-mode-tests)
- [RAG Mode Tests](#rag-mode-tests)
- [Comparison Tests](#comparison-tests)
- [Edge Cases](#edge-cases)
- [Performance Tests](#performance-tests)

---

## 🚀 Quick Start

### Prerequisites

Make sure the Docker container is running:

```powershell
docker-compose ps
# Should show: ai-code-explainer-backend   Up (healthy)
```

### Test Endpoints

- **Basic Mode**: `POST http://localhost:8000/api/explain`
- **RAG Mode**: `POST http://localhost:8000/api/explain-rag`
- **Health Check**: `GET http://localhost:8000/health`

---

## 🔵 Basic Mode Tests

### Test Case 1: Simple Python Function

**Description**: Test basic function explanation  
**Language**: Python  
**Complexity**: Simple

**PowerShell Command**:

```powershell
$body = @{
    code = @"
def greet(name):
    return f"Hello, {name}!"
"@
    language = "python"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ Status: 200 OK
- ✅ Explanation includes: function definition, f-string usage, return statement
- ✅ Mode: "basic"
- ✅ Response time: < 3 seconds

---

### Test Case 2: JavaScript Array Methods

**Description**: Test array manipulation explanation  
**Language**: JavaScript  
**Complexity**: Medium

**PowerShell Command**:

```powershell
$body = @{
    code = @"
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const evens = doubled.filter(n => n % 2 === 0);
console.log(evens);
"@
    language = "javascript"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ Explains `map()` and `filter()` methods
- ✅ Describes arrow functions
- ✅ Explains modulo operator for even number check
- ✅ No retrieved_examples (Basic mode doesn't use RAG)

---

### Test Case 3: Java Class Definition

**Description**: Test OOP concepts explanation  
**Language**: Java  
**Complexity**: Medium

**PowerShell Command**:

```powershell
$body = @{
    code = @"
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }
}
"@
    language = "java"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ Explains encapsulation (private fields)
- ✅ Describes constructor
- ✅ Explains getter method
- ✅ Mentions OOP principles

---

### Test Case 4: C++ Memory Management

**Description**: Test pointer explanation  
**Language**: C++  
**Complexity**: Advanced

**PowerShell Command**:

```powershell
$body = @{
    code = @"
int* createArray(int size) {
    int* arr = new int[size];
    for(int i = 0; i < size; i++) {
        arr[i] = i * 2;
    }
    return arr;
}
"@
    language = "cpp"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ Explains dynamic memory allocation (`new`)
- ✅ Warns about memory leak (no `delete[]`)
- ✅ Describes pointer return type
- ✅ Explains for loop logic

---

### Test Case 5: Python Async/Await

**Description**: Test asynchronous programming explanation  
**Language**: Python  
**Complexity**: Advanced

**PowerShell Command**:

```powershell
$body = @{
    code = @"
import asyncio

async def fetch_data(url):
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
"@
    language = "python"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ Explains `async`/`await` keywords
- ✅ Describes `asyncio.sleep()` simulation
- ✅ Explains event loop (`asyncio.run()`)
- ✅ Mentions non-blocking I/O

---

## 🟢 RAG Mode Tests

### Test Case 6: Quicksort Algorithm (RAG)

**Description**: Test algorithm explanation with RAG context  
**Language**: Python  
**Complexity**: Medium

**PowerShell Command**:

```powershell
$body = @{
    code = @"
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"@
    language = "python"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ Mode: "rag"
- ✅ retrieved_examples: Should find similar sorting algorithms
- ✅ Relevance scores > 0.65
- ✅ Explanation enhanced with context from similar examples
- ✅ Should mention divide-and-conquer strategy
- ✅ May reference similar algorithms from database

---

### Test Case 7: Binary Search (RAG)

**Description**: Test search algorithm with RAG retrieval  
**Language**: Java  
**Complexity**: Medium

**PowerShell Command**:

```powershell
$body = @{
    code = @"
public int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
"@
    language = "java"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ retrieved_examples: Binary search or similar search algorithms
- ✅ Explains O(log n) time complexity
- ✅ Mentions prerequisite: sorted array
- ✅ Contextual comparison with other search methods

---

### Test Case 8: Promise Chain (RAG)

**Description**: Test async JavaScript with RAG context  
**Language**: JavaScript  
**Complexity**: Medium

**PowerShell Command**:

```powershell
$body = @{
    code = @"
function fetchUserData(userId) {
    return fetch(`/api/users/${userId}`)
        .then(response => response.json())
        .then(data => {
            console.log('User:', data.name);
            return data;
        })
        .catch(error => console.error('Error:', error));
}
"@
    language = "javascript"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ retrieved_examples: Async/await or promise-related code
- ✅ Explains promise chaining
- ✅ Describes `.then()` and `.catch()` methods
- ✅ May compare with async/await syntax from database

---

### Test Case 9: Linked List Node (RAG)

**Description**: Test data structure with RAG context  
**Language**: C++  
**Complexity**: Medium

**PowerShell Command**:

```powershell
$body = @{
    code = @"
struct Node {
    int data;
    Node* next;

    Node(int val) : data(val), next(nullptr) {}
};

void printList(Node* head) {
    while (head != nullptr) {
        std::cout << head->data << " ";
        head = head->next;
    }
}
"@
    language = "cpp"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ retrieved_examples: Data structure examples
- ✅ Explains linked list concept
- ✅ Describes traversal pattern
- ✅ May reference similar data structures

---

### Test Case 10: Decorator Pattern (RAG)

**Description**: Test design pattern with RAG context  
**Language**: Python  
**Complexity**: Advanced

**PowerShell Command**:

```powershell
$body = @{
    code = @"
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b
"@
    language = "python"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

**Expected Result**:

- ✅ retrieved_examples: Decorator or higher-order function examples
- ✅ Explains decorator pattern
- ✅ Describes closure concept
- ✅ Explains `@` syntax sugar
- ✅ May reference similar patterns from database

---

## ⚖️ Comparison Tests

### Test Case 11: Same Code, Both Modes

**Description**: Compare Basic vs RAG mode responses for identical input  
**Code**: Simple sorting function

**Basic Mode**:

```powershell
$code = @{
    code = @"
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"@
    language = "python"
} | ConvertTo-Json

Write-Host "`n=== BASIC MODE ===" -ForegroundColor Cyan
$basic = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $code -ContentType "application/json"
Write-Host "Mode: $($basic.mode)"
Write-Host "Retrieved Examples: $($basic.retrieved_examples.Count)"
Write-Host "Explanation Length: $($basic.explanation.Length) chars"
Write-Host "`nExplanation Preview:"
Write-Host $basic.explanation.Substring(0, [Math]::Min(300, $basic.explanation.Length))
```

**RAG Mode**:

```powershell
Write-Host "`n=== RAG MODE ===" -ForegroundColor Green
$rag = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $code -ContentType "application/json"
Write-Host "Mode: $($rag.mode)"
Write-Host "Retrieved Examples: $($rag.retrieved_examples.Count)"
Write-Host "Explanation Length: $($rag.explanation.Length) chars"

if ($rag.retrieved_examples.Count -gt 0) {
    Write-Host "`nRetrieved Examples:"
    $rag.retrieved_examples | ForEach-Object {
        Write-Host "  - $($_.language) | $($_.category) | Score: $($_.relevance_score)"
    }
}

Write-Host "`nExplanation Preview:"
Write-Host $rag.explanation.Substring(0, [Math]::Min(300, $rag.explanation.Length))
```

**Expected Differences**:

- ✅ RAG mode should have retrieved_examples array
- ✅ RAG explanation may be more detailed
- ✅ RAG may reference similar algorithms
- ✅ Both should explain the bubble sort logic

---

## 🔴 Edge Cases

### Test Case 12: Empty Code

**Description**: Test error handling for empty input

**PowerShell Command**:

```powershell
$body = @{
    code = ""
    language = "python"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json"
} catch {
    Write-Host "Error (Expected):" -ForegroundColor Yellow
    $_.Exception.Response.StatusCode.value__
    $_ | ConvertTo-Json
}
```

**Expected Result**:

- ✅ Status: 422 Unprocessable Entity
- ✅ Error message about empty code

---

### Test Case 13: Very Long Code

**Description**: Test handling of large code snippets

**PowerShell Command**:

```powershell
$longCode = @"
def process_data(data):
    # Line 1
    result = []
    # Line 2
    for item in data:
        # Line 3
        processed = item * 2
        # Line 4
        result.append(processed)
    # ... (imagine 200+ more lines)
    return result
"@

$body = @{
    code = $longCode
    language = "python"
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json"
Write-Host "Status: OK"
Write-Host "Response received: $($response.explanation.Length) chars"
```

**Expected Result**:

- ✅ Status: 200 OK
- ✅ Handles up to 10,000 characters
- ✅ Explanation still relevant

---

### Test Case 14: Invalid Language

**Description**: Test unsupported language handling

**PowerShell Command**:

```powershell
$body = @{
    code = "SELECT * FROM users;"
    language = "brainfuck"  # Unsupported language
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json"
Write-Host "Response received - Language detection should handle this"
$response | ConvertTo-Json
```

**Expected Result**:

- ✅ Status: 200 OK (graceful handling)
- ✅ AI attempts to explain despite unusual language
- ✅ May suggest correct language

---

### Test Case 15: Code with Syntax Errors

**Description**: Test handling of invalid syntax

**PowerShell Command**:

```powershell
$body = @{
    code = @"
def broken_function(
    print "missing closing paren"
    return None
"@
    language = "python"
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json"
Write-Host "Explanation for broken code:"
Write-Host $response.explanation.Substring(0, [Math]::Min(500, $response.explanation.Length))
```

**Expected Result**:

- ✅ Status: 200 OK
- ✅ Explanation mentions syntax errors
- ✅ Suggests corrections
- ✅ Explains intent despite errors

---

## ⚡ Performance Tests

### Test Case 16: Response Time Comparison

**Description**: Measure and compare response times

**PowerShell Script**:

```powershell
$testCode = @{
    code = @"
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
"@
    language = "javascript"
} | ConvertTo-Json

# Test Basic Mode
Write-Host "`nTesting Basic Mode..." -ForegroundColor Cyan
$basicStart = Get-Date
$basicResponse = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $testCode -ContentType "application/json"
$basicTime = (Get-Date) - $basicStart
Write-Host "Basic Mode Time: $($basicTime.TotalMilliseconds) ms"

# Test RAG Mode
Write-Host "`nTesting RAG Mode..." -ForegroundColor Green
$ragStart = Get-Date
$ragResponse = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $testCode -ContentType "application/json"
$ragTime = (Get-Date) - $ragStart
Write-Host "RAG Mode Time: $($ragTime.TotalMilliseconds) ms"

# Compare
Write-Host "`n=== Performance Comparison ===" -ForegroundColor Yellow
Write-Host "Basic: $($basicTime.TotalMilliseconds) ms"
Write-Host "RAG:   $($ragTime.TotalMilliseconds) ms"
Write-Host "Diff:  +$([Math]::Round($ragTime.TotalMilliseconds - $basicTime.TotalMilliseconds, 2)) ms"
```

**Expected Result**:

- ✅ Basic mode: 1-3 seconds
- ✅ RAG mode: 1.5-3.5 seconds (slightly slower due to retrieval)
- ✅ RAG overhead: 100-500ms for vector search

---

### Test Case 17: Multiple Concurrent Requests

**Description**: Test system under load

**PowerShell Script**:

```powershell
$jobs = @()
$testCodes = @(
    @{code = "def test1(): pass"; language = "python"},
    @{code = "function test2() {}"; language = "javascript"},
    @{code = "public void test3() {}"; language = "java"},
    @{code = "void test4() {}"; language = "cpp"}
)

Write-Host "Sending 4 concurrent requests..." -ForegroundColor Cyan
foreach ($test in $testCodes) {
    $body = $test | ConvertTo-Json
    $jobs += Start-Job -ScriptBlock {
        param($body)
        Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json"
    } -ArgumentList $body
}

Write-Host "Waiting for responses..."
$jobs | Wait-Job | Receive-Job
$jobs | Remove-Job

Write-Host "`nAll concurrent requests completed!" -ForegroundColor Green
```

**Expected Result**:

- ✅ All requests succeed
- ✅ No timeouts or errors
- ✅ Responses within reasonable time

---

## 📊 Metrics Verification

### Test Case 18: Performance Metrics Endpoint

**Description**: Verify metrics are being tracked

**PowerShell Command**:

```powershell
# Make a few requests first
1..3 | ForEach-Object {
    $body = @{code = "print('test $_')"; language = "python"} | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json" | Out-Null
}

# Check metrics
Write-Host "`nPerformance Metrics:" -ForegroundColor Cyan
$metrics = Invoke-RestMethod -Uri http://localhost:8000/api/metrics/performance
$metrics | ConvertTo-Json -Depth 3

Write-Host "`nKey Metrics:"
Write-Host "Total Requests: $($metrics.total_requests)"
Write-Host "Success Rate: $($metrics.success_rate)%"
Write-Host "Avg Response Time: $($metrics.avg_response_time) ms"
```

**Expected Result**:

- ✅ total_requests > 0
- ✅ success_rate = 100.0
- ✅ avg_response_time < 5000 ms

---

## 🎯 Complete Test Suite

### Run All Tests Script

Save this as `run_all_manual_tests.ps1`:

```powershell
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  AI Code Explainer - Manual Test Suite" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta

# Health Check
Write-Host "`n[1/5] Health Check..." -ForegroundColor Cyan
$health = Invoke-RestMethod -Uri http://localhost:8000/health
if ($health.status -eq "healthy") {
    Write-Host "✓ Server is healthy" -ForegroundColor Green
} else {
    Write-Host "✗ Server health check failed" -ForegroundColor Red
    exit 1
}

# Basic Mode Test
Write-Host "`n[2/5] Basic Mode Test..." -ForegroundColor Cyan
$basicBody = @{code = "def hello(): return 'world'"; language = "python"} | ConvertTo-Json
$basic = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $basicBody -ContentType "application/json"
if ($basic.mode -eq "basic") {
    Write-Host "✓ Basic mode working" -ForegroundColor Green
} else {
    Write-Host "✗ Basic mode failed" -ForegroundColor Red
}

# RAG Mode Test
Write-Host "`n[3/5] RAG Mode Test..." -ForegroundColor Cyan
$ragBody = @{code = "def quicksort(arr): return sorted(arr)"; language = "python"} | ConvertTo-Json
$rag = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain-rag -Body $ragBody -ContentType "application/json"
if ($rag.mode -eq "rag" -and $rag.retrieved_examples.Count -gt 0) {
    Write-Host "✓ RAG mode working with $($rag.retrieved_examples.Count) examples retrieved" -ForegroundColor Green
} else {
    Write-Host "✗ RAG mode failed or no examples retrieved" -ForegroundColor Yellow
}

# Multi-language Test
Write-Host "`n[4/5] Multi-language Test..." -ForegroundColor Cyan
$languages = @("python", "javascript", "java", "cpp")
$passed = 0
foreach ($lang in $languages) {
    $langBody = @{code = "// test code"; language = $lang} | ConvertTo-Json
    try {
        Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $langBody -ContentType "application/json" | Out-Null
        $passed++
    } catch {
        Write-Host "  ✗ $lang failed" -ForegroundColor Red
    }
}
Write-Host "✓ $passed/$($languages.Count) languages tested successfully" -ForegroundColor Green

# Metrics Check
Write-Host "`n[5/5] Metrics Check..." -ForegroundColor Cyan
$metrics = Invoke-RestMethod -Uri http://localhost:8000/api/metrics/performance
Write-Host "✓ Total Requests: $($metrics.total_requests)" -ForegroundColor Green
Write-Host "✓ Success Rate: $($metrics.success_rate)%" -ForegroundColor Green

Write-Host "`n============================================" -ForegroundColor Magenta
Write-Host "  All Manual Tests Complete!" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
```

---

## 📝 Testing Checklist

Use this checklist to track your manual testing progress:

### Basic Mode

- [ ] Test Case 1: Simple Python function
- [ ] Test Case 2: JavaScript array methods
- [ ] Test Case 3: Java class definition
- [ ] Test Case 4: C++ memory management
- [ ] Test Case 5: Python async/await

### RAG Mode

- [ ] Test Case 6: Quicksort algorithm
- [ ] Test Case 7: Binary search
- [ ] Test Case 8: Promise chain
- [ ] Test Case 9: Linked list
- [ ] Test Case 10: Decorator pattern

### Comparisons

- [ ] Test Case 11: Same code in both modes

### Edge Cases

- [ ] Test Case 12: Empty code
- [ ] Test Case 13: Very long code
- [ ] Test Case 14: Invalid language
- [ ] Test Case 15: Syntax errors

### Performance

- [ ] Test Case 16: Response time comparison
- [ ] Test Case 17: Concurrent requests
- [ ] Test Case 18: Metrics verification

---

## 🎨 Tips for Manual Testing

1. **Use PowerShell ISE or VS Code** for easier copy-paste of multi-line commands
2. **Check response times** - Basic should be faster than RAG
3. **Verify retrieved_examples** in RAG mode have relevance_score > 0.65
4. **Compare explanations** between modes for same code
5. **Monitor Docker logs** while testing: `docker-compose logs -f backend`
6. **Check metrics** periodically: `http://localhost:8000/api/metrics/performance`

---

## 🐛 Troubleshooting

**If tests fail:**

1. **Check Docker container**:

   ```powershell
   docker-compose ps
   docker-compose logs backend
   ```

2. **Verify database is populated**:

   ```powershell
   docker-compose exec backend python view_database.py
   ```

3. **Test health endpoint**:

   ```powershell
   Invoke-RestMethod http://localhost:8000/health
   ```

4. **Restart container**:
   ```powershell
   docker-compose restart backend
   ```

---

## 📚 Related Documentation

- [README.md](README.md) - Project overview
- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Docker setup and troubleshooting
- [PHASE3_TESTING.md](PHASE3_TESTING.md) - Automated testing documentation

---

**Happy Testing! 🎉**
