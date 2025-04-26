# EVM Vanity Generator

A simple Flask app to generate vanity Ethereum-compatible wallets (for ApeChain or other EVM networks) by brute-forcing addresses with a specified hex prefix.

## Features

- Enter a hex prefix (e.g., `cafe`) to generate an address starting with that prefix.
- Returns the generated address and the private key.

## Requirements

- Python 3.8+
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the app:
   ```bash
   python app.py
   ```
2. Open your browser at `http://localhost:5000`.
3. Enter a hex prefix (without `0x`) and click `Generate`.
4. Wait for your vanity address to appear.

## Notes

- Brute-forcing can take a long time for longer prefixes.
- Do not share your private key.

## License

MIT
