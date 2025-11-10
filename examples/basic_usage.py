"""
Basic Usage Example for Hybrid Cryptographic System
Demonstrates encryption and decryption of a document.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto_system import HybridCrypto


def main():
    print("=" * 60)
    print("Hybrid Cryptographic System - Basic Usage Example")
    print("=" * 60)
    
    # Initialize the crypto system
    crypto = HybridCrypto()
    
    # Step 1: Generate RSA key pair
    print("\n[Step 1] Generating RSA key pair...")
    keys = crypto.generate_keys(output_dir="example_keys")
    
    # Step 2: Create a sample document
    print("\n[Step 2] Creating sample document...")
    sample_file = "test_documents/sample_document.txt"
    os.makedirs("test_documents", exist_ok=True)
    
    with open(sample_file, 'w') as f:
        f.write("This is a confidential document.\n")
        f.write("It contains sensitive information that needs to be encrypted.\n")
        f.write("Using hybrid cryptography with AES-256, RSA-2048, and QR codes.\n")
        f.write("\n")
        f.write("Security Features:\n")
        f.write("- AES-256 for fast document encryption\n")
        f.write("- RSA-2048 for secure key exchange\n")
        f.write("- QR codes for visual encoding\n")
    
    print(f"✓ Sample document created: {sample_file}")
    
    # Step 3: Encrypt the document
    print("\n[Step 3] Encrypting document...")
    encrypted_result = crypto.encrypt_document(
        input_file=sample_file,
        output_dir="encrypted_output",
        public_key_path=keys["public_key"],
        generate_qr=True
    )
    
    # Step 4: Decrypt the document
    print("\n[Step 4] Decrypting document...")
    decrypted_file = "test_documents/decrypted_document.txt"
    crypto.decrypt_document(
        encrypted_dir="encrypted_output",
        output_file=decrypted_file,
        private_key_path=keys["private_key"]
    )
    
    # Step 5: Verify the decryption
    print("\n[Step 5] Verifying decryption...")
    with open(sample_file, 'r') as f:
        original_content = f.read()
    
    with open(decrypted_file, 'r') as f:
        decrypted_content = f.read()
    
    if original_content == decrypted_content:
        print("✓ SUCCESS: Decrypted content matches original!")
    else:
        print("✗ ERROR: Decrypted content does not match original!")
    
    # Step 6: Test QR code decryption
    print("\n[Step 6] Testing decryption from QR codes...")
    decrypted_from_qr = "test_documents/decrypted_from_qr.txt"
    crypto.decrypt_document(
        encrypted_dir="encrypted_output",
        output_file=decrypted_from_qr,
        private_key_path=keys["private_key"],
        use_qr=True
    )
    
    with open(decrypted_from_qr, 'r') as f:
        qr_decrypted_content = f.read()
    
    if original_content == qr_decrypted_content:
        print("✓ SUCCESS: QR code decryption works correctly!")
    else:
        print("✗ ERROR: QR code decryption failed!")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  Keys: example_keys/")
    print(f"  Encrypted: encrypted_output/")
    print(f"  QR Codes: encrypted_output/qr_codes/")
    print(f"  Decrypted: {decrypted_file}")


if __name__ == "__main__":
    main()
