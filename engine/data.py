"""
Stock Data Module
Handles fetching and processing stock data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(ticker, interval='1d', period='1mo'):
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        interval (str): Data interval - '1m', '5m', '15m', '1h', '1d', '1wk', '1mo'
        period (str): Data period - '1d', '5d', '1mo', '3mo', '6mo', '1y', '5y'
    
    Returns:
        dict: Stock data with dates, open, high, low, close, volume
        {
            'dates': ['2024-01-01', '2024-01-02', ...],
            'open': [150.0, 151.0, ...],
            'high': [152.0, 153.0, ...],
            'low': [149.0, 150.0, ...],
            'close': [151.0, 152.0, ...],
            'volume': [1000000, 1100000, ...]
        }
    """
    try:
        print(f"📊 Fetching data for {ticker} with interval {interval}...")
        
        # Create ticker object
        stock = yf.Ticker(ticker)
        
        # Fetch historical data
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            print(f"❌ No data found for {ticker}")
            return {'error': f'No data found for {ticker}'}
        
        # Format dates based on interval
        if interval in ['1m', '5m', '15m', '30m', '1h']:
            date_format = '%Y-%m-%d %H:%M'
        else:
            date_format = '%Y-%m-%d'
        
        # Prepare data
        data = {
            'ticker': ticker,
            'interval': interval,
            'dates': df.index.strftime(date_format).tolist(),
            'open': df['Open'].tolist(),
            'high': df['High'].tolist(),
            'low': df['Low'].tolist(),
            'close': df['Close'].tolist(),
            'volume': df['Volume'].tolist()
        }
        
        print(f"✅ Successfully fetched {len(data['dates'])} data points for {ticker}")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {str(e)}")
        return {'error': str(e)}


def get_current_price(ticker):
    """
    Get current stock price
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        float: Current stock price or None if error
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get('currentPrice') or info.get('regularMarketPrice')
    except:
        return None


def get_stock_info(ticker):
    """
    Get detailed stock information
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Stock information
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'beta': info.get('beta', 0),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0)
        }
    except Exception as e:
        print(f"Error getting stock info: {str(e)}")
        return {}


def validate_ticker(ticker):
    """
    Validate if ticker symbol exists
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return 'currentPrice' in info or 'regularMarketPrice' in info
    except:
        return False


def get_intraday_data(ticker, interval='15m'):
    """
    Get intraday stock data
    
    Args:
        ticker (str): Stock ticker symbol
        interval (str): Interval - '1m', '5m', '15m', '30m', '1h'
    
    Returns:
        dict: Intraday stock data
    """
    # For intraday, use shorter period
    period_map = {
        '1m': '1d',
        '5m': '5d',
        '15m': '5d',
        '30m': '1mo',
        '1h': '1mo'
    }
    
    period = period_map.get(interval, '5d')
    return get_stock_data(ticker, interval, period)


def get_daily_data(ticker, period='1y'):
    """
    Get daily stock data
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Period - '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'
    
    Returns:
        dict: Daily stock data
    """
    return get_stock_data(ticker, '1d', period)


# Test function
if __name__ == '__main__':
    # Test with AAPL
    print("\n" + "="*50)
    print("Testing Stock Data Module")
    print("="*50 + "\n")
    
    # Test 1: Get daily data
    print("Test 1: Daily data for AAPL")
    data = get_stock_data('AAPL', '1d', '1mo')
    if 'error' not in data:
        print(f"✅ Got {len(data['dates'])} days of data")
        print(f"Latest close: ${data['close'][-1]:.2f}")
    else:
        print(f"❌ {data['error']}")
    
    # Test 2: Get current price
    print("\nTest 2: Current price")
    price = get_current_price('AAPL')
    if price:
        print(f"✅ Current AAPL price: ${price:.2f}")
    
    # Test 3: Get stock info
    print("\nTest 3: Stock info")
    info = get_stock_info('AAPL')
    if info:
        print(f"✅ {info.get('name', 'N/A')}")
        print(f"   Sector: {info.get('sector', 'N/A')}")
    
    print("\n" + "="*50)