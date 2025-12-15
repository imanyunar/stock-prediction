"""
Price Prediction Module
Predict future stock prices using various methods
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_price(stock_data, indicators):
    """
    Predict future stock prices
    
    Args:
        stock_data (dict): Historical stock data
        indicators (dict): Technical indicators
    
    Returns:
        dict: Price predictions
    """
    try:
        closes = [float(x) for x in stock_data['close']]
        current_price = closes[-1]
        
        # Get trend from indicators
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', 0)
        ma20 = indicators.get('ma20', current_price)
        ma50 = indicators.get('ma50', current_price)
        
        # Calculate volatility
        volatility = calculate_volatility(closes)
        
        # Determine trend strength
        trend_strength = calculate_trend_strength(closes, ma20, ma50, rsi, macd)
        
        # Make predictions
        predictions = {
            'next_hour': predict_next_period(current_price, trend_strength, volatility, 1),
            'next_day': predict_next_period(current_price, trend_strength, volatility, 24),
            'next_week': predict_next_period(current_price, trend_strength, volatility, 168),
            'confidence': calculate_confidence(volatility, len(closes))
        }
        
        # Linear regression prediction
        lr_prediction = linear_regression_predict(closes)
        predictions['ml_prediction'] = lr_prediction
        
        print(f"✅ Generated predictions for next periods")
        return predictions
        
    except Exception as e:
        print(f"❌ Error making predictions: {str(e)}")
        current = float(stock_data['close'][-1]) if stock_data['close'] else 100.0
        return {
            'next_hour': current,
            'next_day': current,
            'next_week': current,
            'confidence': 50
        }


def predict_next_period(current_price, trend_strength, volatility, hours):
    """
    Predict price for next period
    
    Args:
        current_price (float): Current stock price
        trend_strength (float): Trend strength (-1 to 1)
        volatility (float): Price volatility
        hours (int): Number of hours ahead
    
    Returns:
        float: Predicted price
    """
    # Base prediction on trend
    trend_factor = 1 + (trend_strength * 0.001 * hours)
    
    # Add some randomness based on volatility
    random_factor = np.random.uniform(-volatility/100, volatility/100)
    
    predicted_price = current_price * trend_factor * (1 + random_factor)
    
    return float(predicted_price)


def calculate_volatility(prices, period=20):
    """Calculate price volatility"""
    try:
        prices = np.array(prices[-period:])
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns) * 100
        return float(volatility)
    except:
        return 2.0


def calculate_trend_strength(prices, ma20, ma50, rsi, macd):
    """
    Calculate trend strength
    
    Returns:
        float: Trend strength from -1 (strong bearish) to 1 (strong bullish)
    """
    try:
        current_price = prices[-1]
        strength = 0
        
        # Price vs MA20 (weight: 0.3)
        if current_price > ma20:
            strength += 0.3
        elif current_price < ma20:
            strength -= 0.3
        
        # MA20 vs MA50 (weight: 0.2)
        if ma20 > ma50:
            strength += 0.2
        elif ma20 < ma50:
            strength -= 0.2
        
        # RSI (weight: 0.3)
        if rsi > 70:
            strength -= 0.3  # Overbought
        elif rsi > 50:
            strength += 0.15
        elif rsi < 30:
            strength += 0.3  # Oversold
        elif rsi < 50:
            strength -= 0.15
        
        # MACD (weight: 0.2)
        if macd > 0:
            strength += 0.2
        elif macd < 0:
            strength -= 0.2
        
        return float(np.clip(strength, -1, 1))
    except:
        return 0.0


def calculate_confidence(volatility, data_points):
    """
    Calculate prediction confidence
    
    Returns:
        float: Confidence percentage (0-100)
    """
    try:
        # Base confidence
        confidence = 70
        
        # Reduce confidence for high volatility
        confidence -= min(volatility * 2, 30)
        
        # Reduce confidence for less data
        if data_points < 30:
            confidence -= (30 - data_points)
        
        return float(np.clip(confidence, 0, 100))
    except:
        return 50.0


def linear_regression_predict(prices, periods_ahead=5):
    """
    Use linear regression to predict future prices
    
    Args:
        prices (list): Historical prices
        periods_ahead (int): Number of periods to predict
    
    Returns:
        float: Predicted price
    """
    try:
        # Use last 30 data points
        data = np.array(prices[-30:])
        X = np.arange(len(data)).reshape(-1, 1)
        y = data
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict
        future_x = np.array([[len(data) + periods_ahead]])
        prediction = model.predict(future_x)[0]
        
        return float(prediction)
    except:
        return float(prices[-1]) if prices else 0.0


def calculate_support_resistance(prices, window=20):
    """
    Calculate support and resistance levels
    
    Args:
        prices (list): Historical prices
        window (int): Lookback window
    
    Returns:
        dict: Support and resistance levels
    """
    try:
        recent_prices = np.array(prices[-window:])
        
        support = float(np.min(recent_prices))
        resistance = float(np.max(recent_prices))
        
        return {
            'support': support,
            'resistance': resistance,
            'range': resistance - support
        }
    except:
        current = float(prices[-1]) if prices else 0.0
        return {
            'support': current * 0.95,
            'resistance': current * 1.05,
            'range': current * 0.1
        }


def calculate_risk_reward(current_price, target_price, stop_loss):
    """
    Calculate risk-reward ratio
    
    Args:
        current_price (float): Current price
        target_price (float): Target price
        stop_loss (float): Stop loss price
    
    Returns:
        dict: Risk-reward analysis
    """
    try:
        potential_reward = target_price - current_price
        potential_risk = current_price - stop_loss
        
        if potential_risk <= 0:
            ratio = 0
        else:
            ratio = potential_reward / potential_risk
        
        return {
            'ratio': float(ratio),
            'reward': float(potential_reward),
            'risk': float(potential_risk),
            'recommendation': 'Good' if ratio >= 2 else 'Poor' if ratio < 1 else 'Fair'
        }
    except:
        return {
            'ratio': 0,
            'reward': 0,
            'risk': 0,
            'recommendation': 'Unknown'
        }


# Test function
if __name__ == '__main__':
    print("\n" + "="*50)
    print("Testing Price Prediction Module")
    print("="*50 + "\n")
    
    # Test with sample data
    sample_data = {
        'close': [100 + i + np.random.uniform(-2, 2) for i in range(100)]
    }
    
    sample_indicators = {
        'rsi': 55.0,
        'macd': 0.5,
        'ma20': 102.0,
        'ma50': 101.0
    }
    
    predictions = predict_price(sample_data, sample_indicators)
    
    print("Predictions:")
    print(f"  Next Hour: ${predictions['next_hour']:.2f}")
    print(f"  Next Day: ${predictions['next_day']:.2f}")
    print(f"  Next Week: ${predictions['next_week']:.2f}")
    print(f"  ML Prediction: ${predictions['ml_prediction']:.2f}")
    print(f"  Confidence: {predictions['confidence']:.1f}%")
    
    # Test support/resistance
    sr = calculate_support_resistance(sample_data['close'])
    print(f"\nSupport/Resistance:")
    print(f"  Support: ${sr['support']:.2f}")
    print(f"  Resistance: ${sr['resistance']:.2f}")
    
    print("\n" + "="*50)