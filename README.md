# Credit Card Number Generator


A simple Python script to generate valid credit card numbers from a given 6-digit Bank Identification Number (BIN). This tool also generates a corresponding CVV and a future expiration date. The generated card numbers are valid according to the Luhn algorithm.

## Prerequisites

- Python 3

## How to Use

1.  Clone the repository or download the `cc.py` file.
2.  Navigate to the directory and run the script from your terminal:
    ```bash
    python3 cc.py
    ```
3.  When prompted, enter a valid 6-digit BIN. The script will then output the generated card details.

### Example

```bash
# Run the script
python3 cc.py

# Enter a BIN when prompted
bin(6 numbers):453910

# The script will output the generated details
card:4539105820428104
cvv079
month:09
year:24
```

## ⚠️ Disclaimer

This tool is intended for educational and testing purposes only, such as validating payment forms. The generated numbers are mathematically valid according to the Luhn algorithm but are not real, active credit card numbers. Attempting to use these numbers for fraudulent transactions is illegal. The author is not responsible for any misuse of this script.
