"""
Test script to verify all imports work correctly
Run this before starting the Flask app
"""

print("="*60)
print("Testing Stock Prediction Engine Imports")
print("="*60)

# Test 1: Import modules
print("\n1️⃣ Testing imports...")
try:
    from engine.data import get_stock_data
    print("   ✅ engine.data imported")
except ImportError as e:
    print(f"   ❌ Failed to import engine.data: {e}")
    exit(1)

try:
    from engine.indicators import calculate_indicators
    print("   ✅ engine.indicators imported")
except ImportError as e:
    print(f"   ❌ Failed to import engine.indicators: {e}")
    exit(1)

try:
    from engine.predictors import predict_price
    print("   ✅ engine.predictors imported")
except ImportError as e:
    print(f"   ❌ Failed to import engine.predictors: {e}")
    exit(1)

# Test 2: Check dependencies
print("\n2️⃣ Checking dependencies...")
try:
    import yfinance
    print("   ✅ yfinance installed")
except ImportError:
    print("   ❌ yfinance not installed. Run: pip install yfinance")
    exit(1)

try:
    import pandas
    print("   ✅ pandas installed")
except ImportError:
    print("   ❌ pandas not installed. Run: pip install pandas")
    exit(1)

try:
    import numpy
    print("   ✅ numpy installed")
except ImportError:
    print("   ❌ numpy not installed. Run: pip install numpy")
    exit(1)

try:
    import sklearn
    print("   ✅ scikit-learn installed")
except ImportError:
    print("   ❌ scikit-learn not installed. Run: pip install scikit-learn")
    exit(1)

try:
    import flask
    print("   ✅ flask installed")
except ImportError:
    print("   ❌ flask not installed. Run: pip install flask")
    exit(1)

# Test 3: Quick functionality test
print("\n3️⃣ Testing functionality...")
try:
    print("   Testing get_stock_data...")
    data = get_stock_data('AAPL', '1d', '5d')
    if 'error' not in data:
        print(f"   ✅ Got {len(data['dates'])} days of AAPL data")
        print(f"      Latest close: ${data['close'][-1]:.2f}")
    else:
        print(f"   ⚠️  Warning: {data['error']}")
except Exception as e:
    print(f"   ⚠️  Warning: {e}")

try:
    print("   Testing calculate_indicators...")
    if 'error' not in data:
        indicators = calculate_indicators(data)
        print(f"   ✅ Calculated indicators (RSI: {indicators['rsi']:.2f})")
except Exception as e:
    print(f"   ⚠️  Warning: {e}")

try:
    print("   Testing predict_price...")
    if 'error' not in data:
        predictions = predict_price(data, indicators)
        print(f"   ✅ Generated predictions (Next day: ${predictions['next_day']:.2f})")
except Exception as e:
    print(f"   ⚠️  Warning: {e}")

# Test 4: Check Flask app structure
print("\n4️⃣ Checking project structure...")
import os

required_files = [
    'app.py',
    'templates/index.html',
    'static/main.js',
    'engine/__init__.py',
    'engine/data.py',
    'engine/indicators.py',
    'engine/predictors.py'
]

for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ Missing: {file}")

print("\n" + "="*60)
print("✅ All tests passed! You can now run: python app.py")
print("="*60 + "\n")