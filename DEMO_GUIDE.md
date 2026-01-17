# JanZ Code Explainer - Demonstration Guide

Complete guide for demonstrating the AI Code Explainer with Chat History functionality.

---

## 📋 Prerequisites Check

Before starting, verify you have:

- Docker Desktop installed and running
- Git Bash or PowerShell terminal
- Web browser (Chrome/Firefox recommended)

---

## 🚀 Part 1: Starting the Application

### Step 1: Navigate to Project Directory

```bash
cd "c:\Users\ehtes\work\Nazish Project\JanZ Code Explainer"
```

### Step 2: Start Docker Containers

```bash
# Build and start the backend container
docker-compose up -d --build

# Verify container is running and healthy
docker ps
```

**Expected Output:**

```
CONTAINER ID   IMAGE                       STATUS                    PORTS
5ff6362e855e   janzcodeexplainer-backend   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp
```

### Step 3: Verify API is Running

```bash
# Check health endpoint
curl http://localhost:8000/health

# Or in PowerShell:
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Expected Output:**

```json
{
  "status": "healthy",
  "groq_api": "connected",
  "model": "llama-3.3-70b-versatile"
}
```

---

## 💻 Part 2: Using the Application

### Open the Frontend

```bash
# Open the chat history interface
start frontend/index_chat_history.html

# Or manually open in browser:
# file:///c:/Users/ehtes/work/Nazish%20Project/JanZ%20Code%20Explainer/frontend/index_chat_history.html
```

### Test the Application

1. **Click "New Chat"** to start a conversation
2. **Select Language**: Choose Python (or any language)
3. **Paste Sample Code**:
   ```python
   def fibonacci(n):
       if n <= 1:
           return n
       return fibonacci(n-1) + fibonacci(n-2)
   ```
4. **Click "🚀 Explain"** (Basic mode)
5. **Try RAG Mode**: Toggle to "🎯 RAG" and paste another code snippet
6. **View Sidebar**: See conversation list populate with history

---

## 🐳 Part 3: Accessing the Docker Container

### Enter the Container Shell

```bash
# Access the running container
docker-compose exec backend bash
```

**You're now inside the container! The prompt will change to:**

```
root@5ff6362e855e:/app#
```

### Explore the Container Structure

```bash
# List files in the working directory
ls -la

# View Python files
ls -la *.py

# Check database directory
ls -la chroma_db/
```

---

## 🗄️ Part 4: Viewing ChromaDB (Vector Database)

### Using the Built-in Viewer Script

```bash
# View ChromaDB statistics and contents
python view_database.py
```

**This will show:**

- Total documents indexed
- Languages available
- Categories and difficulty levels
- Sample code examples stored

### Using Python Interactive Shell

```bash
python3
```

Then inside Python:

```python
from rag_system import get_rag_system

# Initialize RAG system
rag = get_rag_system()

# Get collection info
collection = rag.collection
print(f"Total documents: {collection.count()}")

# Get sample documents
results = collection.get(limit=5)
print(f"Sample IDs: {results['ids']}")
print(f"Sample metadata: {results['metadatas'][0]}")

# Test retrieval
similar = rag.retrieve("def factorial(n):", top_k=3)
print(f"Found {len(similar)} similar examples")

# Exit Python
exit()
```

### Query ChromaDB Directly

```bash
python3 -c "
from rag_system import get_rag_system
rag = get_rag_system()
print('ChromaDB Statistics:')
print(f'  Total Documents: {rag.collection.count()}')
results = rag.collection.get(limit=1)
if results['metadatas']:
    print(f'  Sample Language: {results[\"metadatas\"][0].get(\"language\")}')
    print(f'  Sample Category: {results[\"metadatas\"][0].get(\"category\")}')
"
```

---

## 💾 Part 5: Viewing SQLite Chat History Database

### Option A: Using the Python Viewer (Recommended)

```bash
# View database statistics
python view_chat_history.py stats

# View all conversations
python view_chat_history.py conversations

# View all messages
python view_chat_history.py messages

# View specific conversation (use first 8 chars of ID from conversations list)
python view_chat_history.py conversation <conversation-id>

# Interactive menu with all options
python view_chat_history.py
```

**Example Output:**

```
============================================================
📊 CHAT HISTORY DATABASE STATISTICS
============================================================
Total Conversations:    3
Total Messages:         12
  └─ User Messages:     6
  └─ Assistant Messages: 6
RAG-Enhanced Messages:  4
============================================================
```

### Option B: Using SQLite3 Command Line

**First, install SQLite3 in the container:**

```bash
apt-get update && apt-get install -y sqlite3
```

**Then use it:**

```bash
# Open the database
sqlite3 chroma_db/chat_history.db
```

**Inside SQLite prompt:**

```sql
-- List all tables
.tables

-- Show table structures
.schema conversations
.schema messages

-- Set better display format
.mode column
.headers on
.width 36 20 10 20

-- View all conversations
SELECT id, title, created_at, updated_at FROM conversations;

-- View all messages
SELECT role, language, timestamp
FROM messages
ORDER BY timestamp DESC
LIMIT 10;

-- Count records
SELECT COUNT(*) as total_conversations FROM conversations;
SELECT COUNT(*) as total_messages FROM messages;

-- Get detailed statistics
SELECT
    (SELECT COUNT(*) FROM conversations) as convs,
    (SELECT COUNT(*) FROM messages) as msgs,
    (SELECT COUNT(*) FROM messages WHERE rag_mode = 1) as rag_msgs;

-- View messages in a conversation (replace with actual conversation_id)
SELECT role, substr(content, 1, 50) as preview, timestamp
FROM messages
WHERE conversation_id = 'your-conversation-id-here'
ORDER BY timestamp;

-- Exit SQLite
.exit
```

### Option C: Using Python One-Liners

```bash
# Quick statistics
python3 -c "
from chat_history import get_chat_db
db = get_chat_db()
stats = db.get_statistics()
print('Chat History Stats:')
for key, value in stats.items():
    print(f'  {key}: {value}')
"

# List conversations
python3 -c "
from chat_history import get_chat_db
db = get_chat_db()
convs = db.get_user_conversations()
print('Conversations:')
for c in convs:
    print(f'  {c[\"id\"][:8]}... | {c[\"title\"]} | {c[\"message_count\"]} msgs')
"

# View messages from first conversation
python3 -c "
from chat_history import get_chat_db
db = get_chat_db()
convs = db.get_user_conversations(limit=1)
if convs:
    msgs = db.get_conversation_messages(convs[0]['id'])
    print(f'Messages in: {convs[0][\"title\"]}')
    for m in msgs:
        print(f'  {m[\"role\"]}: {m[\"content\"][:60]}...')
"
```

---

## 🔍 Part 6: Testing the Chat History API

### Exit Container (if inside)

```bash
exit
```

### From Host Machine (PowerShell/Git Bash)

```bash
# Get all conversations
curl http://localhost:8000/api/conversations

# In PowerShell:
Invoke-RestMethod -Uri "http://localhost:8000/api/conversations"

# Get chat statistics
curl http://localhost:8000/api/chat/stats

# In PowerShell:
Invoke-RestMethod -Uri "http://localhost:8000/api/chat/stats"

# Get RAG statistics (ChromaDB)
curl http://localhost:8000/api/rag/stats

# In PowerShell:
Invoke-RestMethod -Uri "http://localhost:8000/api/rag/stats"

# Test explanation endpoint with chat history
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello World\")", "language": "python"}'

# In PowerShell:
$body = @{code = "print('Hello World')"; language = "python"} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/explain" -Body $body -ContentType "application/json"
```

---

## 📊 Part 7: Demonstrating Key Features

### Show Dual Database Architecture

```bash
# Inside container:
docker-compose exec backend bash

# Show both databases
echo "=== DATABASE FILES ==="
ls -lh chroma_db/

# ChromaDB (for vector search)
echo -e "\n=== CHROMADB STATS ==="
python view_database.py

# SQLite (for chat history)
echo -e "\n=== CHAT HISTORY STATS ==="
python view_chat_history.py stats
```

### Show RAG Retrieval in Action

```bash
# Inside container or from host:
python3 -c "
from rag_system import get_rag_system

rag = get_rag_system()
query = 'def bubble_sort(arr):'

print(f'Query: {query}')
print('\\nRetrieving similar examples...')

results = rag.retrieve(query, top_k=3)

print(f'\\nFound {len(results)} similar examples:')
for i, doc in enumerate(results, 1):
    print(f'{i}. {doc[\"metadata\"][\"language\"].upper()} - {doc[\"metadata\"][\"category\"]}')
    print(f'   Relevance: {doc[\"relevance_score\"]:.2%}')
"
```

### Show Chat History Persistence

```bash
# Create a conversation
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "x = [1,2,3]", "language": "python"}'

# View it in database
docker-compose exec backend python view_chat_history.py conversations
```

---

## 🛑 Part 8: Stopping the Application

```bash
# Stop containers
docker-compose down

# Stop and remove volumes (careful - deletes data!)
docker-compose down -v

# Restart containers
docker-compose up -d
```

---

## 📁 Part 9: Database File Locations

### Inside Container:

- **ChromaDB**: `/app/chroma_db/chroma.sqlite3`
- **Chat History**: `/app/chroma_db/chat_history.db`
- **ChromaDB Collections**: `/app/chroma_db/e245d90c-1eec-471d-a58f-92c9fc9ae26a/`

### On Host Machine (if volume mounted):

- **All databases**: `backend/chroma_db/`

### Copy Database from Container to Host:

```bash
# Copy chat history database
docker cp ai-code-explainer-backend:/app/chroma_db/chat_history.db ./chat_history_backup.db

# Copy entire chroma_db folder
docker cp ai-code-explainer-backend:/app/chroma_db ./chroma_db_backup
```

---

## 🎯 Quick Demo Script

```bash
# 1. Start everything
cd "c:\Users\ehtes\work\Nazish Project\JanZ Code Explainer"
docker-compose up -d
echo "Waiting for container to be healthy..."
sleep 10

# 2. Open frontend
start frontend/index_chat_history.html

# 3. Create test conversation via API
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)", "language": "python"}'

# 4. View databases
docker-compose exec backend python view_chat_history.py stats
docker-compose exec backend python view_database.py

# 5. Show API endpoints
echo "Available Endpoints:"
echo "  Frontend: file:///frontend/index_chat_history.html"
echo "  API Docs: http://localhost:8000/docs"
echo "  Health: http://localhost:8000/health"
echo "  Chat Stats: http://localhost:8000/api/chat/stats"
echo "  RAG Stats: http://localhost:8000/api/rag/stats"
```

---

## 📝 API Endpoints Reference

### Chat History Endpoints:

- `POST /api/conversations` - Create new conversation
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/{id}` - Get conversation messages
- `DELETE /api/conversations/{id}` - Delete conversation
- `GET /api/chat/stats` - Chat history statistics

### Explanation Endpoints:

- `POST /api/explain` - Basic code explanation (saves to chat history)
- `POST /api/explain-rag` - RAG-enhanced explanation (saves to chat history)

### Other Endpoints:

- `GET /health` - System health check
- `GET /api/rag/stats` - ChromaDB statistics
- `GET /docs` - Interactive API documentation

---

## 🏆 Key Points to Demonstrate

1. **Dual Database System**:

   - ChromaDB for vector search (code examples)
   - SQLite for chat history (conversations)

2. **Chat History Like ChatGPT**:

   - Sidebar with conversation list
   - Persistent message history
   - RAG mode tracking

3. **RAG Enhancement**:

   - Retrieves similar code examples
   - Enhances explanations with context
   - Shows relevance scores

4. **Docker Deployment**:

   - Containerized application
   - Easy to deploy and scale
   - Persistent data volumes

5. **Professional API**:
   - RESTful endpoints
   - Comprehensive documentation
   - Error handling and validation

---

## 🐛 Troubleshooting

### Container not starting:

```bash
docker-compose logs backend
```

### Database not accessible:

```bash
docker-compose exec backend ls -la chroma_db/
```

### Port already in use:

```bash
# Change port in docker-compose.yaml from 8000:8000 to 8001:8000
docker-compose down
docker-compose up -d
```

### Reset everything:

```bash
docker-compose down -v
docker-compose up -d --build
```

---

**End of Demonstration Guide**
