#!/usr/bin/env python3
"""
Educational Payload - Auto-Execution Demo
This prints "Hello World" when executed
Educational purposes only - Intro to Cybersecurity
"""

import sys
import time

def main():
    # Simple payload - prints message
    print("=" * 50)
    print("Hello World!")
    print("=" * 50)
    print("[*] This executable was auto-executed!")
    print("[*] Educational demonstration for cybersecurity")
    print("[*] Timestamp:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Keep window open for a moment
    time.sleep(2)

if __name__ == "__main__":
    main()
