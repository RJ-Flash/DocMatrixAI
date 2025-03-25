"""
Test script to verify imports with the new directory structure.

Run this script from the ContractAI directory using:
python -m app.test_imports
"""

import sys
import os

print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

# Test config imports
try:
    from app.config import get_settings
    settings = get_settings()
    print(f"✅ Successfully imported settings from app.config")
    print(f"   Project name: {settings.PROJECT_NAME}")
except Exception as e:
    print(f"❌ Failed to import settings from app.config: {e}")

# Test database imports
try:
    from app.database import get_db, Base
    print(f"✅ Successfully imported database components")
except Exception as e:
    print(f"❌ Failed to import database components: {e}")

# Test AI model imports
try:
    from app.ai.models.bert.clause_extractor import BertClauseExtractor
    print(f"✅ Successfully imported BertClauseExtractor")
    
    # Try to instantiate the model
    try:
        bert_model = BertClauseExtractor()
        print(f"✅ Successfully instantiated BertClauseExtractor")
    except Exception as e:
        print(f"❌ Failed to instantiate BertClauseExtractor: {e}")
        
except Exception as e:
    print(f"❌ Failed to import BertClauseExtractor: {e}")

try:
    from app.ai.models.gpt.text_analyzer import GPTTextAnalyzer
    print(f"✅ Successfully imported GPTTextAnalyzer")
    
    # Try to instantiate the model
    try:
        gpt_model = GPTTextAnalyzer()
        print(f"✅ Successfully instantiated GPTTextAnalyzer")
    except Exception as e:
        print(f"❌ Failed to instantiate GPTTextAnalyzer: {e}")
        
except Exception as e:
    print(f"❌ Failed to import GPTTextAnalyzer: {e}")

print("\n--- Import test completed ---") 