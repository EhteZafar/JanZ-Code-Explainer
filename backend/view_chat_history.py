"""
View Chat History Database
Simple script to view conversations and messages from the SQLite database
"""

import sqlite3
from datetime import datetime
import sys

def simple_table(data, headers):
    """Simple table formatter (no external dependencies)"""
    if not data:
        return ""
    
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Build table
    lines = []
    
    # Header separator
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    lines.append(sep)
    
    # Header
    header_line = "|"
    for i, h in enumerate(headers):
        header_line += f" {h.ljust(widths[i])} |"
    lines.append(header_line)
    lines.append(sep)
    
    # Data rows
    for row in data:
        row_line = "|"
        for i, cell in enumerate(row):
            row_line += f" {str(cell).ljust(widths[i])} |"
        lines.append(row_line)
    
    lines.append(sep)
    return "\n".join(lines)

DB_PATH = "chroma_db/chat_history.db"


def view_statistics():
    """Display database statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM conversations) as total_conversations,
            (SELECT COUNT(*) FROM messages) as total_messages,
            (SELECT COUNT(*) FROM messages WHERE role = 'user') as user_messages,
            (SELECT COUNT(*) FROM messages WHERE role = 'assistant') as assistant_messages,
            (SELECT COUNT(*) FROM messages WHERE rag_mode = 1) as rag_enhanced_messages
    """)
    
    stats = cursor.fetchone()
    conn.close()
    
    print("\n" + "="*60)
    print("📊 CHAT HISTORY DATABASE STATISTICS")
    print("="*60)
    print(f"Total Conversations:    {stats[0]}")
    print(f"Total Messages:         {stats[1]}")
    print(f"  └─ User Messages:     {stats[2]}")
    print(f"  └─ Assistant Messages: {stats[3]}")
    print(f"RAG-Enhanced Messages:  {stats[4]}")
    print("="*60 + "\n")


def view_conversations():
    """Display all conversations"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.id,
            c.title,
            c.created_at,
            c.updated_at,
            (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count
        FROM conversations c
        ORDER BY c.updated_at DESC
    """)
    
    conversations = cursor.fetchall()
    conn.close()
    
    if not conversations:
        print("No conversations found.\n")
        return
    
    print("\n" + "="*100)
    print("💬 ALL CONVERSATIONS")
    print("="*100)
    
    table_data = []
    for conv in conversations:
        table_data.append([
            conv['id'][:8] + "...",
            conv['title'][:40],
            conv['message_count'],
            conv['created_at'],
            conv['updated_at']
        ])
    
    headers = ["ID", "Title", "Messages", "Created", "Updated"]
    print(simple_table(table_data, headers))
    print()


def view_conversation_details(conversation_id: str):
    """Display messages in a specific conversation"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get conversation info
    cursor.execute("SELECT * FROM conversations WHERE id = ? OR id LIKE ?", (conversation_id, conversation_id + "%"))
    conv = cursor.fetchone()
    
    if not conv:
        print(f"❌ Conversation not found: {conversation_id}\n")
        conn.close()
        return
    
    # Get messages
    cursor.execute("""
        SELECT role, content, code_snippet, language, rag_mode, retrieved_count, timestamp
        FROM messages
        WHERE conversation_id = ?
        ORDER BY timestamp ASC
    """, (conv['id'],))
    
    messages = cursor.fetchall()
    conn.close()
    
    print("\n" + "="*100)
    print(f"💬 CONVERSATION: {conv['title']}")
    print(f"ID: {conv['id']}")
    print(f"Created: {conv['created_at']} | Updated: {conv['updated_at']}")
    print("="*100 + "\n")
    
    for i, msg in enumerate(messages, 1):
        role_icon = "👤" if msg['role'] == 'user' else "🤖"
        rag_badge = f" [RAG: {msg['retrieved_count']} examples]" if msg['rag_mode'] else ""
        
        print(f"{role_icon} {msg['role'].upper()}{rag_badge} - {msg['timestamp']}")
        print("-" * 100)
        
        if msg['role'] == 'user':
            print(f"Language: {msg['language']}")
            print(f"Code:\n{msg['code_snippet'][:200]}{'...' if len(msg['code_snippet']) > 200 else ''}")
        else:
            print(f"{msg['content'][:300]}{'...' if len(msg['content']) > 300 else ''}")
        
        print()


def view_all_messages():
    """Display all messages across all conversations"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            m.conversation_id,
            c.title as conv_title,
            m.role,
            m.language,
            m.rag_mode,
            m.retrieved_count,
            m.timestamp,
            SUBSTR(m.content, 1, 50) as content_preview
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        ORDER BY m.timestamp DESC
        LIMIT 50
    """)
    
    messages = cursor.fetchall()
    conn.close()
    
    if not messages:
        print("No messages found.\n")
        return
    
    print("\n" + "="*120)
    print("📨 RECENT MESSAGES (Last 50)")
    print("="*120)
    
    table_data = []
    for msg in messages:
        conv_id = msg['conversation_id'][:8] + "..."
        rag_info = f"✓ ({msg['retrieved_count']})" if msg['rag_mode'] else "✗"
        
        table_data.append([
            conv_id,
            msg['conv_title'][:25],
            msg['role'],
            msg['language'] or "-",
            rag_info,
            msg['timestamp'],
            msg['content_preview'] + "..."
        ])
    
    headers = ["Conv ID", "Conversation", "Role", "Lang", "RAG", "Time", "Preview"]
    print(simple_table(table_data, headers))
    print()


def search_messages(search_term: str):
    """Search messages by content"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            m.conversation_id,
            c.title as conv_title,
            m.role,
            m.content,
            m.timestamp
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        WHERE m.content LIKE ?
        ORDER BY m.timestamp DESC
    """, (f"%{search_term}%",))
    
    results = cursor.fetchall()
    conn.close()
    
    print(f"\n🔍 Search Results for '{search_term}': {len(results)} matches\n")
    
    for result in results:
        print(f"Conversation: {result['conv_title']}")
        print(f"Role: {result['role']} | Time: {result['timestamp']}")
        print(f"Content: {result['content'][:200]}...")
        print("-" * 80 + "\n")


def interactive_menu():
    """Interactive menu for viewing database"""
    while True:
        print("\n" + "="*60)
        print("🗄️  CHAT HISTORY DATABASE VIEWER")
        print("="*60)
        print("1. View Statistics")
        print("2. View All Conversations")
        print("3. View Conversation Details (by ID)")
        print("4. View All Messages")
        print("5. Search Messages")
        print("6. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            view_statistics()
        elif choice == "2":
            view_conversations()
        elif choice == "3":
            conv_id = input("Enter conversation ID (full or first 8 chars): ").strip()
            view_conversation_details(conv_id)
        elif choice == "4":
            view_all_messages()
        elif choice == "5":
            term = input("Enter search term: ").strip()
            search_messages(term)
        elif choice == "6":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def main():
    """Main function"""
    print("\n🚀 Chat History Database Viewer")
    print(f"Database: {DB_PATH}\n")
    
    # Check if database exists
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.close()
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return
    
    # If arguments provided, handle them
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "stats":
            view_statistics()
        elif command == "conversations":
            view_conversations()
        elif command == "messages":
            view_all_messages()
        elif command == "conversation" and len(sys.argv) > 2:
            view_conversation_details(sys.argv[2])
        elif command == "search" and len(sys.argv) > 2:
            search_messages(sys.argv[2])
        else:
            print("Usage:")
            print("  python view_chat_history.py              - Interactive menu")
            print("  python view_chat_history.py stats        - Show statistics")
            print("  python view_chat_history.py conversations - List conversations")
            print("  python view_chat_history.py messages     - List all messages")
            print("  python view_chat_history.py conversation <id> - View conversation")
            print("  python view_chat_history.py search <term> - Search messages")
    else:
        # No arguments, start interactive menu
        interactive_menu()


if __name__ == "__main__":
    main()
