"""
View all documents stored in ChromaDB
"""
from rag_system import get_rag_system
import json

def view_all_documents():
    """Display all documents in the database"""
    print("=" * 80)
    print("CHROMADB VECTOR DATABASE VIEWER")
    print("=" * 80)
    
    rag = get_rag_system()
    collection = rag.collection
    
    # Get all documents
    results = collection.get()
    
    total = len(results['documents'])
    print(f"\n📊 Total Documents: {total}\n")
    
    if total == 0:
        print("⚠️  Database is empty. Run: python ingest_documents.py --reset")
        return
    
    # Display each document
    for i, (doc_id, doc, metadata) in enumerate(zip(
        results['ids'], 
        results['documents'], 
        results['metadatas']
    ), 1):
        print(f"\n{'='*80}")
        print(f"📄 Document {i}/{total}")
        print(f"{'='*80}")
        print(f"ID: {doc_id}")
        print(f"Language: {metadata.get('language', 'N/A').upper()}")
        print(f"Category: {metadata.get('category', 'N/A')}")
        print(f"Subcategory: {metadata.get('subcategory', 'N/A')}")
        print(f"Difficulty: {metadata.get('difficulty', 'N/A')}")
        
        # Show explanation if available
        explanation = metadata.get('explanation', '')
        if explanation:
            print(f"\nExplanation (first 150 chars):")
            print("-" * 80)
            print(explanation[:150] + "..." if len(explanation) > 150 else explanation)
            print("-" * 80)
        
        print(f"\nCode Preview (first 300 chars):")
        print("-" * 80)
        print(doc[:300] + "..." if len(doc) > 300 else doc)
        print("-" * 80)
    
    # Summary statistics
    print(f"\n{'='*80}")
    print("📈 SUMMARY STATISTICS")
    print(f"{'='*80}")
    
    # Count by language
    languages = {}
    categories = {}
    difficulties = {}
    
    for metadata in results['metadatas']:
        lang = metadata.get('language', 'unknown')
        cat = metadata.get('category', 'unknown')
        diff = metadata.get('difficulty', 'unknown')
        
        languages[lang] = languages.get(lang, 0) + 1
        categories[cat] = categories.get(cat, 0) + 1
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print(f"\n📚 By Language:")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        print(f"   {lang.upper()}: {count}")
    
    print(f"\n🏷️  By Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count}")
    
    print(f"\n⭐ By Difficulty:")
    for diff, count in sorted(difficulties.items(), key=lambda x: x[1], reverse=True):
        print(f"   {diff.upper()}: {count}")
    
    print(f"\n{'='*80}")
    print(f"✅ Viewing complete: {total} documents displayed")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    view_all_documents()
