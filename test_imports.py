#!/usr/bin/env python3
"""
Test script to validate import structure without requiring dependencies
"""

import sys
import os
import ast

def check_python_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def main():
    """Check all Python files for syntax errors"""
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print("🔍 Checking Python file syntax...")
    print("=" * 50)
    
    errors = []
    for file_path in python_files:
        valid, error = check_python_syntax(file_path)
        if valid:
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: {error}")
            errors.append((file_path, error))
    
    print("=" * 50)
    
    if errors:
        print(f"❌ Found {len(errors)} syntax errors:")
        for file_path, error in errors:
            print(f"  - {file_path}: {error}")
        return 1
    else:
        print(f"✅ All {len(python_files)} Python files have valid syntax!")
        return 0

if __name__ == "__main__":
    sys.exit(main())