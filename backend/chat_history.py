"""
Chat History Database Manager
Manages conversation history using SQLite for persistent storage
Stores user prompts and chatbot responses similar to ChatGPT
"""

import sqlite3
import uuid
import json
from datetime import datetime
from typing import List, Dict, Optional
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class ChatHistoryDB:
    """SQLite database manager for chat history"""
    
    def __init__(self, db_path: str = "chroma_db/chat_history.db"):
        """
        Initialize SQLite database for chat history
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
        logger.info(f"Chat history database initialized at {db_path}")
    
    def _init_database(self):
        """Create tables if they don't exist"""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    user_id TEXT DEFAULT 'default',
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    code_snippet TEXT,
                    language TEXT,
                    rag_context TEXT,
                    rag_mode BOOLEAN DEFAULT 0,
                    retrieved_count INTEGER DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                );
                
                CREATE INDEX IF NOT EXISTS idx_conv_user ON conversations(user_id, updated_at DESC);
                CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id, timestamp ASC);
            """)
            logger.info("Database tables created/verified successfully")
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise e
        finally:
            conn.close()
    
    def create_conversation(self, user_id: str = "default", title: str = "New Chat") -> str:
        """
        Create a new conversation and return its ID
        
        Args:
            user_id: User identifier (default for anonymous users)
            title: Conversation title
            
        Returns:
            Conversation ID (UUID)
        """
        conv_id = str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO conversations (id, user_id, title) VALUES (?, ?, ?)",
                (conv_id, user_id, title)
            )
        logger.info(f"Created new conversation: {conv_id}")
        return conv_id
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        code_snippet: Optional[str] = None,
        language: Optional[str] = None,
        rag_context: Optional[str] = None,
        rag_mode: bool = False,
        retrieved_count: int = 0
    ) -> str:
        """
        Add a message to a conversation
        
        Args:
            conversation_id: ID of the conversation
            role: 'user' or 'assistant'
            content: Message content (explanation for assistant, code for user)
            code_snippet: Original code snippet (for user messages)
            language: Programming language
            rag_context: JSON string of retrieved RAG examples
            rag_mode: Whether RAG mode was used
            retrieved_count: Number of retrieved examples
            
        Returns:
            Message ID (UUID)
        """
        msg_id = str(uuid.uuid4())
        with self._get_connection() as conn:
            conn.execute(
                """INSERT INTO messages 
                   (id, conversation_id, role, content, code_snippet, language, 
                    rag_context, rag_mode, retrieved_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (msg_id, conversation_id, role, content, code_snippet, language, 
                 rag_context, rag_mode, retrieved_count)
            )
            # Update conversation updated_at timestamp
            conn.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conversation_id,)
            )
        logger.info(f"Added {role} message to conversation {conversation_id}")
        return msg_id
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 100) -> List[Dict]:
        """
        Get all messages in a conversation ordered by timestamp
        
        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """SELECT id, role, content, code_snippet, language, rag_context, 
                          rag_mode, retrieved_count, timestamp
                   FROM messages 
                   WHERE conversation_id = ?
                   ORDER BY timestamp ASC
                   LIMIT ?""",
                (conversation_id, limit)
            )
            messages = []
            for row in cursor.fetchall():
                msg = dict(row)
                # Parse RAG context from JSON if present
                if msg['rag_context']:
                    try:
                        msg['rag_context'] = json.loads(msg['rag_context'])
                    except json.JSONDecodeError:
                        msg['rag_context'] = None
                messages.append(msg)
            return messages
    
    def get_user_conversations(self, user_id: str = "default", limit: int = 50) -> List[Dict]:
        """
        Get all conversations for a user ordered by last update
        
        Args:
            user_id: User identifier
            limit: Maximum number of conversations to retrieve
            
        Returns:
            List of conversation dictionaries with message counts
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """SELECT c.id, c.title, c.created_at, c.updated_at,
                          (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count,
                          (SELECT content FROM messages WHERE conversation_id = c.id 
                           AND role = 'user' ORDER BY timestamp ASC LIMIT 1) as first_message_preview
                   FROM conversations c
                   WHERE c.user_id = ?
                   ORDER BY c.updated_at DESC
                   LIMIT ?""",
                (user_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_conversation(self, conversation_id: str):
        """
        Delete a conversation and all its messages (CASCADE)
        
        Args:
            conversation_id: ID of the conversation to delete
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        logger.info(f"Deleted conversation: {conversation_id}")
    
    def update_conversation_title(self, conversation_id: str, title: str):
        """
        Update conversation title (auto-generate from first message)
        
        Args:
            conversation_id: ID of the conversation
            title: New title for the conversation
        """
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (title, conversation_id)
            )
        logger.info(f"Updated conversation title: {conversation_id} -> {title}")
    
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict]:
        """
        Get conversation metadata by ID
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Conversation dictionary or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """SELECT id, user_id, title, created_at, updated_at
                   FROM conversations
                   WHERE id = ?""",
                (conversation_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def clear_all_history(self, user_id: str = "default"):
        """
        Clear all conversation history for a user (use with caution!)
        
        Args:
            user_id: User identifier
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        logger.warning(f"Cleared all conversation history for user: {user_id}")
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with database stats
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM conversations) as total_conversations,
                    (SELECT COUNT(*) FROM messages) as total_messages,
                    (SELECT COUNT(*) FROM messages WHERE role = 'user') as user_messages,
                    (SELECT COUNT(*) FROM messages WHERE role = 'assistant') as assistant_messages,
                    (SELECT COUNT(*) FROM messages WHERE rag_mode = 1) as rag_enhanced_messages
            """)
            row = cursor.fetchone()
            return dict(row) if row else {}


# Singleton instance
_chat_db_instance = None


def get_chat_db() -> ChatHistoryDB:
    """
    Get or create the ChatHistoryDB singleton instance
    
    Returns:
        ChatHistoryDB instance
    """
    global _chat_db_instance
    if _chat_db_instance is None:
        _chat_db_instance = ChatHistoryDB()
    return _chat_db_instance
