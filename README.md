# 🤖 AI Code Explainer - Phase 1

A web application that uses **LLaMA 3.3 70B Versatile** (via Groq) to provide instant, comprehensive explanations of code snippets in any programming language.

## 📋 Project Overview

This project demonstrates the integration of a state-of-the-art Large Language Model (LLaMA 3.3 70B) into a practical web application for code explanation. Users can paste any code snippet and receive detailed, educational explanations powered by AI.

**Tech Stack:**

- **Backend**: FastAPI (Python)
- **LLM**: LLaMA 3.3 70B Versatile via Groq API
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Localhost (Development)

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Groq API key (free at [console.groq.com](https://console.groq.com/keys))
- A modern web browser

### Step 1: Get Your Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for a free account (if you don't have one)
3. Create a new API key
4. Copy the key (you'll need it in Step 3)

### Step 2: Install Backend Dependencies

```powershell
# Navigate to the backend directory
cd backend

# Install required Python packages
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

```powershell
# Copy the example environment file
copy .env.example .env

# Open .env in a text editor and add your Groq API key
# Replace 'your_groq_api_key_here' with your actual API key
notepad .env
```

Your `.env` file should look like:

```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### Step 4: Run the Backend Server

```powershell
# Make sure you're in the backend directory
# Start the FastAPI server
uvicorn main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Starting AI Code Explainer API...
INFO:     ✓ Groq API connection successful
```

**Keep this terminal window open!** The backend must be running for the application to work.

### Step 5: Open the Frontend

1. Open a new terminal or File Explorer
2. Navigate to the `frontend` directory
3. Open `index.html` in your web browser:
   - **Option 1**: Double-click `index.html`
   - **Option 2**: Right-click → Open with → Your browser
   - **Option 3**: Drag the file into your browser window

### Step 6: Use the Application

1. **Paste Code**: Copy any code snippet into the text area
2. **Click "Explain Code"**: The AI will analyze your code
3. **Read Explanation**: View the comprehensive explanation
4. **Try Examples**: Click example buttons to test different languages

---

## 📁 Project Structure

```
JanZ Code Explainer/
│
├── backend/
│   ├── main.py                 # FastAPI server with /api/explain endpoint
│   ├── groq_integration.py     # Groq API integration with LLaMA 3.3 70B
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── .env                   # Your API key (create this)
│
├── frontend/
│   └── index.html             # Web interface
│
├── PHASE1_DOCUMENTATION.md    # Domain & LLM justification
├── README.md                  # This file
└── .gitignore                # Git ignore rules
```

---

## 🔧 Backend API Documentation

### **POST /api/explain**

Explains a code snippet using LLaMA 3.3 70B Versatile.

**Request:**

```json
{
  "code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)"
}
```

**Response:**

```json
{
  "explanation": "**Overview**: This code implements a recursive factorial function...\n\n**Detailed Breakdown**:..."
}
```

**Other Endpoints:**

- `GET /` - API information
- `GET /health` - Health check and Groq connection status
- `GET /docs` - Interactive API documentation (Swagger UI)

### Testing the API

You can test the API directly using the interactive docs:

1. Make sure the backend is running
2. Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser
3. Try the `/api/explain` endpoint

Or use curl:

```powershell
curl -X POST "http://localhost:8000/api/explain" -H "Content-Type: application/json" -d "{\"code\":\"print('Hello, World!')\"}"
```

---

## 🎯 Features

### Current Features (Phase 1)

✅ **Multi-Language Support**: Explains code in Python, JavaScript, Java, C++, and more  
✅ **Comprehensive Explanations**: Includes overview, detailed breakdown, key concepts, and potential issues  
✅ **Fast Response**: Groq's LPU provides 300-800 tokens/second inference speed  
✅ **Clean UI**: Modern, responsive interface with loading animations  
✅ **Error Handling**: Graceful error messages for connectivity and API issues  
✅ **Example Code**: Pre-loaded examples for quick testing  
✅ **Copy Function**: One-click copy of explanations

### Supported Programming Languages

- Python
- JavaScript / TypeScript
- Java
- C / C++
- C#
- Go
- Rust
- PHP
- Ruby
- Swift
- Kotlin
- And many more!

---

## 🐛 Troubleshooting

### Backend Issues

**"GROQ_API_KEY not configured"**

- Make sure you created the `.env` file in the `backend` directory
- Verify your API key is correct (no extra spaces or quotes)
- The line should be: `GROQ_API_KEY=gsk_your_key_here`

**"ModuleNotFoundError: No module named 'fastapi'"**

- Run `pip install -r requirements.txt` in the backend directory
- Make sure you're using the correct Python environment

**"Address already in use"**

- Another application is using port 8000
- Stop the other application or use a different port:
  ```powershell
  uvicorn main:app --reload --port 8001
  ```
- Update the API_URL in `frontend/index.html` to match

**"Groq API connection failed"**

- Check your internet connection
- Verify your API key is valid at [console.groq.com](https://console.groq.com/keys)
- Check Groq's status page if the service is down

### Frontend Issues

**"Could not connect to the server"**

- Make sure the backend is running (check terminal)
- Verify the backend is accessible at [http://localhost:8000](http://localhost:8000)
- Check browser console (F12) for detailed error messages

**CORS Errors**

- Make sure you're running the backend with `--reload` flag
- The CORS middleware is configured to allow all origins
- Try clearing browser cache (Ctrl+Shift+Delete)

**Explanation not appearing**

- Check browser console (F12) for JavaScript errors
- Verify the API response in Network tab
- Try a simpler code example first

---

## 📊 System Requirements

### Minimum Requirements

- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM**: 4GB (8GB recommended)
- **Python**: 3.8 or higher
- **Internet**: Stable connection for API calls
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Performance Expectations

- **Typical Response Time**: 1-3 seconds
- **API Rate Limit**: Varies by Groq free tier (check console.groq.com)
- **Max Code Length**: 10,000 characters per request

---

## 🔒 Security Notes

- **Never commit your `.env` file** to version control (already in `.gitignore`)
- **Keep your API key private** - don't share it publicly
- **For production deployment**:
  - Use environment variables instead of `.env` files
  - Configure CORS to allow only your frontend domain
  - Add rate limiting to prevent abuse
  - Use HTTPS for all connections

---

## 📚 Documentation

For detailed information about the project:

- **Domain Justification**: See `PHASE1_DOCUMENTATION.md` - Section 1
- **LLM Selection Rationale**: See `PHASE1_DOCUMENTATION.md` - Section 2
- **Technical Architecture**: This README + code comments
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (when backend is running)

---

## 🎓 Educational Use

This project demonstrates:

- **AI Integration**: Practical use of LLMs in web applications
- **API Development**: RESTful API design with FastAPI
- **Async Programming**: Async/await patterns in Python
- **Web Development**: Frontend-backend communication
- **Error Handling**: Robust error handling and user feedback
- **Environment Management**: Secure configuration with environment variables

---

## 🚧 Future Enhancements (Phase 2+)

Potential features for future phases:

- 🔍 Code quality analysis and bug detection
- ⚡ Performance optimization suggestions
- 🔄 Code refactoring recommendations
- 🔐 Security vulnerability identification
- 💬 Interactive Q&A about code
- 📝 Automatic documentation generation
- 🌐 Multi-file project analysis
- 👥 User authentication and history
- 📊 Usage analytics dashboard

---

## 🤝 Contributing

This is a Phase 1 CS project. For educational purposes, the codebase is kept simple and well-commented. Feel free to:

- Report issues
- Suggest improvements
- Fork and experiment
- Use as a learning resource

---

## 📄 License

This project is created for educational purposes as part of a CS course assignment.

---

## 👨‍💻 Author

**Course**: Computer Science - AI/LLM Integration Project  
**Phase**: 1 - Core Functionality  
**Model**: LLaMA 3.3 70B Versatile (Meta AI via Groq)

---

## 🙏 Acknowledgments

- **Meta AI** for LLaMA 3.3 70B model
- **Groq** for fast, free inference infrastructure
- **FastAPI** for the excellent Python web framework
- The open-source community for inspiration and tools

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the error messages carefully
3. Check the browser console (F12) for frontend errors
4. Check the terminal output for backend errors
5. Verify all prerequisites are met
6. Ensure your API key is valid and properly configured

---

**Ready to explain some code? Let's get started! 🚀**
