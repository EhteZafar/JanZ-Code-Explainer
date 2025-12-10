# FRONTEND DOCUMENTATION

## **SECTION 5 — Frontend HTML/JS**

### Complete Frontend Implementation

The frontend is a single-page application (SPA) built with pure HTML, CSS, and JavaScript. No frameworks required—just open the file in a browser!

---

## Frontend Architecture

### File Structure

```
frontend/
└── index.html          # Complete web application (HTML + CSS + JS)
```

**Single File Design Benefits:**

- No build process required
- No dependencies to install
- Works offline (after initial load)
- Easy to deploy (just upload one file)
- Simple to understand and modify

---

## Implementation Overview

The `index.html` file contains three main sections:

1. **HTML Structure** - Page layout and elements
2. **CSS Styling** - Visual design and animations
3. **JavaScript Logic** - Interactivity and API communication

---

## HTML Structure

### Main Components

```html
<body>
  <div class="container">
    <!-- Header -->
    <header>
      <h1>🤖 AI Code Explainer</h1>
      <p class="subtitle">Understand any code in seconds</p>
      <span class="model-badge">Powered by LLaMA 3.3 70B Versatile</span>
    </header>

    <!-- Input Section -->
    <div class="input-section">
      <label for="codeInput">📝 Paste your code here:</label>
      <textarea id="codeInput" placeholder="..."></textarea>
    </div>

    <!-- Action Buttons -->
    <div class="button-container">
      <button class="explain-btn" onclick="explainCode()">
        ✨ Explain Code
      </button>
      <button class="clear-btn" onclick="clearAll()">🗑️ Clear</button>
    </div>

    <!-- Loading Animation -->
    <div class="loading" id="loading">
      <div class="spinner"></div>
      <p class="loading-text">Analyzing code with LLaMA 3.3 70B...</p>
    </div>

    <!-- Error Display -->
    <div class="error" id="error">
      <div class="error-title">❌ Error</div>
      <p id="errorMessage"></p>
    </div>

    <!-- Explanation Output -->
    <div class="output-section" id="outputSection">
      <div class="output-header">
        <span class="output-title">💡 Explanation:</span>
        <button class="copy-btn" onclick="copyExplanation()">📋 Copy</button>
      </div>
      <div class="explanation-box" id="explanation"></div>
    </div>

    <!-- Example Buttons -->
    <div class="examples">
      <p class="examples-title">🎯 Try an example:</p>
      <div class="example-buttons">
        <button class="example-btn" onclick="loadExample('python')">
          Python
        </button>
        <button class="example-btn" onclick="loadExample('javascript')">
          JavaScript
        </button>
        <button class="example-btn" onclick="loadExample('java')">Java</button>
        <button class="example-btn" onclick="loadExample('cpp')">C++</button>
      </div>
    </div>

    <!-- Footer -->
    <footer>
      <p>Built with FastAPI + LLaMA 3.3 70B via Groq | Phase 1 CS Project</p>
    </footer>
  </div>
</body>
```

**Key Elements:**

- **Container**: Centers and styles the main content
- **Textarea**: Large input area for code with monospace font
- **Buttons**: Styled action buttons with hover effects
- **Loading Indicator**: Animated spinner shown during API calls
- **Error Display**: Hidden by default, shown on errors
- **Output Section**: Displays formatted explanations
- **Examples**: Quick-load buttons for testing

---

## CSS Styling

### Design Philosophy

**Modern, Professional Look:**

- Gradient backgrounds (purple theme)
- Card-based layout with shadows
- Smooth animations and transitions
- Responsive design for all screen sizes
- Clean typography with good readability

### Key CSS Features

**1. Gradient Background**

```css
body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**2. Container Card**

```css
.container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 1200px;
  padding: 40px;
}
```

**3. Animations**

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
```

**4. Responsive Design**

```css
@media (max-width: 768px) {
  .container {
    padding: 20px;
  }
  h1 {
    font-size: 1.8em;
  }
  .button-container {
    flex-direction: column;
  }
}
```

**5. Interactive Elements**

```css
button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

---

## JavaScript Functionality

### Core Functions

#### 1. **explainCode()** - Main Function

```javascript
async function explainCode() {
  const code = document.getElementById("codeInput").value.trim();

  // Validate input
  if (!code) {
    showError("Please paste some code to explain.");
    return;
  }

  // Reset UI state
  hideError();
  hideOutput();
  showLoading();

  try {
    // Call backend API
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: code }),
    });

    const data = await response.json();

    if (response.ok) {
      showOutput(data.explanation);
    } else {
      showError(data.detail || "Failed to generate explanation.");
    }
  } catch (error) {
    showError(
      "Could not connect to the server. Make sure the backend is running."
    );
  } finally {
    hideLoading();
  }
}
```

**What It Does:**

1. Gets code from textarea
2. Validates input (not empty)
3. Shows loading animation
4. Calls backend API with fetch
5. Handles response (success or error)
6. Displays result or error message
7. Hides loading animation

**Key Features:**

- Async/await for clean asynchronous code
- Comprehensive error handling
- User-friendly error messages
- Proper UI state management

#### 2. **showOutput()** - Display Explanation

```javascript
function showOutput(explanation) {
  const explanationDiv = document.getElementById("explanation");

  // Convert markdown-style formatting to HTML
  let formatted = explanation
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, "<code>$1</code>");

  explanationDiv.innerHTML = formatted;
  document.getElementById("outputSection").classList.add("visible");

  // Scroll to output
  document.getElementById("outputSection").scrollIntoView({
    behavior: "smooth",
    block: "nearest",
  });
}
```

**What It Does:**

1. Takes explanation text
2. Converts basic markdown to HTML:
   - `**text**` → `<strong>text</strong>`
   - `*text*` → `<em>text</em>`
   - `` `text` `` → `<code>text</code>`
3. Displays in explanation box
4. Shows the output section
5. Smoothly scrolls to result

#### 3. **loadExample()** - Load Sample Code

```javascript
const examples = {
  python: `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1`,

  javascript: `async function fetchUserData(userId) {
    try {
        const response = await fetch(\`/api/users/\${userId}\`);
        if (!response.ok) throw new Error('User not found');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}`,
  // ... more examples
};

function loadExample(language) {
  document.getElementById("codeInput").value = examples[language];
  hideError();
  hideOutput();
}
```

**What It Does:**

1. Stores example code for multiple languages
2. Loads selected example into textarea
3. Resets UI state (hides previous results)

**Example Languages:**

- Python (binary search)
- JavaScript (async fetch)
- Java (bubble sort)
- C++ (fibonacci with DP)

#### 4. **copyExplanation()** - Copy to Clipboard

```javascript
function copyExplanation() {
  const explanation = document.getElementById("explanation").innerText;
  navigator.clipboard.writeText(explanation).then(() => {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = "✓ Copied!";
    setTimeout(() => {
      btn.textContent = originalText;
    }, 2000);
  });
}
```

**What It Does:**

1. Gets explanation text (plain text, not HTML)
2. Copies to clipboard using Clipboard API
3. Shows "Copied!" confirmation
4. Reverts to original button text after 2 seconds

#### 5. **UI State Management Functions**

```javascript
function showLoading() {
  document.getElementById("loading").classList.add("visible");
  document.getElementById("explainBtn").disabled = true;
}

function hideLoading() {
  document.getElementById("loading").classList.remove("visible");
  document.getElementById("explainBtn").disabled = false;
}

function showError(message) {
  document.getElementById("errorMessage").textContent = message;
  document.getElementById("error").classList.add("visible");
}

function hideError() {
  document.getElementById("error").classList.remove("visible");
}

function showOutput(explanation) {
  /* ... */
}

function hideOutput() {
  document.getElementById("outputSection").classList.remove("visible");
}

function clearAll() {
  document.getElementById("codeInput").value = "";
  hideError();
  hideOutput();
}
```

**Purpose:**

- Centralized UI state management
- Consistent show/hide behavior
- Easy to maintain and modify
- Prevents duplicate code

### API Configuration

```javascript
const API_URL = "http://localhost:8000/api/explain";
```

**Important:**

- Must match backend URL
- Change if backend runs on different port
- For production, use actual domain

### Event Listeners

```javascript
// Keyboard shortcut: Ctrl+Enter or Cmd+Enter to submit
document.getElementById("codeInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
    explainCode();
  }
});
```

**Features:**

- Keyboard shortcut for power users
- Doesn't interfere with normal Enter (newline in textarea)
- Works on both Windows (Ctrl) and Mac (Cmd)

---

## User Flow

### Normal Usage Flow

1. **User arrives at page**

   - Sees clean interface with input area
   - Reads title and model badge

2. **User pastes code**

   - Types or pastes code into textarea
   - Or clicks an example button

3. **User clicks "Explain Code"**

   - Loading animation appears
   - Button becomes disabled (prevents double-click)
   - "Analyzing code..." message shows

4. **Backend processes request**

   - API call to LLaMA 3.3 70B
   - Takes 1-3 seconds typically

5. **Explanation appears**

   - Loading animation disappears
   - Explanation box fades in smoothly
   - Page scrolls to show result

6. **User reads explanation**
   - Can copy with one click
   - Can clear and try another example

### Error Flow

1. **User clicks "Explain Code" with empty input**

   - Error message: "Please paste some code to explain."
   - No API call made (client-side validation)

2. **Backend is not running**

   - Error message: "Could not connect to the server..."
   - Suggests checking backend status

3. **API returns error**
   - Displays error from backend
   - Examples: "Invalid API key", "Code too long", etc.

---

## Frontend Features

### ✨ User Experience Features

1. **Instant Feedback**

   - Loading animation during processing
   - Visual feedback on button hover
   - Focus states on input elements

2. **Error Handling**

   - Clear, actionable error messages
   - Different messages for different error types
   - Graceful degradation

3. **Smooth Animations**

   - Fade-in effects for new content
   - Smooth scrolling to results
   - Button hover effects
   - Spinner animation

4. **Accessibility**

   - Semantic HTML elements
   - Keyboard navigation support
   - High contrast text
   - Clear labels

5. **Responsive Design**

   - Works on desktop, tablet, mobile
   - Adjusts layout for small screens
   - Touch-friendly button sizes

6. **Code Examples**
   - Pre-loaded examples for testing
   - Multiple languages represented
   - Real-world code snippets

### 🎨 Visual Features

- **Modern Gradient Background**: Purple theme
- **Card-Based Layout**: Clean, focused design
- **Syntax Highlighting**: Monospace font for code
- **Formatted Output**: Bold, italic, code tags
- **Loading Spinner**: Animated CSS spinner
- **Smooth Transitions**: 0.3s easing on interactions

---

## Customization Guide

### Change Color Scheme

```css
/* Current purple theme */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Blue theme */
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

/* Green theme */
background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);

/* Orange theme */
background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
```

### Adjust Layout

```css
/* Wider container */
.container {
  max-width: 1400px; /* Default: 1200px */
}

/* Smaller textarea */
textarea {
  min-height: 200px; /* Default: 250px */
}
```

### Modify API URL

```javascript
// For production
const API_URL = "https://yourapi.com/api/explain";

// For different port
const API_URL = "http://localhost:8001/api/explain";
```

---

## Testing the Frontend

### Manual Testing Checklist

✅ **Basic Functionality**

- [ ] Page loads without errors
- [ ] Can type in textarea
- [ ] "Explain Code" button is clickable
- [ ] "Clear" button clears textarea

✅ **API Integration**

- [ ] Clicking "Explain Code" shows loading animation
- [ ] Explanation appears after successful request
- [ ] Error shows if backend is offline

✅ **Examples**

- [ ] All example buttons work
- [ ] Examples load correct code

✅ **Copy Function**

- [ ] Copy button copies explanation
- [ ] Button shows "Copied!" confirmation

✅ **Error Handling**

- [ ] Empty input shows error
- [ ] Offline backend shows error
- [ ] API errors display properly

✅ **Responsive Design**

- [ ] Works on desktop (1920x1080)
- [ ] Works on tablet (768x1024)
- [ ] Works on mobile (375x667)

✅ **Keyboard Shortcuts**

- [ ] Ctrl+Enter / Cmd+Enter submits form

### Browser Compatibility

**Tested Browsers:**

- ✅ Chrome 90+ (recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Required Features:**

- `fetch` API (all modern browsers)
- `async/await` (all modern browsers)
- `classList` API (all modern browsers)
- `Clipboard API` (for copy function)
- CSS Grid/Flexbox (for layout)

---

## Usage Instructions

### For End Users

**Step 1: Open the Application**

```powershell
# Navigate to frontend directory
cd "c:\Users\ehtes\work\Nazish Project\JanZ Code Explainer\frontend"

# Open in browser (Windows)
start index.html

# Or double-click index.html in File Explorer
```

**Step 2: Make Sure Backend is Running**

- Backend must be running on `http://localhost:8000`
- See BACKEND_SETUP.md for instructions

**Step 3: Use the Application**

1. Paste code in the text area (or click an example)
2. Click "✨ Explain Code"
3. Wait 1-3 seconds for explanation
4. Read the detailed explanation
5. Click "📋 Copy" to copy explanation
6. Click "🗑️ Clear" to try another example

**Step 4: Troubleshooting**

- If error appears, read the message carefully
- Common issue: Backend not running
- Solution: Start backend server (see README.md)

### For Developers

**Modifying the Frontend:**

1. **Open `index.html` in VS Code**
2. **Make changes to:**
   - HTML structure (between `<body>` tags)
   - CSS styles (in `<style>` section)
   - JavaScript logic (in `<script>` section)
3. **Save file**
4. **Refresh browser** (Ctrl+R or F5)

**Common Modifications:**

- **Add new example**: Add to `examples` object in JavaScript
- **Change colors**: Modify CSS gradient values
- **Add features**: Add JavaScript functions
- **Improve styling**: Update CSS rules

---

## Browser Console Debugging

### Enable Developer Tools

- **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I`
- **Firefox**: Press `F12` or `Ctrl+Shift+K`
- **Safari**: Enable Developer menu, then press `Cmd+Option+I`

### Useful Console Commands

```javascript
// Test API call manually
fetch("http://localhost:8000/api/explain", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ code: 'print("test")' }),
})
  .then((r) => r.json())
  .then(console.log);

// Check current code value
document.getElementById("codeInput").value;

// Manually show/hide elements
document.getElementById("loading").classList.add("visible");
document.getElementById("loading").classList.remove("visible");
```

---

## Performance Optimization

### Current Performance

- **Initial Load**: < 1 second (single HTML file)
- **Rendering**: Instant (no heavy JavaScript)
- **API Call**: 1-3 seconds (depends on Groq)
- **Total Time**: ~2-4 seconds per explanation

### Future Optimizations

- Minify HTML/CSS/JS for production
- Add code syntax highlighting library
- Implement request caching
- Add request cancellation
- Progressive web app (PWA) support

---

## Accessibility Considerations

### Current Accessibility Features

✅ **Semantic HTML**

- Proper heading hierarchy (`<h1>`, `<h2>`)
- Meaningful labels for inputs
- Button elements (not styled divs)

✅ **Keyboard Navigation**

- Tab through all interactive elements
- Enter to click buttons
- Ctrl+Enter to submit

✅ **Visual Clarity**

- High contrast text
- Large, readable fonts
- Clear focus indicators

### Future Improvements

- Add ARIA labels
- Screen reader testing
- Keyboard-only mode
- High contrast mode toggle

---

## Conclusion

The frontend is a complete, production-ready web interface that:

- ✅ **Works out of the box** (just open in browser)
- ✅ **Communicates with backend** (RESTful API)
- ✅ **Handles errors gracefully** (user-friendly messages)
- ✅ **Provides great UX** (smooth animations, clear feedback)
- ✅ **Looks professional** (modern design, responsive)
- ✅ **Easy to customize** (single file, clear structure)

**The frontend is complete and ready to use!** 🎉

Open `index.html` in your browser and start explaining code!
