import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
import os
import json

class PositionSizeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Position Size Calculator")
        self.root.geometry("500x650")  # Made taller for watchlist management
        self.root.resizable(False, False)
        
        # Initialize files
        self.excel_file = 'trade_journal.xlsx'
        self.watchlist_file = 'watchlist.json'
        self.initialize_journal()
        self.load_watchlist()
        
        self.setup_icon()
        self.create_widgets()
        self.setup_layout()
        self.setup_validation()
        
    def initialize_journal(self):
        # Create Excel file if it doesn't exist
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=[
                'Date', 'Symbol', 'Direction', 'Entry Price', 'Position Size',
                'Stop Loss', 'Risk Amount', 'Leverage', 'Status',
                'Exit Price', 'Profit/Loss', 'Notes'
            ])
            df.to_excel(self.excel_file, index=False)
    
    def load_watchlist(self):
        # Default watchlist with trading pairs
        self.symbols = [
            "BTCUSDT", "ETHUSDT", "SUIUSDT", "SEIUSDT", "INJUSDT",
            "AEVOUSDT", "PYTHUSDT", "BNBUSDT", "APTUSDT",
            "ZKUSDT", "ZROUSDT",
            "BSUSDT", "WUSDT", "TIAUSDT", "JUPUSDT"
        ]
        
        if os.path.exists(self.watchlist_file):
            with open(self.watchlist_file, 'r') as f:
                data = json.load(f)
                self.symbols = data.get("Symbols", self.symbols)
        else:
            self.save_watchlist()
    
    def save_watchlist(self):
        with open(self.watchlist_file, 'w') as f:
            json.dump({"Symbols": self.symbols}, f, indent=4)
    
    def setup_icon(self):
        try:
            img = Image.open('calculator.png')
            photo = ImageTk.PhotoImage(img)
            self.root.iconphoto(False, photo)
        except:
            try:
                self.root.iconbitmap('calculator.ico')
            except:
                pass
    
    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Warning.TLabel', foreground='red')
        style.configure('Safety.TLabel', font=('Arial', 10, 'bold'), foreground='red', anchor='center')
        style.configure('Suggestion.TLabel', font=('Arial', 10), foreground='#006400', anchor='center')
        
        # Input Fields
        self.risk_label = ttk.Label(self.root, text="Risk per trade (%):*")
        self.risk_entry = ttk.Entry(self.root)
        self.risk_warning = ttk.Label(self.root, text="", style='Warning.TLabel')
        
        self.capital_label = ttk.Label(self.root, text="Total capital ($):*")
        self.capital_entry = ttk.Entry(self.root)
        self.capital_warning = ttk.Label(self.root, text="", style='Warning.TLabel')
        
        self.stop_loss_label = ttk.Label(self.root, text="Stop loss (%):*")
        self.stop_loss_entry = ttk.Entry(self.root)
        self.stop_loss_warning = ttk.Label(self.root, text="", style='Warning.TLabel')
        
        self.leverage_label = ttk.Label(self.root, text="Leverage:*")
        self.leverage_entry = ttk.Entry(self.root)
        self.leverage_warning = ttk.Label(self.root, text="", style='Warning.TLabel')
        
        # Calculate and Clear buttons
        self.calculate_btn = ttk.Button(
            self.root, 
            text="Calculate Position", 
            command=self.validate_fields
        )
        
        self.clear_btn = ttk.Button(
            self.root, 
            text="Clear All", 
            command=self.clear_fields
        )
        
        # Trade Journal Frame
        self.journal_frame = ttk.LabelFrame(self.root, text="Trade Journal Entry")
        
        # Symbol selection (using the watchlist dropdown)
        self.symbol_label = ttk.Label(self.journal_frame, text="Symbol:")
        self.symbol_combo = ttk.Combobox(self.journal_frame, state="readonly")
        
        # Trade Direction
        self.direction_var = tk.StringVar(value="LONG")
        self.direction_frame = ttk.Frame(self.journal_frame)
        self.long_radio = ttk.Radiobutton(self.direction_frame, text="LONG", variable=self.direction_var, value="LONG")
        self.short_radio = ttk.Radiobutton(self.direction_frame, text="SHORT", variable=self.direction_var, value="SHORT")
        
        # Entry Price
        self.entry_price_label = ttk.Label(self.journal_frame, text="Entry Price:")
        self.entry_price_entry = ttk.Entry(self.journal_frame)
        
        # Notes
        self.notes_label = ttk.Label(self.journal_frame, text="Notes:")
        self.notes_entry = ttk.Entry(self.journal_frame)
        
        # Journal Buttons
        self.save_trade_btn = ttk.Button(
            self.journal_frame,
            text="Save Trade",
            command=self.save_trade
        )
        
        self.view_journal_btn = ttk.Button(
            self.journal_frame,
            text="View Journal",
            command=self.view_journal
        )
        
        # Add/Remove Symbol buttons
        self.new_symbol_label = ttk.Label(self.root, text="Add New Symbol:")
        self.new_symbol_entry = ttk.Entry(self.root)
        self.add_symbol_btn = ttk.Button(
            self.root,
            text="Add",
            command=self.add_to_watchlist
        )
        self.remove_symbol_btn = ttk.Button(
            self.root,
            text="Remove Selected",
            command=self.remove_from_watchlist
        )
        
        # Result Display
        self.result_frame = ttk.LabelFrame(self.root, text="Results")
        self.position_size_label = ttk.Label(self.result_frame, text="Position Size: ")
        self.risk_amount_label = ttk.Label(self.result_frame, text="Risk Amount: ")
        self.margin_required_label = ttk.Label(self.result_frame, text="Margin Required: ")
        
        # Message Frame
        self.message_frame = ttk.LabelFrame(self.root, text="Messages")
        
        # Leverage suggestion
        self.leverage_suggestion = ttk.Label(
            self.message_frame,
            text="",
            style='Suggestion.TLabel'
        )
        
        # Safety Message
        self.safety_message = ttk.Label(
            self.message_frame, 
            text="Stay Safe And Don't Trade Without Stoploss!", 
            style='Safety.TLabel'
        )
        
        # New Watchlist Management
        self.watchlist_frame = ttk.LabelFrame(self.root, text="Watchlist Management")
        
        # Symbol selection
        self.symbol_label = ttk.Label(self.watchlist_frame, text="Symbol:")
        self.symbol_combo = ttk.Combobox(
            self.watchlist_frame,
            state="readonly"
        )
        
        # Add new symbol
        self.new_symbol_label = ttk.Label(self.watchlist_frame, text="Add New Symbol:")
        self.new_symbol_entry = ttk.Entry(self.watchlist_frame)
        self.add_symbol_btn = ttk.Button(
            self.watchlist_frame,
            text="Add to Watchlist",
            command=self.add_to_watchlist
        )
        
        # Remove symbol
        self.remove_symbol_btn = ttk.Button(
            self.watchlist_frame,
            text="Remove Selected",
            command=self.remove_from_watchlist
        )
        
        # Set default category
        self.update_symbol_list()
    
    def setup_layout(self):
        # Input fields grid
        inputs = [
            (self.risk_label, self.risk_entry, self.risk_warning),
            (self.capital_label, self.capital_entry, self.capital_warning),
            (self.stop_loss_label, self.stop_loss_entry, self.stop_loss_warning),
            (self.leverage_label, self.leverage_entry, self.leverage_warning)
        ]
        
        for row, (label, entry, warning) in enumerate(inputs):
            label.grid(row=row, column=0, sticky="e", padx=10, pady=5)
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            warning.grid(row=row, column=2, sticky="w", padx=5)
        
        # Calculate and Clear buttons
        self.calculate_btn.grid(row=4, column=1, sticky="e", padx=10, pady=10)
        self.clear_btn.grid(row=4, column=2, sticky="w", padx=10, pady=10)
        
        # Results Frame
        self.result_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        self.position_size_label.pack(anchor="w", padx=5, pady=2)
        self.risk_amount_label.pack(anchor="w", padx=5, pady=2)
        self.margin_required_label.pack(anchor="w", padx=5, pady=2)
        
        # Symbol Management
        self.new_symbol_label.grid(row=6, column=0, sticky="e", padx=5, pady=2)
        self.new_symbol_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=2)
        self.add_symbol_btn.grid(row=6, column=2, padx=5, pady=2)
        
        # Trade Journal Frame
        self.journal_frame.grid(row=7, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        # Symbol Selection
        self.symbol_label.grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.symbol_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.remove_symbol_btn.grid(row=0, column=2, padx=5, pady=2)
        
        # Update symbol list
        self.update_symbol_list()
        
        # Direction
        self.direction_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.long_radio.pack(side=tk.LEFT, padx=10)
        self.short_radio.pack(side=tk.LEFT, padx=10)
        
        # Entry Price
        self.entry_price_label.grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.entry_price_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        
        # Notes
        self.notes_label.grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.notes_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        
        # Journal Buttons
        self.save_trade_btn.grid(row=4, column=0, padx=5, pady=10)
        self.view_journal_btn.grid(row=4, column=1, padx=5, pady=10)
        
        # Watchlist Management Frame
        self.watchlist_frame.grid(row=8, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        # Message Frame
        self.message_frame.grid(row=9, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        # Leverage suggestion
        self.leverage_suggestion.pack(fill='x', padx=5, pady=2)
        
        # Separator between messages
        ttk.Separator(self.message_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Safety message
        self.safety_message.pack(fill='x', padx=5, pady=2)
        
        self.root.grid_columnconfigure(1, weight=1)
    
    def setup_validation(self):
        validation = {
            self.risk_entry: (0.01, 5, "Risk should be 0.01-5%"),
            self.capital_entry: (0.01, float('inf'), "Capital must be positive"),
            self.stop_loss_entry: (0.01, 4, "Stop loss must be 0.01-4%"),
            self.leverage_entry: (1, 10, "Leverage must be between 1-10x")
        }
        
        # Set default risk to 3%
        self.risk_entry.insert(0, "3")
        
        for entry, (min_val, max_val, warning_text) in validation.items():
            validate_cmd = (self.root.register(
                lambda val, min=min_val, max=max_val, text=warning_text, e=entry: 
                self.validate_entry(e, val, min, max, text)
            ), '%P')
            entry.configure(validate='focusout', validatecommand=validate_cmd)
        
        # Add trace to stop loss entry to suggest leverage
        self.stop_loss_var = tk.StringVar()
        self.stop_loss_entry.config(textvariable=self.stop_loss_var)
        self.stop_loss_var.trace_add('write', self.suggest_leverage)
        
        # Also trace changes to leverage entry to update suggestion message
        self.leverage_var = tk.StringVar()
        self.leverage_entry.config(textvariable=self.leverage_var)
        self.leverage_var.trace_add('write', self.check_leverage_against_suggestion)
    
    def suggest_leverage(self, *args):
        try:
            stop_loss = float(self.stop_loss_var.get())
            
            # Get suggested leverage based on stop loss
            if stop_loss <= 1:
                suggested = "10"
            elif 1 < stop_loss <= 2.5:
                suggested = "8"
            elif 2.5 < stop_loss <= 3:
                suggested = "6"
            elif 3 < stop_loss <= 4:
                suggested = "5"
            else:
                self.leverage_suggestion.config(text="")
                return
            
            # Update leverage entry and message
            current_leverage = self.leverage_entry.get().strip()
            
            # If current leverage is empty or different from suggestion, update it
            if not current_leverage or float(current_leverage) != float(suggested):
                self.leverage_entry.delete(0, tk.END)
                self.leverage_entry.insert(0, suggested)
            
            # Always update the suggestion message
            self.leverage_suggestion.config(
                text=f"Suggested Leverage For {stop_loss:.1f}% Stop Loss: {suggested}x"
            )
            
            # Clear any warning if the leverage is at suggested value
            if current_leverage == suggested:
                self.leverage_warning.config(text="")
                
        except ValueError:
            self.leverage_suggestion.config(text="")
    
    def validate_entry(self, entry, value, min_val, max_val, warning_text):
        try:
            if not value.strip():
                self.clear_warning(entry)
                return True
                
            val = float(value)
            if min_val <= val <= max_val:
                # Special validation for leverage based on stop loss
                if entry == self.leverage_entry:
                    try:
                        stop_loss = float(self.stop_loss_entry.get())
                        max_leverage = self.get_max_leverage(stop_loss)
                        if val > max_leverage:
                            self.show_warning(entry, f"Max leverage for {stop_loss:.1f}% stop loss is {max_leverage}x")
                            return False
                    except ValueError:
                        pass
                
                self.clear_warning(entry)
                return True
            else:
                self.show_warning(entry, warning_text)
                return False
        except ValueError:
            if value.strip():  # Only warn if there's actually input
                self.show_warning(entry, "Must be a number")
            return False
    
    def get_max_leverage(self, stop_loss):
        if stop_loss <= 1:
            return 10
        elif 1 < stop_loss <= 2.5:
            return 8
        elif 2.5 < stop_loss <= 3:
            return 6
        else:  # 3 < stop_loss <= 4
            return 5
    
    def show_warning(self, entry, text):
        if entry == self.risk_entry:
            self.risk_warning.config(text=text)
        elif entry == self.capital_entry:
            self.capital_warning.config(text=text)
        elif entry == self.stop_loss_entry:
            self.stop_loss_warning.config(text=text)
        elif entry == self.leverage_entry:
            self.leverage_warning.config(text=text)
    
    def clear_warning(self, entry):
        self.show_warning(entry, "")
    
    def validate_fields(self):
        required = [
            (self.risk_entry, "Risk percentage"),
            (self.capital_entry, "Capital amount"),
            (self.stop_loss_entry, "Stop loss percentage"),
            (self.leverage_entry, "Leverage")
        ]
        
        missing = []
        for entry, name in required:
            if not entry.get().strip():
                missing.append(name)
        
        if missing:
            messagebox.showwarning(
                "Missing Fields",
                f"Please fill in all required fields:\n{', '.join(missing)}"
            )
            return
        
        self.calculate_position()
    
    def calculate_position(self):
        try:
            capital = float(self.capital_entry.get())
            stop_loss_pct = float(self.stop_loss_entry.get()) / 100
            leverage = float(self.leverage_entry.get())
            risk_percent = float(self.risk_entry.get()) / 100

            # Core calculations
            risk_amount = risk_percent * capital
            position_size = risk_amount / (leverage * stop_loss_pct)
            margin_required = position_size / leverage
            
            # Display results
            self.position_size_label.config(
                text=f"Position Size: ${position_size:,.2f}"
            )
            
            self.risk_amount_label.config(
                text=f"Risk Amount: ${risk_amount:,.2f} ({risk_percent*100:.2f}% of capital)"
            )
            
            self.margin_required_label.config(
                text=f"Margin Required: ${margin_required:,.2f} ({(margin_required/capital*100):.1f}% of capital)"
            )
            
        except ValueError as e:
            messagebox.showerror("Calculation Error", f"Invalid input: {str(e)}")
    
    def clear_fields(self):
        # Clear all entries except risk which gets reset to 3%
        self.capital_entry.delete(0, tk.END)
        self.stop_loss_entry.delete(0, tk.END)
        self.leverage_entry.delete(0, tk.END)
        
        # Reset risk to 3%
        self.risk_entry.delete(0, tk.END)
        self.risk_entry.insert(0, "3")
        
        # Clear all warnings and messages
        for warning in [self.risk_warning, self.capital_warning,
                       self.stop_loss_warning, self.leverage_warning]:
            warning.config(text="")
        self.leverage_suggestion.config(text="")
        
        # Clear results
        self.position_size_label.config(text="Position Size: ")
        self.risk_amount_label.config(text="Risk Amount: ")
        self.margin_required_label.config(text="Margin Required: ")

    def check_leverage_against_suggestion(self, *args):
        try:
            stop_loss = float(self.stop_loss_entry.get())
            current_leverage = float(self.leverage_entry.get())
            
            # Get suggested leverage
            if stop_loss <= 1:
                suggested = 10
            elif 1 < stop_loss <= 2.5:
                suggested = 8
            elif 2.5 < stop_loss <= 3:
                suggested = 6
            elif 3 < stop_loss <= 4:
                suggested = 5
            else:
                return
            
            # Update message to show if current leverage differs from suggestion
            if current_leverage != suggested:
                self.leverage_suggestion.config(
                    text=f"Suggested Leverage For {stop_loss:.1f}% Stop Loss: {suggested}x (Current: {current_leverage:.0f}x)"
                )
            else:
                self.leverage_suggestion.config(
                    text=f"Suggested Leverage For {stop_loss:.1f}% Stop Loss: {suggested}x"
                )
                
        except ValueError:
            pass  # Ignore invalid values while typing

    def save_trade(self):
        try:
            # Get current values
            symbol = self.symbol_combo.get()
            if not symbol:
                messagebox.showerror("Error", "Please select a symbol")
                return
                
            direction = self.direction_var.get()
            entry_price = float(self.entry_price_entry.get() or 0)
            position_size = float(self.position_size_label.get().split('$')[1].replace(',', ''))
            stop_loss = float(self.stop_loss_entry.get())
            risk_amount = float(self.risk_amount_label.get().split('$')[1].split(' ')[0].replace(',', ''))
            leverage = float(self.leverage_entry.get())
            notes = self.notes_entry.get()
            
            # Create new trade entry
            new_trade = {
                'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Symbol': symbol,
                'Direction': direction,
                'Entry Price': entry_price,
                'Position Size': position_size,
                'Stop Loss': stop_loss,
                'Risk Amount': risk_amount,
                'Leverage': leverage,
                'Status': 'OPEN',
                'Exit Price': None,
                'Profit/Loss': None,
                'Notes': notes
            }
            
            # Read existing trades
            if os.path.exists(self.excel_file):
                df = pd.read_excel(self.excel_file)
            else:
                df = pd.DataFrame(columns=list(new_trade.keys()))
            
            # Append new trade
            df = pd.concat([df, pd.DataFrame([new_trade])], ignore_index=True)
            
            # Save to Excel
            df.to_excel(self.excel_file, index=False)
            
            messagebox.showinfo("Success", "Trade saved successfully!")
            
            # Clear journal fields
            self.entry_price_entry.delete(0, tk.END)
            self.notes_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save trade: {str(e)}")

    def view_journal(self):
        try:
            # Try to open the Excel file
            os.startfile(self.excel_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open trade journal: {str(e)}")

    def update_symbol_list(self):
        self.symbol_combo['values'] = sorted(self.symbols)
        if self.symbols:
            self.symbol_combo.set(self.symbols[0])

    def add_to_watchlist(self):
        new_symbol = self.new_symbol_entry.get().strip().upper()
        
        if not new_symbol:
            messagebox.showerror("Error", "Please enter a symbol")
            return
            
        if new_symbol not in self.symbols:
            self.symbols.append(new_symbol)
            self.symbols.sort()
            self.save_watchlist()
            self.update_symbol_list()
            self.new_symbol_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added {new_symbol}")
        else:
            messagebox.showinfo("Info", f"{new_symbol} already in watchlist")

    def remove_from_watchlist(self):
        symbol = self.symbol_combo.get()
        
        if not symbol:
            messagebox.showerror("Error", "Please select a symbol to remove")
            return
            
        if symbol in self.symbols:
            self.symbols.remove(symbol)
            self.save_watchlist()
            self.update_symbol_list()
            messagebox.showinfo("Success", f"Removed {symbol}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PositionSizeCalculator(root)
    root.mainloop()