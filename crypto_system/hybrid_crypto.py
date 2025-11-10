"""
Hybrid Cryptographic System
Combines AES, RSA, and QR code encoding for secure document encryption.
"""

import os
import json
import base64
from typing import Optional
from .aes_handler import AESHandler
from .rsa_handler import RSAHandler
from .qr_handler import QRHandler


class HybridCrypto:
    """
    Hybrid cryptographic system that combines:
    - AES-256 for fast document encryption
    - RSA-2048 for secure key exchange
    - QR codes for visual encoding of encrypted data
    """
    
    def __init__(self):
        """Initialize all crypto handlers."""
        self.aes = AESHandler()
        self.rsa = RSAHandler()
        self.qr = QRHandler()
    
    def generate_keys(self, output_dir: str = "keys", password: Optional[bytes] = None) -> dict:
        """
        Generate RSA key pair and save to files.
        
        Args:
            output_dir: Directory to save keys
            password: Optional password to encrypt private key
            
        Returns:
            dict: Paths to generated key files
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate RSA key pair
        private_key, public_key = self.rsa.generate_key_pair()
        
        # Save keys
        private_key_path = os.path.join(output_dir, "private_key.pem")
        public_key_path = os.path.join(output_dir, "public_key.pem")
        
        self.rsa.save_private_key(private_key, private_key_path, password)
        self.rsa.save_public_key(public_key, public_key_path)
        
        print(f"✓ RSA key pair generated successfully!")
        print(f"  Private key: {private_key_path}")
        print(f"  Public key: {public_key_path}")
        
        return {
            "private_key": private_key_path,
            "public_key": public_key_path
        }
    
    def encrypt_document(
        self,
        input_file: str,
        output_dir: str,
        public_key_path: str,
        generate_qr: bool = True
    ) -> dict:
        """
        Encrypt a document using hybrid cryptography.
        
        Process:
        1. Generate random AES key
        2. Encrypt document with AES
        3. Encrypt AES key with RSA public key
        4. Optionally generate QR codes for encrypted data
        
        Args:
            input_file: Path to document to encrypt
            output_dir: Directory to save encrypted files
            public_key_path: Path to RSA public key
            generate_qr: Whether to generate QR codes
            
        Returns:
            dict: Paths to generated files and metadata
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load RSA public key
        public_key = self.rsa.load_public_key(public_key_path)
        
        # Generate AES key
        aes_key = self.aes.generate_key()
        
        # Encrypt document with AES
        encrypted_file = os.path.join(output_dir, "encrypted_document.bin")
        iv = self.aes.encrypt_file(input_file, encrypted_file, aes_key)
        
        # Encrypt AES key with RSA
        encrypted_aes_key = self.rsa.encrypt(aes_key, public_key)
        
        # Save encrypted AES key and IV
        key_file = os.path.join(output_dir, "encrypted_key.bin")
        with open(key_file, 'wb') as f:
            f.write(encrypted_aes_key)
        
        iv_file = os.path.join(output_dir, "iv.bin")
        with open(iv_file, 'wb') as f:
            f.write(iv)
        
        # Create metadata
        metadata = {
            "original_filename": os.path.basename(input_file),
            "encrypted_file": "encrypted_document.bin",
            "encrypted_key_file": "encrypted_key.bin",
            "iv_file": "iv.bin",
            "encryption_method": "AES-256-CBC + RSA-2048"
        }
        
        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        result = {
            "encrypted_document": encrypted_file,
            "encrypted_key": key_file,
            "iv": iv_file,
            "metadata": metadata_file
        }
        
        # Generate QR codes if requested
        if generate_qr:
            qr_dir = os.path.join(output_dir, "qr_codes")
            if not os.path.exists(qr_dir):
                os.makedirs(qr_dir)
            
            # QR code for encrypted key
            key_qr = os.path.join(qr_dir, "encrypted_key_qr.png")
            self.qr.encode_binary_to_qr(encrypted_aes_key, key_qr)
            
            # QR code for IV
            iv_qr = os.path.join(qr_dir, "iv_qr.png")
            self.qr.encode_binary_to_qr(iv, iv_qr)
            
            # QR code for metadata
            metadata_qr = os.path.join(qr_dir, "metadata_qr.png")
            self.qr.encode_dict_to_qr(metadata, metadata_qr)
            
            result["qr_codes"] = {
                "encrypted_key": key_qr,
                "iv": iv_qr,
                "metadata": metadata_qr
            }
            
            print(f"✓ QR codes generated in: {qr_dir}")
        
        print(f"✓ Document encrypted successfully!")
        print(f"  Encrypted document: {encrypted_file}")
        print(f"  Encrypted key: {key_file}")
        print(f"  IV: {iv_file}")
        print(f"  Metadata: {metadata_file}")
        
        return result
    
    def decrypt_document(
        self,
        encrypted_dir: str,
        output_file: str,
        private_key_path: str,
        password: Optional[bytes] = None,
        use_qr: bool = False
    ) -> str:
        """
        Decrypt a document using hybrid cryptography.
        
        Process:
        1. Load encrypted AES key and IV
        2. Decrypt AES key with RSA private key
        3. Decrypt document with AES key
        
        Args:
            encrypted_dir: Directory containing encrypted files
            output_file: Path to save decrypted document
            private_key_path: Path to RSA private key
            password: Optional password for private key
            use_qr: Whether to read from QR codes instead of binary files
            
        Returns:
            str: Path to decrypted file
        """
        # Load RSA private key
        private_key = self.rsa.load_private_key(private_key_path, password)
        
        if use_qr:
            # Read from QR codes
            qr_dir = os.path.join(encrypted_dir, "qr_codes")
            
            # Decode encrypted key from QR
            key_qr = os.path.join(qr_dir, "encrypted_key_qr.png")
            encrypted_aes_key = self.qr.decode_qr_to_binary(key_qr)
            
            # Decode IV from QR
            iv_qr = os.path.join(qr_dir, "iv_qr.png")
            iv = self.qr.decode_qr_to_binary(iv_qr)
        else:
            # Read from binary files
            key_file = os.path.join(encrypted_dir, "encrypted_key.bin")
            with open(key_file, 'rb') as f:
                encrypted_aes_key = f.read()
            
            iv_file = os.path.join(encrypted_dir, "iv.bin")
            with open(iv_file, 'rb') as f:
                iv = f.read()
        
        # Decrypt AES key with RSA
        aes_key = self.rsa.decrypt(encrypted_aes_key, private_key)
        
        # Decrypt document with AES
        encrypted_file = os.path.join(encrypted_dir, "encrypted_document.bin")
        self.aes.decrypt_file(encrypted_file, output_file, aes_key, iv)
        
        print(f"✓ Document decrypted successfully!")
        print(f"  Decrypted file: {output_file}")
        
        return output_file
    
    def encrypt_with_qr_only(
        self,
        input_file: str,
        output_dir: str,
        public_key_path: str,
        max_qr_size: int = 2000
    ) -> dict:
        """
        Encrypt document and encode everything in QR codes.
        Useful for small documents that can fit in QR codes.
        
        Args:
            input_file: Path to document to encrypt
            output_dir: Directory to save QR codes
            public_key_path: Path to RSA public key
            max_qr_size: Maximum data size per QR code
            
        Returns:
            dict: Paths to generated QR codes
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load RSA public key
        public_key = self.rsa.load_public_key(public_key_path)
        
        # Read document
        with open(input_file, 'rb') as f:
            document_data = f.read()
        
        # Generate AES key and encrypt
        aes_key = self.aes.generate_key()
        encrypted_data, iv = self.aes.encrypt(document_data, aes_key)
        
        # Encrypt AES key with RSA
        encrypted_aes_key = self.rsa.encrypt(aes_key, public_key)
        
        # Encode to base64 for QR
        encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        encrypted_key_b64 = base64.b64encode(encrypted_aes_key).decode('utf-8')
        iv_b64 = base64.b64encode(iv).decode('utf-8')
        
        # Create package
        package = {
            "filename": os.path.basename(input_file),
            "encrypted_data": encrypted_data_b64,
            "encrypted_key": encrypted_key_b64,
            "iv": iv_b64
        }
        
        package_json = json.dumps(package)
        
        # Generate QR codes
        qr_paths = self.qr.encode_large_data_to_qr(
            package_json,
            output_dir,
            prefix="encrypted_package"
        )
        
        print(f"✓ Document encrypted and encoded in {len(qr_paths)} QR code(s)")
        print(f"  QR codes saved in: {output_dir}")
        
        return {"qr_codes": qr_paths, "count": len(qr_paths)}
    
    def decrypt_from_qr_only(
        self,
        qr_images: list,
        output_file: str,
        private_key_path: str,
        password: Optional[bytes] = None
    ) -> str:
        """
        Decrypt document from QR codes only.
        
        Args:
            qr_images: List of QR code image paths
            output_file: Path to save decrypted document
            private_key_path: Path to RSA private key
            password: Optional password for private key
            
        Returns:
            str: Path to decrypted file
        """
        # Load RSA private key
        private_key = self.rsa.load_private_key(private_key_path, password)
        
        # Decode QR codes
        if len(qr_images) == 1:
            package_json = self.qr.decode_qr(qr_images[0])
        else:
            package_json = self.qr.decode_multi_qr(qr_images)
        
        package = json.loads(package_json)
        
        # Decode from base64
        encrypted_data = base64.b64decode(package["encrypted_data"])
        encrypted_aes_key = base64.b64decode(package["encrypted_key"])
        iv = base64.b64decode(package["iv"])
        
        # Decrypt AES key with RSA
        aes_key = self.rsa.decrypt(encrypted_aes_key, private_key)
        
        # Decrypt document with AES
        decrypted_data = self.aes.decrypt(encrypted_data, aes_key, iv)
        
        # Save decrypted document
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"✓ Document decrypted from QR codes successfully!")
        print(f"  Decrypted file: {output_file}")
        
        return output_file
