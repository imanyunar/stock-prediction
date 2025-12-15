// Main JavaScript for Stock Prediction Dashboard

let currentChartData = null;

// Analyze function - calls backend API
async function analyze() {
    const ticker = document.getElementById('ticker').value.trim().toUpperCase();
    const interval = document.getElementById('interval').value;
    const loading = document.getElementById('loading');
    
    if (!ticker) {
        showError('Please enter a stock ticker');
        return;
    }
    
    // Show loading
    loading.classList.remove('hidden');
    
    try {
        // Call backend API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ticker: ticker,
                interval: interval
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Update UI with real data
        updateUI(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to fetch data. Please try again.');
    } finally {
        loading.classList.add('hidden');
    }
}

// Update UI with data from backend
function updateUI(data) {
    // Update current price
    const currentPrice = data.current_price || data.close;
    const priceChange = data.price_change || 0;
    const priceChangePercent = data.price_change_percent || 0;
    
    updateStat('price', `$${parseFloat(currentPrice).toFixed(2)}`, 
               priceChange >= 0 ? 'text-green-600' : 'text-red-600');
    
    document.getElementById('price-change').textContent = 
        `${priceChange >= 0 ? '+' : ''}${priceChangePercent.toFixed(2)}% (${priceChange >= 0 ? '+' : ''}$${Math.abs(priceChange).toFixed(2)})`;
    document.getElementById('price-change').className = 
        `text-sm mt-1 font-semibold ${priceChange >= 0 ? 'text-green-600' : 'text-red-600'}`;
    
    // Update signal
    const signal = data.signal || 'HOLD';
    const signalEmoji = signal === 'BUY' ? '🟢' : signal === 'SELL' ? '🔴' : '🟡';
    const signalColor = signal === 'BUY' ? 'text-green-600' : signal === 'SELL' ? 'text-red-600' : 'text-yellow-600';
    
    updateStat('signal', `${signal} ${signalEmoji}`, signalColor);
    
    // Update RSI
    const rsi = data.rsi || data.indicators?.rsi || 50;
    const rsiColor = rsi > 70 ? 'text-red-600' : rsi < 30 ? 'text-green-600' : 'text-blue-600';
    updateStat('rsi', parseFloat(rsi).toFixed(2), rsiColor);
    
    // Update predictions
    updatePredictions(data);
    
    // Update chart
    updateChart(data);
}

// Update stat with animation
function updateStat(id, value, colorClass) {
    const el = document.getElementById(id);
    el.style.opacity = '0';
    el.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        el.textContent = value;
        el.className = `text-3xl font-bold transition-all duration-300 ${colorClass}`;
        el.style.opacity = '1';
        el.style.transform = 'scale(1)';
    }, 150);
}

// Update predictions section
function updatePredictions(data) {
    const predictionsDiv = document.getElementById('predictions');
    const predictions = data.predictions || {};
    
    const html = `
        <div class="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-xl">
            <h4 class="font-bold text-blue-900 mb-2">📊 Technical Indicators</h4>
            <div class="space-y-1 text-sm">
                <p><span class="font-semibold">RSI:</span> ${(data.rsi || 50).toFixed(2)}</p>
                <p><span class="font-semibold">MACD:</span> ${(data.indicators?.macd || 0).toFixed(2)}</p>
                <p><span class="font-semibold">MA(20):</span> $${(data.indicators?.ma20 || data.current_price || 0).toFixed(2)}</p>
                <p><span class="font-semibold">MA(50):</span> $${(data.indicators?.ma50 || data.current_price || 0).toFixed(2)}</p>
            </div>
        </div>
        
        <div class="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-xl">
            <h4 class="font-bold text-purple-900 mb-2">🔮 Price Predictions</h4>
            <div class="space-y-1 text-sm">
                <p><span class="font-semibold">Next Hour:</span> $${(predictions.next_hour || data.current_price || 0).toFixed(2)}</p>
                <p><span class="font-semibold">Next Day:</span> $${(predictions.next_day || data.current_price || 0).toFixed(2)}</p>
                <p><span class="font-semibold">Next Week:</span> $${(predictions.next_week || data.current_price || 0).toFixed(2)}</p>
                <p><span class="font-semibold">Confidence:</span> ${(predictions.confidence || 75).toFixed(0)}%</p>
            </div>
        </div>
        
        <div class="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-xl">
            <h4 class="font-bold text-green-900 mb-2">📈 Trend Analysis</h4>
            <div class="space-y-1 text-sm">
                <p><span class="font-semibold">Short-term:</span> ${data.trend?.short_term || 'Neutral'}</p>
                <p><span class="font-semibold">Medium-term:</span> ${data.trend?.medium_term || 'Neutral'}</p>
                <p><span class="font-semibold">Long-term:</span> ${data.trend?.long_term || 'Neutral'}</p>
                <p><span class="font-semibold">Volume:</span> ${formatVolume(data.volume || 0)}</p>
            </div>
        </div>
        
        <div class="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-xl">
            <h4 class="font-bold text-orange-900 mb-2">⚠️ Risk Analysis</h4>
            <div class="space-y-1 text-sm">
                <p><span class="font-semibold">Volatility:</span> ${(data.volatility || 15).toFixed(2)}%</p>
                <p><span class="font-semibold">Risk Level:</span> ${data.risk_level || 'Medium'}</p>
                <p><span class="font-semibold">Support:</span> $${(data.support || data.current_price * 0.95 || 0).toFixed(2)}</p>
                <p><span class="font-semibold">Resistance:</span> $${(data.resistance || data.current_price * 1.05 || 0).toFixed(2)}</p>
            </div>
        </div>
    `;
    
    predictionsDiv.innerHTML = html;
}

// Update chart with candlestick data
function updateChart(data) {
    const chartData = data.chart_data || data.historical_data || {};
    
    if (!chartData.dates || chartData.dates.length === 0) {
        console.warn('No chart data available');
        return;
    }
    
    const trace = {
        x: chartData.dates,
        close: chartData.close,
        high: chartData.high,
        low: chartData.low,
        open: chartData.open,
        type: 'candlestick',
        name: data.ticker || 'Stock',
        increasing: {line: {color: '#10B981', width: 2}},
        decreasing: {line: {color: '#EF4444', width: 2}}
    };

    const layout = {
        title: {
            text: `${data.ticker || 'Stock'} - Candlestick Chart`,
            font: {
                size: 20,
                color: '#1F2937',
                family: 'system-ui, -apple-system, sans-serif'
            }
        },
        xaxis: {
            title: 'Date',
            rangeslider: {visible: false},
            gridcolor: '#E5E7EB'
        },
        yaxis: {
            title: 'Price (USD)',
            gridcolor: '#E5E7EB'
        },
        paper_bgcolor: 'rgba(255,255,255,0.9)',
        plot_bgcolor: 'rgba(255,255,255,0.5)',
        font: {
            family: 'system-ui, -apple-system, sans-serif',
            size: 12,
            color: '#374151'
        },
        hovermode: 'x unified'
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
    };

    Plotly.newPlot('chart', [trace], layout, config);
    currentChartData = data;
}

// Format volume
function formatVolume(volume) {
    if (volume >= 1e9) return `${(volume / 1e9).toFixed(2)}B`;
    if (volume >= 1e6) return `${(volume / 1e6).toFixed(2)}M`;
    if (volume >= 1e3) return `${(volume / 1e3).toFixed(2)}K`;
    return volume.toString();
}

// Show error message
function showError(message) {
    const errorToast = document.getElementById('error-toast');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorToast.classList.remove('hidden');
    
    setTimeout(() => {
        errorToast.classList.add('hidden');
    }, 5000);
}

// Enter key support
document.getElementById('ticker').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyze();
    }
});

// Initialize on page load
window.addEventListener('load', () => {
    console.log('Stock Prediction Dashboard loaded');
    // Optionally auto-load default ticker
    // analyze();
});