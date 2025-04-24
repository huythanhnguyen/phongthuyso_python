#!/usr/bin/env python3
"""
Debug imports và modules
"""

import sys
import os
import inspect

# Đường dẫn tới các module
print("=== PYTHON PATH ===")
for path in sys.path:
    print(path)

# Kiểm tra các module đã import
print("\n=== IMPORTED MODULES ===")
for name, module in sys.modules.items():
    if 'agent' in name.lower():
        print(f"{name}: {getattr(module, '__file__', 'No file')}")

# Import RootAgent và kiểm tra
print("\n=== ROOT AGENT MODULE ===")
try:
    from agents.root_agent import RootAgent
    print(f"RootAgent module: {inspect.getmodule(RootAgent).__file__}")
    print(f"RootAgent class definition: {inspect.getsource(RootAgent)}")
    
    # Tạo instance và kiểm tra method
    print("\n=== ROOT AGENT METHODS ===")
    agent = RootAgent()
    print(f"process_direct_root_request method: {inspect.getsource(agent.process_direct_root_request)}")
except Exception as e:
    print(f"Error importing RootAgent: {e}")

print("\n=== DONE ===") 