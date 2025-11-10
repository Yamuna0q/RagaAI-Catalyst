"""
QR Code Only Example
Demonstrates encryption and decryption using only QR codes.
Useful for small documents or messages.
"""

import os
import sys
import glob

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto_system import HybridCrypto


def main():
    print("=" * 60)
    print("Hybrid Cryptographic System - QR Code Only Example")
    print("=" * 60)
    
    # Initialize the crypto system
    crypto = HybridCrypto()
    
    # Step 1: Generate RSA key pair (reuse if exists)
    print("\n[Step 1] Setting up RSA keys...")
    if not os.path.exists("example_keys/private_key.pem"):
        keys = crypto.generate_keys(output_dir="example_keys")
    else:
        print("✓ Using existing keys from example_keys/")
        keys = {
            "private_key": "example_keys/private_key.pem",
            "public_key": "example_keys/public_key.pem"
        }
    
    # Step 2: Create a small message
    print("\n[Step 2] Creating secret message...")
    message_file = "test_documents/secret_message.txt"
    os.makedirs("test_documents", exist_ok=True)
    
    with open(message_file, 'w') as f:
        f.write("TOP SECRET MESSAGE\n")
        f.write("=" * 40 + "\n\n")
        f.write("Meeting Location: Warehouse 7\n")
        f.write("Time: 23:00 hours\n")
        f.write("Code Word: Phoenix Rising\n")
        f.write("\nThis message will self-destruct... just kidding!\n")
        f.write("But it is encrypted in QR codes for secure transmission.\n")
    
    print(f"✓ Secret message created: {message_file}")
    
    # Step 3: Encrypt and encode in QR codes
    print("\n[Step 3] Encrypting message and generating QR codes...")
    qr_result = crypto.encrypt_with_qr_only(
        input_file=message_file,
        output_dir="qr_only_output",
        public_key_path=keys["public_key"]
    )
    
    print(f"\n✓ Message encrypted and encoded in {qr_result['count']} QR code(s)")
    print("  You can now share these QR codes securely!")
    
    # Step 4: Decrypt from QR codes
    print("\n[Step 4] Decrypting message from QR codes...")
    
    # Get all QR code files
    qr_files = sorted(glob.glob("qr_only_output/*.png"))
    
    decrypted_file = "test_documents/decrypted_secret_message.txt"
    crypto.decrypt_from_qr_only(
        qr_images=qr_files,
        output_file=decrypted_file,
        private_key_path=keys["private_key"]
    )
    
    # Step 5: Verify the decryption
    print("\n[Step 5] Verifying decryption...")
    with open(message_file, 'r') as f:
        original_content = f.read()
    
    with open(decrypted_file, 'r') as f:
        decrypted_content = f.read()
    
    if original_content == decrypted_content:
        print("✓ SUCCESS: Message decrypted correctly from QR codes!")
        print("\nDecrypted message:")
        print("-" * 60)
        print(decrypted_content)
        print("-" * 60)
    else:
        print("✗ ERROR: Decrypted content does not match original!")
    
    print("\n" + "=" * 60)
    print("QR Code Example completed successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print(f"  QR Codes: qr_only_output/")
    print(f"  Decrypted: {decrypted_file}")
    print("\nUse Case:")
    print("  - Share QR codes via email, messaging apps, or print them")
    print("  - Recipient scans QR codes and decrypts with their private key")
    print("  - Perfect for secure message transmission!")


if __name__ == "__main__":
    main()
