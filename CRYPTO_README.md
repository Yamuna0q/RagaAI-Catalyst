# Hybrid Cryptographic System

A secure document encryption and decryption system that combines **AES-256**, **RSA-2048**, and **QR code encoding** for maximum security and convenience.

## 🔐 Features

- **AES-256 Encryption**: Fast symmetric encryption for documents of any size
- **RSA-2048 Key Exchange**: Secure asymmetric encryption for AES keys
- **QR Code Encoding**: Visual encoding of encrypted data for easy sharing
- **Hybrid Approach**: Combines the best of symmetric and asymmetric cryptography
- **CLI Interface**: Easy-to-use command-line tools
- **Python API**: Programmatic access for integration into applications

## 🏗️ Architecture

### How It Works

1. **Encryption Process**:
   - Generate a random AES-256 key
   - Encrypt the document with AES (fast, efficient)
   - Encrypt the AES key with RSA public key (secure)
   - Optionally encode encrypted data in QR codes

2. **Decryption Process**:
   - Decrypt the AES key using RSA private key
   - Decrypt the document using the AES key
   - Can read from binary files or QR codes

### Why Hybrid Cryptography?

- **AES**: Fast encryption for large documents
- **RSA**: Secure key exchange without pre-shared secrets
- **QR Codes**: Easy visual transmission and storage

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Install Dependencies

```bash
pip install cryptography qrcode pillow pyzbar opencv-python
```

Or install from requirements file:

```bash
pip install -r crypto_requirements.txt
```

### System Dependencies (for QR code decoding)

**Ubuntu/Debian:**
```bash
sudo apt-get install libzbar0
```

**macOS:**
```bash
brew install zbar
```

**Amazon Linux 2023:**
```bash
sudo dnf install zbar
```

## 🚀 Quick Start

### 1. Generate RSA Key Pair

```bash
python -m crypto_system.cli generate-keys --output keys/
```

This creates:
- `keys/private_key.pem` - Keep this secret!
- `keys/public_key.pem` - Share this with others

### 2. Encrypt a Document

```bash
python -m crypto_system.cli encrypt \
  --input document.pdf \
  --output encrypted/ \
  --public-key keys/public_key.pem
```

This creates:
- `encrypted/encrypted_document.bin` - Encrypted document
- `encrypted/encrypted_key.bin` - Encrypted AES key
- `encrypted/iv.bin` - Initialization vector
- `encrypted/metadata.json` - Encryption metadata
- `encrypted/qr_codes/` - QR codes for all components

### 3. Decrypt a Document

```bash
python -m crypto_system.cli decrypt \
  --input encrypted/ \
  --output decrypted.pdf \
  --private-key keys/private_key.pem
```

### 4. Encrypt with QR Codes Only (Small Files)

```bash
python -m crypto_system.cli encrypt-qr \
  --input message.txt \
  --output qr_codes/ \
  --public-key keys/public_key.pem
```

### 5. Decrypt from QR Codes

```bash
python -m crypto_system.cli decrypt-qr \
  --qr-codes qr_codes/*.png \
  --output message.txt \
  --private-key keys/private_key.pem
```

## 💻 Python API Usage

### Basic Encryption/Decryption

```python
from crypto_system import HybridCrypto

# Initialize
crypto = HybridCrypto()

# Generate keys
keys = crypto.generate_keys(output_dir="keys")

# Encrypt document
result = crypto.encrypt_document(
    input_file="document.pdf",
    output_dir="encrypted",
    public_key_path="keys/public_key.pem",
    generate_qr=True
)

# Decrypt document
crypto.decrypt_document(
    encrypted_dir="encrypted",
    output_file="decrypted.pdf",
    private_key_path="keys/private_key.pem"
)
```

### QR Code Only Mode

```python
from crypto_system import HybridCrypto
import glob

crypto = HybridCrypto()

# Encrypt to QR codes
qr_result = crypto.encrypt_with_qr_only(
    input_file="message.txt",
    output_dir="qr_codes",
    public_key_path="keys/public_key.pem"
)

# Decrypt from QR codes
qr_files = sorted(glob.glob("qr_codes/*.png"))
crypto.decrypt_from_qr_only(
    qr_images=qr_files,
    output_file="decrypted_message.txt",
    private_key_path="keys/private_key.pem"
)
```

### Individual Components

```python
from crypto_system import AESHandler, RSAHandler, QRHandler

# AES encryption
aes = AESHandler()
key = aes.generate_key()
ciphertext, iv = aes.encrypt(b"Secret data", key)
plaintext = aes.decrypt(ciphertext, key, iv)

# RSA encryption
rsa = RSAHandler()
private_key, public_key = rsa.generate_key_pair()
encrypted = rsa.encrypt(b"Secret key", public_key)
decrypted = rsa.decrypt(encrypted, private_key)

# QR code generation
qr = QRHandler()
qr.generate_qr("Hello, World!", "qr_code.png")
data = qr.decode_qr("qr_code.png")
```

## 📚 Examples

Run the example scripts to see the system in action:

### Basic Usage Example

```bash
python examples/basic_usage.py
```

This demonstrates:
- Key generation
- Document encryption
- Document decryption
- QR code generation and decoding
- Verification of decrypted content

### QR Code Only Example

```bash
python examples/qr_only_example.py
```

This demonstrates:
- Encrypting small messages to QR codes
- Sharing encrypted data via QR codes
- Decrypting from QR codes

## 🔒 Security Features

### Encryption Algorithms

- **AES-256-CBC**: Industry-standard symmetric encryption
- **RSA-2048-OAEP**: Secure asymmetric encryption with OAEP padding
- **SHA-256**: Cryptographic hashing for OAEP

### Security Best Practices

1. **Key Management**:
   - Keep private keys secure and never share them
   - Use strong passwords to encrypt private keys
   - Regularly rotate keys for long-term security

2. **Random Number Generation**:
   - Uses `os.urandom()` for cryptographically secure randomness
   - Each encryption uses a unique IV (Initialization Vector)

3. **Padding**:
   - PKCS7 padding for AES
   - OAEP padding for RSA

4. **Error Correction**:
   - QR codes use high error correction (Level H)
   - Can recover from up to 30% damage

## 📁 Project Structure

```
crypto_system/
├── __init__.py           # Package initialization
├── __main__.py           # Module entry point
├── aes_handler.py        # AES encryption/decryption
├── rsa_handler.py        # RSA key generation and encryption
├── qr_handler.py         # QR code generation and decoding
├── hybrid_crypto.py      # Main hybrid system
└── cli.py                # Command-line interface

examples/
├── basic_usage.py        # Basic encryption/decryption example
└── qr_only_example.py    # QR code only example
```

## 🛠️ CLI Commands Reference

### generate-keys

Generate RSA key pair.

```bash
python -m crypto_system.cli generate-keys [OPTIONS]

Options:
  --output, -o PATH      Output directory (default: keys/)
  --password, -p TEXT    Password to encrypt private key
```

### encrypt

Encrypt a document.

```bash
python -m crypto_system.cli encrypt [OPTIONS]

Options:
  --input, -i PATH       Input file to encrypt (required)
  --output, -o PATH      Output directory (required)
  --public-key, -k PATH  RSA public key path (required)
  --no-qr                Don't generate QR codes
```

### decrypt

Decrypt a document.

```bash
python -m crypto_system.cli decrypt [OPTIONS]

Options:
  --input, -i PATH       Encrypted files directory (required)
  --output, -o PATH      Output file path (required)
  --private-key, -k PATH RSA private key path (required)
  --password, -p TEXT    Private key password
  --use-qr               Read from QR codes instead of binary files
```

### encrypt-qr

Encrypt and encode in QR codes only.

```bash
python -m crypto_system.cli encrypt-qr [OPTIONS]

Options:
  --input, -i PATH       Input file to encrypt (required)
  --output, -o PATH      Output directory for QR codes (required)
  --public-key, -k PATH  RSA public key path (required)
```

### decrypt-qr

Decrypt from QR codes only.

```bash
python -m crypto_system.cli decrypt-qr [OPTIONS]

Options:
  --qr-codes, -q PATH [PATH ...]  QR code image files (required)
  --output, -o PATH               Output file path (required)
  --private-key, -k PATH          RSA private key path (required)
  --password, -p TEXT             Private key password
```

## 🎯 Use Cases

1. **Secure Document Sharing**:
   - Encrypt sensitive documents before sending via email
   - Share QR codes for small messages

2. **Data Archival**:
   - Encrypt documents for long-term storage
   - Print QR codes for physical backup

3. **Secure Communication**:
   - Exchange encrypted messages via QR codes
   - No need for secure channel to share keys

4. **Compliance**:
   - Meet data protection requirements
   - Audit trail via metadata files

## ⚠️ Limitations

- **QR Code Size**: Large files may require multiple QR codes
- **RSA Encryption**: Can only encrypt small data (max ~190 bytes for RSA-2048)
- **QR Decoding**: Requires good image quality for reliable decoding

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for educational and commercial use.

## 🔗 Dependencies

- `cryptography` - Cryptographic primitives
- `qrcode` - QR code generation
- `pillow` - Image processing
- `pyzbar` - QR code decoding
- `opencv-python` - Image reading for QR decoding

## 📞 Support

For issues, questions, or suggestions, please open an issue on the project repository.

## 🎓 Learn More

- [AES Encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [RSA Cryptography](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [QR Codes](https://en.wikipedia.org/wiki/QR_code)
- [Hybrid Cryptography](https://en.wikipedia.org/wiki/Hybrid_cryptosystem)

---

**Made with 🔐 for secure communications**
