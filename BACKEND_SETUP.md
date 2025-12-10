# BACKEND SETUP AND USAGE INSTRUCTIONS

## **SECTION 3 — Backend (FastAPI) + Instructions**

### Complete Backend Implementation

The backend is built with **FastAPI**, a modern Python web framework that provides:

- Fast performance (comparable to Node.js)
- Automatic API documentation
- Type validation with Pydantic
- Async support for concurrent requests
- Easy CORS configuration

---

## Backend Architecture

### Project Structure

```
backend/
├── main.py                 # FastAPI application with endpoints
├── groq_integration.py     # LLaMA 3.3 70B API integration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── .env                   # Your configuration (create this)
```

---

## File Descriptions

### **1. main.py** - FastAPI Server

This file contains:

- FastAPI application initialization
- CORS middleware configuration
- API endpoints (`/`, `/health`, `/api/explain`)
- Request/response models using Pydantic
- Error handling and logging
- Startup/shutdown events

**Key Features:**

- **CORS Enabled**: Frontend can call from any origin (configure for production)
- **Auto Documentation**: Swagger UI at `/docs`, ReDoc at `/redoc`
- **Type Safety**: Pydantic models ensure valid request/response data
- **Async Support**: Handles multiple requests concurrently
- **Logging**: Detailed logs for debugging and monitoring

### **2. groq_integration.py** - Groq API Integration

This file contains:

- Groq client initialization with API key from environment
- Prompt engineering for code explanation
- LLaMA 3.3 70B API call implementation
- Error handling (API errors, timeouts, rate limits)
- Input validation (code length, empty input)
- Connection testing functionality

**Key Features:**

- **Optimized Prompts**: Structured prompts for high-quality explanations
- **Error Recovery**: Graceful handling of API failures
- **Timeout Protection**: Prevents hanging requests
- **Model Configuration**: Temperature, max tokens, and other parameters
- **Validation**: Input sanitization and length limits

### **3. requirements.txt** - Dependencies

Lists all required Python packages with specific versions:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable management
- `groq` - Official Groq API client
- `pydantic` - Data validation

### **4. .env.example** - Configuration Template

Template for environment variables. Copy to `.env` and add your API key.

---

## Detailed Setup Instructions

### Step 1: Install Python

Ensure Python 3.8+ is installed:

```powershell
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/).

### Step 2: Navigate to Backend Directory

```powershell
cd "c:\Users\ehtes\work\Nazish Project\JanZ Code Explainer\backend"
```

### Step 3: Create Virtual Environment (Optional but Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

Expected output:

```
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 python-dotenv-1.0.0 groq-0.4.1 pydantic-2.5.3
```

### Step 5: Configure Environment Variables

```powershell
# Copy example file
copy .env.example .env

# Edit with your API key
notepad .env
```

In `.env`, replace the placeholder:

```
GROQ_API_KEY=gsk_your_actual_api_key_from_groq_console
```

**Get your API key:**

1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up / Log in
3. Click "Create API Key"
4. Copy the key
5. Paste it in `.env`

### Step 6: Run the Server

```powershell
# Standard run
uvicorn main:app --reload

# Or specify host and port explicitly
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Expected Output:**

```
INFO:     Will watch for changes in these directories: ['C:\\Users\\ehtes\\work\\Nazish Project\\JanZ Code Explainer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Starting AI Code Explainer API...
INFO:     Testing Groq API connection...
INFO:     ✓ Groq API connection successful
INFO:     Application startup complete.
```

**The server is now running!** Keep this terminal open.

---

## Testing the Backend

### Method 1: Browser

Open [http://localhost:8000](http://localhost:8000)

You should see:

```json
{
  "name": "AI Code Explainer API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "explain": "/api/explain (POST)",
    "health": "/health (GET)",
    "docs": "/docs (GET)"
  }
}
```

### Method 2: Health Check

Open [http://localhost:8000/health](http://localhost:8000/health)

You should see:

```json
{
  "status": "healthy",
  "groq_api": "connected",
  "model": "llama-3.3-70b-versatile"
}
```

### Method 3: Interactive API Docs

Open [http://localhost:8000/docs](http://localhost:8000/docs)

1. Click on **POST /api/explain**
2. Click **"Try it out"**
3. Enter test code:

```json
{
  "code": "print('Hello, World!')"
}
```

4. Click **"Execute"**
5. See the response with explanation

### Method 4: cURL (Command Line)

```powershell
curl -X POST "http://localhost:8000/api/explain" -H "Content-Type: application/json" -d "{\"code\":\"def add(a, b):\n    return a + b\"}"
```

### Method 5: Python Script

Create `test_api.py`:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/explain",
    json={"code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)"}
)

print(response.json()["explanation"])
```

Run:

```powershell
python test_api.py
```

---

## API Endpoint Details

### **POST /api/explain**

Explains code using LLaMA 3.3 70B Versatile.

**Request Body:**

```json
{
  "code": "string (1-10000 characters, required)"
}
```

**Success Response (200 OK):**

```json
{
  "explanation": "**Overview**: This function...\n\n**Detailed Breakdown**:..."
}
```

**Error Responses:**

- **422 Unprocessable Entity** - Invalid request format

```json
{
  "detail": [
    {
      "loc": ["body", "code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

- **500 Internal Server Error** - API error or server issue

```json
{
  "detail": "Invalid API key. Please check your GROQ_API_KEY in .env file."
}
```

### **GET /**

Root endpoint with API information.

**Response (200 OK):**

```json
{
  "name": "AI Code Explainer API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {...}
}
```

### **GET /health**

Health check endpoint.

**Response (200 OK):**

```json
{
  "status": "healthy" | "degraded",
  "groq_api": "connected" | "disconnected",
  "model": "llama-3.3-70b-versatile"
}
```

---

## Configuration Options

### Environment Variables (.env)

```bash
# Required
GROQ_API_KEY=your_api_key_here

# Optional (defaults shown)
# MAX_CODE_LENGTH=10000
# REQUEST_TIMEOUT=30
# LOG_LEVEL=INFO
```

### Uvicorn Server Options

```powershell
# Development (auto-reload on file changes)
uvicorn main:app --reload

# Custom host and port
uvicorn main:app --host 0.0.0.0 --port 8080

# Production (no reload, multiple workers)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With log level
uvicorn main:app --reload --log-level debug
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**

```powershell
pip install -r requirements.txt
```

### Issue: "GROQ_API_KEY not configured"

**Solution:**

1. Check `.env` file exists in backend directory
2. Verify format: `GROQ_API_KEY=gsk_...` (no spaces, no quotes)
3. Restart the server after changing `.env`

### Issue: "Address already in use"

**Solution:**

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
uvicorn main:app --port 8001 --reload
```

### Issue: "uvicorn: command not found"

**Solution:**

```powershell
# Make sure you're in the virtual environment (if using one)
.\venv\Scripts\Activate.ps1

# Or install globally
pip install uvicorn

# Or run as module
python -m uvicorn main:app --reload
```

### Issue: Slow responses or timeouts

**Possible Causes:**

- Slow internet connection
- Groq API service issues
- Very large code snippets

**Solutions:**

- Check internet connection
- Try smaller code snippet
- Check Groq status page
- Increase timeout in `groq_integration.py`

### Issue: CORS errors from frontend

**Solution:**
The backend already has CORS configured to allow all origins. If you still get errors:

1. Make sure backend is running
2. Clear browser cache
3. Check console for specific error
4. Verify API URL is correct: `http://localhost:8000`

---

## Development Tips

### Enable Debug Mode

Edit `main.py`, set logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

### View All Logs

Watch the terminal where uvicorn is running. You'll see:

- Request logs
- Connection status
- Errors and exceptions
- Performance timing

### Test with Different Code

Try various programming languages:

- Python, JavaScript, Java, C++, C#
- Algorithms, data structures, web code
- Short snippets and longer functions

### Check API Usage

Monitor your Groq API usage at:
[https://console.groq.com](https://console.groq.com)

---

## Performance Optimization

### For Development

- Use `--reload` flag for auto-restart on code changes
- Single worker is sufficient

### For Production (Future)

- Remove `--reload` flag
- Use multiple workers: `--workers 4`
- Deploy behind reverse proxy (Nginx)
- Use environment variables instead of `.env`
- Enable HTTPS
- Configure CORS for specific domains
- Add rate limiting
- Implement caching for common queries

---

## Next Steps

After setting up the backend:

1. ✅ Verify backend is running (`http://localhost:8000`)
2. ✅ Test the `/health` endpoint
3. ✅ Try the `/docs` interactive interface
4. ✅ Set up the frontend (see frontend section)
5. ✅ Test end-to-end with the web interface

---

**Backend setup complete! The server is ready to receive requests from the frontend.** 🚀
