import sys
import os

# Add current directory to Python path for app imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.rag import get_rag_service
    import inspect
    
    def check_rag_method():
        print("🔍 RAG Service Method Inspection")
        print("=" * 40)
        
        try:
            rag_service = get_rag_service()
            print(f"✅ RAG Service Type: {type(rag_service)}")
            
            if hasattr(rag_service, 'add_knowledge'):
                method = rag_service.add_knowledge
                print("✅ add_knowledge method exists")
                
                try:
                    sig = inspect.signature(method)
                    print(f"📋 Method Signature: add_knowledge{sig}")
                    print(f"📝 Parameters: {list(sig.parameters.keys())}")
                    
                    # Show parameter details
                    for param_name, param in sig.parameters.items():
                        default = f" = {param.default}" if param.default != inspect.Parameter.empty else ""
                        print(f"   - {param_name}: {param.annotation}{default}")
                        
                except Exception as e:
                    print(f"❌ Could not inspect signature: {e}")
                
                # Try to get docstring
                doc = inspect.getdoc(method)
                if doc:
                    print(f"📚 Documentation: {doc}")
                    
            else:
                print("❌ add_knowledge method NOT found")
                methods = [m for m in dir(rag_service) if not m.startswith('_')]
                print(f"📋 Available methods: {methods}")
            
        except Exception as e:
            print(f"❌ Error accessing RAG service: {e}")
            import traceback
            traceback.print_exc()
    
    if __name__ == "__main__":
        check_rag_method()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📂 Python path first 3 entries: {sys.path[:3]}")
    
    # Check directory structure
    if os.path.exists('app'):
        print("✅ 'app' directory exists")
        if os.path.exists('app/core/rag.py'):
            print("✅ 'app/core/rag.py' file exists")
        else:
            print("❌ 'app/core/rag.py' file missing")
    else:
        print("❌ 'app' directory not found")
        print(f"📋 Available directories: {[d for d in os.listdir('.') if os.path.isdir(d)]}")
