"""
Test script to verify all modules import correctly
Run this after installing dependencies to ensure everything is working
"""

import sys
import importlib.util

def test_imports():
    """Test that all required modules can be imported"""

    modules_to_test = [
        'typer',
        'rich', 
        'pendulum',
        'pandas',
        'numpy',
        'plotille',
        'requests',
        'bs4'  # beautifulsoup4
    ]

    print("🧪 Testing module imports...")
    print("=" * 50)

    failed_imports = []

    for module in modules_to_test:
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                failed_imports.append(module)
                print(f"❌ {module:<15} - Not found")
            else:
                print(f"✅ {module:<15} - OK")
        except Exception as e:
            failed_imports.append(module)
            print(f"❌ {module:<15} - Error: {str(e)}")

    print("=" * 50)

    if failed_imports:
        print(f"❌ {len(failed_imports)} modules failed to import:")
        for module in failed_imports:
            print(f"   - {module}")
        print("\nPlease install missing modules with:")
        print("pip install -r requirements.txt")
        return False
    else:
        print(f"✅ All {len(modules_to_test)} modules imported successfully!")
        return True

def test_local_imports():
    """Test that all local modules can be imported"""

    local_modules = [
        'config',
        'date_utils', 
        'scraper',
        'data_handler',
        'weather_display',
        'chart_generator'
    ]

    print("\n🏠 Testing local module imports...")
    print("=" * 50)

    failed_imports = []

    for module in local_modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                failed_imports.append(module)
                print(f"❌ {module:<20} - Not found")
            else:
                print(f"✅ {module:<20} - OK")
        except Exception as e:
            failed_imports.append(module)
            print(f"❌ {module:<20} - Error: {str(e)}")

    print("=" * 50)

    if failed_imports:
        print(f"❌ {len(failed_imports)} local modules failed to import:")
        for module in failed_imports:
            print(f"   - {module}")
        return False
    else:
        print(f"✅ All {len(local_modules)} local modules imported successfully!")
        return True

def show_project_status():
    """Show overall project status"""
    print("\n📋 Project Status Summary")
    print("=" * 50)

    required_files = [
        'main.py',
        'scraper.py', 
        'data_handler.py',
        'weather_display.py',
        'chart_generator.py',
        'date_utils.py',
        'config.py',
        'requirements.txt',
        'README.md'
    ]

    import os
    missing_files = []

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)

    print("=" * 50)

    if missing_files:
        print(f"❌ {len(missing_files)} files are missing")
        return False
    else:
        print("✅ All project files are present!")
        return True

def main():
    """Run all tests"""
    print("🌤️ Weather CLI Scraper - Setup Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print("=" * 50)

    # Test file presence
    files_ok = show_project_status()

    # Test external dependencies
    external_ok = test_imports()

    # Test local modules 
    local_ok = test_local_imports()

    # Final status
    print("\n🏁 Final Status")
    print("=" * 50)

    if files_ok and external_ok and local_ok:
        print("✅ All tests passed! Your Weather CLI Scraper is ready to use.")
        print("\nTo start the application, run:")
        print("   python main.py")
        print("\nFor help, run:")
        print("   python main.py --help")
    else:
        print("❌ Some tests failed. Please fix the issues above before using the application.")

    print("=" * 50)

if __name__ == "__main__":
    main()