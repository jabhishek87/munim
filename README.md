# 🦉 Munim (मुनीम)

<img src="assets/munim.jpg" width="200"
alt="Munim (मुनीम) Mascot: A wise owl wearing spectacles and a pagdi, sitting at a desk and organizing financial data from paper to a digital screen." style="max-width: 500px; border-radius: 12px;"/>

A bank statement parser and expense categorizer for Indian banks.

## 🦉 Description

Munim is a tool designed to parse bank statements from various Indian financial institutions and automatically categorize expenses for better financial management.

## ✨ Key Features

- Support for multiple Indian banks
- Automatic expense categorization
- Statement parsing and data extraction
- YAML-based configuration for expense mapping

## 🛠️ Installation

Clone the repository and install dependencies:

```bash
git clone git@github.com:jabhishek87/munim.git
cd munim
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## 🚀 Quick Usage

### CLI Commands

```bash
# Parse statements for a specific bank
munim parse hdfc --verbose

# Parse statements for all supported banks
munim parse_all --verbose

# View help
munim --help
munim parse --help
```

### Options

- `--verbose, -v`: Enable verbose output with stderr logging
- `--log-file`: Specify custom log file path (default: munim.log)

### Python API

```python
from parser import HDFCParser

parser = HDFCParser()
transactions = parser.parse('statement.csv')
```

## 🏦 Supported Banks

| Bank | Parser | Status |
|------|--------|--------|
| HDFC | HDFCParser | ✅ |
| ICICI | ICICIParser | ✅ |
| SBI | SBIParser | ✅ |
| Axis | AxisParser | ✅ |
| HDFC Credit Card | CCHDFCParser | ✅ |
| ICICI Credit Card | CCICICIParser | ✅ |

## 📜 License

Distributed under the MIT License.

## 📞 Contact