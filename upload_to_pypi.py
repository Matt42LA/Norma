#!/usr/bin/env python3
"""
Upload Norma ORM to PyPI

This script uploads the built package to PyPI with proper error handling
and verification steps.

WARNING: This script is for project maintainers only.
Make sure you have the necessary permissions before running.
Never commit API tokens or credentials to version control.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {description} failed")
        print(f"Command: {cmd}")
        print(f"Error: {result.stderr}")
        return False
    
    print(f"✅ {description} completed successfully")
    if result.stdout:
        print(f"Output: {result.stdout}")
    return True

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check if dist directory exists and has files
    dist_path = Path("dist")
    if not dist_path.exists():
        print("❌ Error: dist/ directory not found. Run 'python -m build' first.")
        return False
    
    # Check for wheel and tar.gz files
    wheel_files = list(dist_path.glob("*.whl"))
    tar_files = list(dist_path.glob("*.tar.gz"))
    
    if not wheel_files or not tar_files:
        print("❌ Error: Missing wheel or tar.gz files in dist/")
        print("Run 'python -m build' to create distribution files.")
        return False
    
    print(f"✅ Found {len(wheel_files)} wheel file(s) and {len(tar_files)} tar.gz file(s)")
    
    # Check if twine is installed
    try:
        import twine
        print("✅ Twine is available")
    except ImportError:
        print("❌ Error: twine not installed. Run 'pip install twine'")
        return False
    
    return True

def verify_package():
    """Verify the package before upload."""
    print("\n📦 Verifying package...")
    
    # Check package with twine
    if not run_command("twine check dist/*", "Package verification"):
        return False
    
    return True

def upload_to_test_pypi():
    """Upload to Test PyPI first for verification."""
    print("\n🧪 Uploading to Test PyPI...")
    print("This allows you to test the package without affecting the real PyPI.")
    
    cmd = "twine upload --repository testpypi dist/*"
    print(f"Command: {cmd}")
    print("\nNote: You'll need Test PyPI credentials.")
    print("Create an account at: https://test.pypi.org/account/register/")
    
    confirm = input("Upload to Test PyPI? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Test PyPI upload skipped")
        return False
    
    return run_command(cmd, "Test PyPI upload")

def upload_to_pypi():
    """Upload to the real PyPI."""
    print("\n🚀 Uploading to PyPI...")
    print("⚠️  WARNING: This will make the package publicly available!")
    
    cmd = "twine upload dist/*"
    print(f"Command: {cmd}")
    print("\nNote: You'll need PyPI credentials.")
    print("Create an account at: https://pypi.org/account/register/")
    
    confirm = input("Upload to PyPI? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ PyPI upload skipped")
        return False
    
    return run_command(cmd, "PyPI upload")

def main():
    """Main upload process."""
    print("🚀 Norma ORM PyPI Upload Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Verify package
    if not verify_package():
        sys.exit(1)
    
    print("\n📋 Package Information:")
    print("Package name: norma-orm")
    print("Version: 0.1.0")
    print("Author: Geoion")
    print("Description: A modern Python ORM framework with dataclass support")
    
    print("\n🗂️  Files to upload:")
    for file in Path("dist").glob("*"):
        print(f"  - {file.name} ({file.stat().st_size} bytes)")
    
    print("\n📝 Upload Options:")
    print("1. Upload to Test PyPI first (recommended)")
    print("2. Upload directly to PyPI")
    print("3. Exit")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        # Upload to Test PyPI first
        if upload_to_test_pypi():
            print("\n✅ Test PyPI upload successful!")
            print("Test installation with:")
            print("pip install --index-url https://test.pypi.org/simple/ norma-orm")
            
            # Ask if they want to upload to real PyPI
            print("\nAfter testing, you can upload to the real PyPI:")
            if upload_to_pypi():
                print("\n🎉 Successfully uploaded to PyPI!")
                print("Installation command: pip install norma-orm")
        
    elif choice == "2":
        # Upload directly to PyPI
        if upload_to_pypi():
            print("\n🎉 Successfully uploaded to PyPI!")
            print("Installation command: pip install norma-orm")
    
    elif choice == "3":
        print("👋 Upload cancelled")
        
    else:
        print("❌ Invalid choice")
        sys.exit(1)

if __name__ == "__main__":
    main() 