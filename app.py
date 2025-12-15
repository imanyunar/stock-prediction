from flask import Flask, render_template, request, jsonify
from engine.data import get_stock_data
from engine.indicators import calculate_indicators
from engine.predictors import predict_price
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main API endpoint for stock analysis
    Expected JSON body:
    {
        "ticker": "AAPL",
        "interval": "1d"
    }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()
        interval = data.get('interval', '1d')
        
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400
        
        # Get stock data using your existing engine modules
        stock_data = get_stock_data(ticker, interval)
        
        if not stock_data or 'error' in stock_data:
            return jsonify({
                'error': f'Failed to fetch data for {ticker}'
            }), 404
        
        # Calculate technical indicators
        indicators = calculate_indicators(stock_data)
        
        # Get predictions
        predictions = predict_price(stock_data, indicators)
        
        # Prepare response
        current_price = float(stock_data['close'][-1])
        previous_price = float(stock_data['close'][-2]) if len(stock_data['close']) > 1 else current_price
        price_change = current_price - previous_price
        price_change_percent = (price_change / previous_price * 100) if previous_price > 0 else 0
        
        # Determine signal based on indicators
        signal = determine_signal(indicators)
        
        response = {
            'ticker': ticker,
            'interval': interval,
            'current_price': current_price,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
            'signal': signal,
            'rsi': indicators.get('rsi', 50),
            'indicators': {
                'rsi': indicators.get('rsi', 50),
                'macd': indicators.get('macd', 0),
                'ma20': indicators.get('ma20', current_price),
                'ma50': indicators.get('ma50', current_price),
            },
            'predictions': {
                'next_hour': predictions.get('next_hour', current_price),
                'next_day': predictions.get('next_day', current_price),
                'next_week': predictions.get('next_week', current_price),
                'confidence': predictions.get('confidence', 75)
            },
            'trend': {
                'short_term': determine_trend(indicators, 'short'),
                'medium_term': determine_trend(indicators, 'medium'),
                'long_term': determine_trend(indicators, 'long')
            },
            'volume': stock_data.get('volume', [0])[-1] if 'volume' in stock_data else 0,
            'volatility': calculate_volatility(stock_data),
            'risk_level': determine_risk_level(indicators),
            'support': calculate_support(stock_data),
            'resistance': calculate_resistance(stock_data),
            'chart_data': {
                'dates': stock_data.get('dates', []),
                'open': stock_data.get('open', []),
                'high': stock_data.get('high', []),
                'low': stock_data.get('low', []),
                'close': stock_data.get('close', [])
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

def determine_signal(indicators):
    """Determine BUY/SELL/HOLD signal based on indicators"""
    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    
    buy_signals = 0
    sell_signals = 0
    
    # RSI signals
    if rsi < 30:
        buy_signals += 1
    elif rsi > 70:
        sell_signals += 1
    
    # MACD signals
    if macd > 0:
        buy_signals += 1
    elif macd < 0:
        sell_signals += 1
    
    if buy_signals > sell_signals:
        return 'BUY'
    elif sell_signals > buy_signals:
        return 'SELL'
    else:
        return 'HOLD'

def determine_trend(indicators, timeframe):
    """Determine trend for different timeframes"""
    ma20 = indicators.get('ma20', 0)
    ma50 = indicators.get('ma50', 0)
    
    if ma20 > ma50:
        return 'Bullish 📈'
    elif ma20 < ma50:
        return 'Bearish 📉'
    else:
        return 'Neutral ➡️'

def calculate_volatility(stock_data):
    """Calculate volatility from stock data"""
    import numpy as np
    closes = [float(x) for x in stock_data.get('close', [])]
    if len(closes) < 2:
        return 0
    
    returns = np.diff(closes) / closes[:-1]
    volatility = np.std(returns) * np.sqrt(252) * 100  # Annualized
    return float(volatility)

def determine_risk_level(indicators):
    """Determine risk level"""
    rsi = indicators.get('rsi', 50)
    
    if rsi > 70 or rsi < 30:
        return 'High'
    elif rsi > 60 or rsi < 40:
        return 'Medium'
    else:
        return 'Low'

def calculate_support(stock_data):
    """Calculate support level"""
    import numpy as np
    lows = [float(x) for x in stock_data.get('low', [])]
    if not lows:
        return 0
    return float(np.min(lows[-20:]))  # Last 20 days minimum

def calculate_resistance(stock_data):
    """Calculate resistance level"""
    import numpy as np
    highs = [float(x) for x in stock_data.get('high', [])]
    if not highs:
        return 0
    return float(np.max(highs[-20:]))  # Last 20 days maximum

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)