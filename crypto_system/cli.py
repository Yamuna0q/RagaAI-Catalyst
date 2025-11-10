"""
Command Line Interface for Hybrid Cryptographic System
"""

import argparse
import sys
import os
from .hybrid_crypto import HybridCrypto


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Hybrid Cryptographic System - Secure document encryption using AES, RSA, and QR codes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate RSA key pair
  python -m crypto_system.cli generate-keys --output keys/
  
  # Encrypt a document
  python -m crypto_system.cli encrypt --input document.pdf --output encrypted/ --public-key keys/public_key.pem
  
  # Decrypt a document
  python -m crypto_system.cli decrypt --input encrypted/ --output decrypted.pdf --private-key keys/private_key.pem
  
  # Encrypt with QR codes only (for small files)
  python -m crypto_system.cli encrypt-qr --input message.txt --output qr_codes/ --public-key keys/public_key.pem
  
  # Decrypt from QR codes
  python -m crypto_system.cli decrypt-qr --qr-codes qr_codes/*.png --output message.txt --private-key keys/private_key.pem
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate keys command
    gen_parser = subparsers.add_parser('generate-keys', help='Generate RSA key pair')
    gen_parser.add_argument(
        '--output', '-o',
        default='keys',
        help='Output directory for keys (default: keys/)'
    )
    gen_parser.add_argument(
        '--password', '-p',
        help='Password to encrypt private key (optional)'
    )
    
    # Encrypt command
    enc_parser = subparsers.add_parser('encrypt', help='Encrypt a document')
    enc_parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file to encrypt'
    )
    enc_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for encrypted files'
    )
    enc_parser.add_argument(
        '--public-key', '-k',
        required=True,
        help='Path to RSA public key'
    )
    enc_parser.add_argument(
        '--no-qr',
        action='store_true',
        help='Do not generate QR codes'
    )
    
    # Decrypt command
    dec_parser = subparsers.add_parser('decrypt', help='Decrypt a document')
    dec_parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input directory containing encrypted files'
    )
    dec_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output file path for decrypted document'
    )
    dec_parser.add_argument(
        '--private-key', '-k',
        required=True,
        help='Path to RSA private key'
    )
    dec_parser.add_argument(
        '--password', '-p',
        help='Password for private key (if encrypted)'
    )
    dec_parser.add_argument(
        '--use-qr',
        action='store_true',
        help='Read encrypted data from QR codes'
    )
    
    # Encrypt with QR only command
    enc_qr_parser = subparsers.add_parser('encrypt-qr', help='Encrypt and encode in QR codes only')
    enc_qr_parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file to encrypt'
    )
    enc_qr_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for QR codes'
    )
    enc_qr_parser.add_argument(
        '--public-key', '-k',
        required=True,
        help='Path to RSA public key'
    )
    
    # Decrypt from QR only command
    dec_qr_parser = subparsers.add_parser('decrypt-qr', help='Decrypt from QR codes only')
    dec_qr_parser.add_argument(
        '--qr-codes', '-q',
        required=True,
        nargs='+',
        help='QR code image files (space-separated)'
    )
    dec_qr_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output file path for decrypted document'
    )
    dec_qr_parser.add_argument(
        '--private-key', '-k',
        required=True,
        help='Path to RSA private key'
    )
    dec_qr_parser.add_argument(
        '--password', '-p',
        help='Password for private key (if encrypted)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize crypto system
    crypto = HybridCrypto()
    
    try:
        if args.command == 'generate-keys':
            password = args.password.encode() if args.password else None
            crypto.generate_keys(args.output, password)
            
        elif args.command == 'encrypt':
            if not os.path.exists(args.input):
                print(f"Error: Input file '{args.input}' not found")
                sys.exit(1)
            if not os.path.exists(args.public_key):
                print(f"Error: Public key '{args.public_key}' not found")
                sys.exit(1)
            
            crypto.encrypt_document(
                args.input,
                args.output,
                args.public_key,
                generate_qr=not args.no_qr
            )
            
        elif args.command == 'decrypt':
            if not os.path.exists(args.input):
                print(f"Error: Input directory '{args.input}' not found")
                sys.exit(1)
            if not os.path.exists(args.private_key):
                print(f"Error: Private key '{args.private_key}' not found")
                sys.exit(1)
            
            password = args.password.encode() if args.password else None
            crypto.decrypt_document(
                args.input,
                args.output,
                args.private_key,
                password,
                use_qr=args.use_qr
            )
            
        elif args.command == 'encrypt-qr':
            if not os.path.exists(args.input):
                print(f"Error: Input file '{args.input}' not found")
                sys.exit(1)
            if not os.path.exists(args.public_key):
                print(f"Error: Public key '{args.public_key}' not found")
                sys.exit(1)
            
            crypto.encrypt_with_qr_only(
                args.input,
                args.output,
                args.public_key
            )
            
        elif args.command == 'decrypt-qr':
            for qr_file in args.qr_codes:
                if not os.path.exists(qr_file):
                    print(f"Error: QR code file '{qr_file}' not found")
                    sys.exit(1)
            if not os.path.exists(args.private_key):
                print(f"Error: Private key '{args.private_key}' not found")
                sys.exit(1)
            
            password = args.password.encode() if args.password else None
            crypto.decrypt_from_qr_only(
                args.qr_codes,
                args.output,
                args.private_key,
                password
            )
        
        print("\n✓ Operation completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
