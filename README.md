# Forex Lot Size Calculator

This is a Python-based Forex Lot Size Calculator application built using the `tkinter` library for the graphical user interface (GUI) and `matplotlib` for visualizing the results. The tool helps traders calculate the recommended lot size for their trades based on their capital, risk tolerance, stop-loss distance, and the selected financial instrument.

## Features

- **Instrument Selection**: Choose from a list of financial instruments (e.g., EURUSD, GBPUSD, XAUUSD, NQ) to automatically set the pip value.
- **Risk Management**:
  - Set risk as a percentage of your capital or as a fixed amount.
  - Input stop-loss distance in pips.
- **Automatic Pip Value**: The pip value is automatically determined based on the selected instrument.
- **Graphical Visualization**: A bar chart displays the capital, risk amount, and recommended lot size.
- **Save/Load Parameters**: Save your trading parameters to a file and load them later for quick calculations.
- **User-Friendly Interface**: Simple and intuitive GUI for easy input and calculation.

## Supported Instruments

The following financial instruments are supported, along with their pip values (for 1 standard lot):

| Instrument | Pip Value (USD) |
|------------|-----------------|
| EURUSD     | 10              |
| GBPUSD     | 10              |
| USDJPY     | 9.09            |
| XAUUSD     | 1               |
| NQ         | 20              |

## How to Use

1. **Select Instrument**: Choose the financial instrument you are trading from the dropdown menu.
2. **Enter Capital**: Input your available capital in USD.
3. **Set Risk**:
   - Choose whether to set risk as a percentage of your capital or as a fixed amount.
   - Enter the risk value (e.g., 2% or $100).
4. **Set Stop-Loss**: Enter the stop-loss distance in pips.
5. **Calculate**: Click the "Calculer la Taille du Lot" button to calculate the recommended lot size.
6. **View Results**: The recommended lot size, risk amount, and other details will be displayed. A bar chart will also show a summary of the calculation.
7. **Save/Load Parameters**: Use the "Sauvegarder les paramètres" button to save your inputs to a file, or use "Charger les paramètres" to load previously saved parameters.

## Requirements

- Python 3.x
- Libraries:
  - `tkinter` (included with Python)
  - `matplotlib` (install with `pip install matplotlib`)

## Installation

1. Clone this repository or download the `calcule.py` file.
2. Install the required libraries:
   ```bash
   pip install matplotlib