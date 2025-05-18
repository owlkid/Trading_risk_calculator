# Trading System

A comprehensive trading tool that includes a Position Size Calculator and Trade Journal.

## Features

- Position Size Calculator with risk management
- Trade Journal with Excel export
- Customizable Symbol Watchlist
- Leverage suggestions based on stop loss
- Trade direction tracking (Long/Short)

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python Trading_calculator.py
```

2. Calculator Features:
   - Enter your risk percentage (default 3%)
   - Input your total capital
   - Set your stop loss percentage
   - The calculator will suggest appropriate leverage
   - Click "Calculate Position" to see position size and margin required

3. Trade Journal:
   - Select a symbol from your watchlist
   - Choose trade direction (Long/Short)
   - Enter entry price and notes
   - Click "Save Trade" to record the trade
   - Use "View Journal" to open the Excel file

4. Watchlist Management:
   - Add new symbols using the "Add" button
   - Remove symbols using the "Remove Selected" button
   - All symbols are automatically saved

## Files

- `Trading_Rules.py` - Main application
- `trade_journal.xlsx` - Excel file for trade records
- `watchlist.json` - Saved watchlist configuration
- `calculator.ico` - Application icon

## Support

For any issues or feature requests, please contact the developer. 
