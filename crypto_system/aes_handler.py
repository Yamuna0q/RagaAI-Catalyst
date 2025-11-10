"""
AES Handler Module
Provides AES-256 encryption and decryption functionality for documents.
"""

import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class AESHandler:
    """Handles AES-256 encryption and decryption operations."""
    
    def __init__(self):
        """Initialize AES handler with 256-bit key size."""
        self.key_size = 32  # 256 bits
        self.block_size = 128  # AES block size in bits
        
    def generate_key(self) -> bytes:
        """
        Generate a random AES-256 key.
        
        Returns:
            bytes: 32-byte random key
        """
        return os.urandom(self.key_size)
    
    def generate_iv(self) -> bytes:
        """
        Generate a random initialization vector (IV).
        
        Returns:
            bytes: 16-byte random IV
        """
        return os.urandom(16)
    
    def encrypt(self, plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
        """
        Encrypt data using AES-256 in CBC mode.
        
        Args:
            plaintext: Data to encrypt
            key: 32-byte AES key
            
        Returns:
            tuple: (encrypted_data, iv)
        """
        # Generate random IV
        iv = self.generate_iv()
        
        # Pad the plaintext to be multiple of block size
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # Create cipher and encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return ciphertext, iv
    
    def decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Decrypt data using AES-256 in CBC mode.
        
        Args:
            ciphertext: Encrypted data
            key: 32-byte AES key
            iv: 16-byte initialization vector
            
        Returns:
            bytes: Decrypted plaintext
        """
        # Create cipher and decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext
    
    def encrypt_file(self, input_path: str, output_path: str, key: bytes) -> bytes:
        """
        Encrypt a file using AES-256.
        
        Args:
            input_path: Path to input file
            output_path: Path to save encrypted file
            key: 32-byte AES key
            
        Returns:
            bytes: IV used for encryption
        """
        # Read file content
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        # Encrypt
        ciphertext, iv = self.encrypt(plaintext, key)
        
        # Write encrypted data
        with open(output_path, 'wb') as f:
            f.write(ciphertext)
        
        return iv
    
    def decrypt_file(self, input_path: str, output_path: str, key: bytes, iv: bytes) -> None:
        """
        Decrypt a file using AES-256.
        
        Args:
            input_path: Path to encrypted file
            output_path: Path to save decrypted file
            key: 32-byte AES key
            iv: 16-byte initialization vector
        """
        # Read encrypted content
        with open(input_path, 'rb') as f:
            ciphertext = f.read()
        
        # Decrypt
        plaintext = self.decrypt(ciphertext, key, iv)
        
        # Write decrypted data
        with open(output_path, 'wb') as f:
            f.write(plaintext)
    
    def key_to_base64(self, key: bytes) -> str:
        """
        Convert key to base64 string for easy storage/transmission.
        
        Args:
            key: Binary key
            
        Returns:
            str: Base64 encoded key
        """
        return base64.b64encode(key).decode('utf-8')
    
    def base64_to_key(self, key_str: str) -> bytes:
        """
        Convert base64 string back to binary key.
        
        Args:
            key_str: Base64 encoded key
            
        Returns:
            bytes: Binary key
        """
        return base64.b64decode(key_str.encode('utf-8'))
