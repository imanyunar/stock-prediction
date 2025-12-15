"""
Technical Indicators Module
Calculate various technical indicators for stock analysis
"""

import pandas as pd
import numpy as np


def calculate_indicators(stock_data):
    """
    Calculate technical indicators from stock data
    
    Args:
        stock_data (dict): Stock data with close, high, low, volume
    
    Returns:
        dict: Technical indicators
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame({
            'close': [float(x) for x in stock_data['close']],
            'high': [float(x) for x in stock_data['high']],
            'low': [float(x) for x in stock_data['low']],
            'volume': [float(x) for x in stock_data['volume']]
        })
        
        indicators = {}
        
        # RSI (Relative Strength Index)
        indicators['rsi'] = calculate_rsi(df['close'])
        
        # MACD
        macd_data = calculate_macd(df['close'])
        indicators['macd'] = macd_data['macd']
        indicators['macd_signal'] = macd_data['signal']
        indicators['macd_histogram'] = macd_data['histogram']
        
        # Moving Averages
        indicators['ma20'] = calculate_ma(df['close'], 20)
        indicators['ma50'] = calculate_ma(df['close'], 50)
        indicators['ma200'] = calculate_ma(df['close'], 200)
        
        # Exponential Moving Averages
        indicators['ema12'] = calculate_ema(df['close'], 12)
        indicators['ema26'] = calculate_ema(df['close'], 26)
        
        # Bollinger Bands
        bb = calculate_bollinger_bands(df['close'])
        indicators['bb_upper'] = bb['upper']
        indicators['bb_middle'] = bb['middle']
        indicators['bb_lower'] = bb['lower']
        
        # Stochastic Oscillator
        stoch = calculate_stochastic(df['high'], df['low'], df['close'])
        indicators['stoch_k'] = stoch['k']
        indicators['stoch_d'] = stoch['d']
        
        # ATR (Average True Range)
        indicators['atr'] = calculate_atr(df['high'], df['low'], df['close'])
        
        # Volume indicators
        indicators['volume_ma'] = calculate_ma(df['volume'], 20)
        
        print(f"✅ Calculated {len(indicators)} technical indicators")
        return indicators
        
    except Exception as e:
        print(f"❌ Error calculating indicators: {str(e)}")
        return {
            'rsi': 50,
            'macd': 0,
            'ma20': stock_data['close'][-1] if stock_data['close'] else 0,
            'ma50': stock_data['close'][-1] if stock_data['close'] else 0
        }


def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index"""
    try:
        prices = pd.Series([float(x) for x in prices])
        delta = prices.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi.iloc[-1]) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0
    except:
        return 50.0


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    try:
        prices = pd.Series([float(x) for x in prices])
        
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return {
            'macd': float(macd.iloc[-1]) if not macd.empty else 0.0,
            'signal': float(signal_line.iloc[-1]) if not signal_line.empty else 0.0,
            'histogram': float(histogram.iloc[-1]) if not histogram.empty else 0.0
        }
    except:
        return {'macd': 0.0, 'signal': 0.0, 'histogram': 0.0}


def calculate_ma(prices, period):
    """Calculate Simple Moving Average"""
    try:
        prices = pd.Series([float(x) for x in prices])
        ma = prices.rolling(window=period).mean()
        return float(ma.iloc[-1]) if not ma.empty and not pd.isna(ma.iloc[-1]) else float(prices.iloc[-1])
    except:
        return float(prices.iloc[-1]) if len(prices) > 0 else 0.0


def calculate_ema(prices, period):
    """Calculate Exponential Moving Average"""
    try:
        prices = pd.Series([float(x) for x in prices])
        ema = prices.ewm(span=period, adjust=False).mean()
        return float(ema.iloc[-1]) if not ema.empty else float(prices.iloc[-1])
    except:
        return float(prices.iloc[-1]) if len(prices) > 0 else 0.0


def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    try:
        prices = pd.Series([float(x) for x in prices])
        
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return {
            'upper': float(upper.iloc[-1]) if not upper.empty else float(prices.iloc[-1]) * 1.05,
            'middle': float(middle.iloc[-1]) if not middle.empty else float(prices.iloc[-1]),
            'lower': float(lower.iloc[-1]) if not lower.empty else float(prices.iloc[-1]) * 0.95
        }
    except:
        current = float(prices.iloc[-1]) if len(prices) > 0 else 0.0
        return {
            'upper': current * 1.05,
            'middle': current,
            'lower': current * 0.95
        }


def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """Calculate Stochastic Oscillator"""
    try:
        high = pd.Series([float(x) for x in high])
        low = pd.Series([float(x) for x in low])
        close = pd.Series([float(x) for x in close])
        
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d = k.rolling(window=d_period).mean()
        
        return {
            'k': float(k.iloc[-1]) if not k.empty and not pd.isna(k.iloc[-1]) else 50.0,
            'd': float(d.iloc[-1]) if not d.empty and not pd.isna(d.iloc[-1]) else 50.0
        }
    except:
        return {'k': 50.0, 'd': 50.0}


def calculate_atr(high, low, close, period=14):
    """Calculate Average True Range"""
    try:
        high = pd.Series([float(x) for x in high])
        low = pd.Series([float(x) for x in low])
        close = pd.Series([float(x) for x in close])
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return float(atr.iloc[-1]) if not atr.empty and not pd.isna(atr.iloc[-1]) else 0.0
    except:
        return 0.0


# Test function
if __name__ == '__main__':
    print("\n" + "="*50)
    print("Testing Technical Indicators Module")
    print("="*50 + "\n")
    
    # Test with sample data
    sample_data = {
        'close': [100 + i + np.random.uniform(-2, 2) for i in range(100)],
        'high': [102 + i + np.random.uniform(-1, 3) for i in range(100)],
        'low': [98 + i + np.random.uniform(-3, 1) for i in range(100)],
        'volume': [1000000 + np.random.randint(-100000, 100000) for i in range(100)]
    }
    
    indicators = calculate_indicators(sample_data)
    
    print("Calculated Indicators:")
    print(f"  RSI: {indicators['rsi']:.2f}")
    print(f"  MACD: {indicators['macd']:.2f}")
    print(f"  MA(20): {indicators['ma20']:.2f}")
    print(f"  MA(50): {indicators['ma50']:.2f}")
    print(f"  BB Upper: {indicators['bb_upper']:.2f}")
    print(f"  BB Lower: {indicators['bb_lower']:.2f}")
    print(f"  Stochastic K: {indicators['stoch_k']:.2f}")
    print(f"  ATR: {indicators['atr']:.2f}")
    
    print("\n" + "="*50)