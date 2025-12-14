"""
Diagnostic script to test imports step by step
"""
import sys
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("DIAGNOSTIC IMPORT TEST")
print("=" * 60)

try:
    print("\n1. Testing basic imports...")
    sys.stdout.flush()
    
    import numpy
    print(f"   ✓ numpy {numpy.__version__}")
    sys.stdout.flush()
    
    import torch
    print(f"   ✓ torch {torch.__version__}")
    sys.stdout.flush()
    
    print("\n2. Testing transformers...")
    sys.stdout.flush()
    
    import transformers
    print(f"   ✓ transformers {transformers.__version__}")
    sys.stdout.flush()
    
    print("\n3. Testing sentence_transformers (this is where it usually fails)...")
    sys.stdout.flush()
    
    import sentence_transformers
    print(f"   ✓ sentence_transformers {sentence_transformers.__version__}")
    sys.stdout.flush()
    
    print("\n4. Testing SentenceTransformer class...")
    sys.stdout.flush()
    
    from sentence_transformers import SentenceTransformer
    print("   ✓ SentenceTransformer class imported")
    sys.stdout.flush()
    
    print("\n" + "=" * 60)
    print("ALL IMPORTS SUCCESSFUL!")
    print("=" * 60)
    print("\nYou can now use the regular download script.")
    
except Exception as e:
    print(f"\n✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
