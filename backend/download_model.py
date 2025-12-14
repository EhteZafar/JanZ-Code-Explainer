"""
Pre-download sentence-transformers model with progress display
"""
import sys
import traceback

def main():
    print("=" * 60)
    print("DOWNLOADING SENTENCE-TRANSFORMERS MODEL")
    print("=" * 60)
    print("\nModel: sentence-transformers/all-MiniLM-L6-v2")
    print("Size: ~90 MB")
    print("\nThis may take 2-5 minutes depending on your internet speed...")
    print("You'll see progress updates below:\n")
    
    try:
        import time
        import warnings
        
        # Suppress NumPy warnings for cleaner output
        warnings.filterwarnings('ignore')
        
        print("Step 1: Importing sentence_transformers...")
        sys.stdout.flush()
        
        from sentence_transformers import SentenceTransformer
        
        print("✓ sentence_transformers imported successfully")
        print("\nStep 2: Initializing model download...")
        print("(This will download ~90MB and may take 2-5 minutes)")
        print("Please be patient, this is downloading in the background...")
        sys.stdout.flush()
        
        start_time = time.time()
        
        # This will show download progress from HuggingFace
        print("\n[Downloading files from HuggingFace...]")
        sys.stdout.flush()
        
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
        
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("✓ MODEL DOWNLOADED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\nDownload took: {elapsed:.1f} seconds")
        print(f"Model dimension: {model.get_sentence_embedding_dimension()}")
        print("\nThe model is now cached and ready to use.")
        print("You can now restart your server with: uvicorn main:app --reload")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n✗ Download interrupted by user (Ctrl+C)")
        print("You can run this script again to resume the download.")
        return 1
    except ImportError as e:
        print(f"\n✗ Import Error: {e}")
        print("\nPlease install sentence-transformers first:")
        print("  pip install sentence-transformers")
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        print(f"\nError type: {type(e).__name__}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Try again - downloads can sometimes fail")
        print("3. If it keeps failing, try: pip install --upgrade sentence-transformers")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
