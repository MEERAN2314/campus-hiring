#!/usr/bin/env python3
"""
Test script to verify Gemini API is working
"""

from google import genai
from app.config import settings

print("Testing Gemini API...")
print(f"API Key: {settings.GOOGLE_API_KEY[:10]}..." if settings.GOOGLE_API_KEY else "No API key found!")
print(f"Model: {settings.GEMINI_MODEL}")

try:
    # Configure Gemini
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    
    # Test simple generation
    print("\nTesting simple generation...")
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents="Say 'Hello, World!' in JSON format"
    )
    print(f"Response: {response.text}")
    
    print("\n✅ Gemini API is working!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. API quota exceeded")
    print("3. Model name incorrect")
    print("4. Network/firewall issues")

