#!/usr/bin/env python3
"""
Installation Test Script
Verifies that all required dependencies are installed correctly
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name}: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 Testing Technical Analysis Pro Installation")
    print("="*60 + "\n")
    
    print("Testing Python dependencies...\n")
    
    dependencies = [
        ("flask", "Flask"),
        ("flask_cors", "Flask-CORS"),
        ("flask_socketio", "Flask-SocketIO"),
        ("yfinance", "yfinance"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("ta", "ta (Technical Analysis)"),
        ("scipy", "scipy"),
        ("sklearn", "scikit-learn"),
        ("google.generativeai", "Google Generative AI"),
    ]
    
    results = []
    for module, name in dependencies:
        results.append(test_import(module, name))
    
    print("\n" + "="*60)
    
    if all(results):
        print("✅ All dependencies installed successfully!")
        print("\nYou're ready to run the application:")
        print("  ./start.sh              (Development mode)")
        print("  ./start_production.sh   (Production mode)")
    else:
        print("❌ Some dependencies are missing!")
        print("\nPlease run:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print("="*60 + "\n")
    
    # Test core modules
    print("Testing core modules...\n")
    
    core_modules = [
        "technical_analysis",
        "html_report",
        "visualization",
        "app"
    ]
    
    core_results = []
    for module in core_modules:
        core_results.append(test_import(module))
    
    print("\n" + "="*60)
    
    if all(core_results):
        print("✅ All core modules loaded successfully!")
    else:
        print("⚠️  Some core modules had issues")
    
    print("="*60 + "\n")
    
    # Python version check
    print("Python version check...\n")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 9:
        print("✅ Python version is compatible (3.9+)")
    else:
        print("⚠️  Python 3.9+ recommended (you have {}.{}.{})".format(
            version.major, version.minor, version.micro))
    
    print("\n" + "="*60)
    print("🎉 Installation test complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
