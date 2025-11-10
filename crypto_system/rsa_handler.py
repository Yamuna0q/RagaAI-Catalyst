"""
RSA Handler Module
Provides RSA-2048 key generation, encryption, and decryption functionality.
"""

import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


class RSAHandler:
    """Handles RSA-2048 encryption and decryption operations."""
    
    def __init__(self):
        """Initialize RSA handler with 2048-bit key size."""
        self.key_size = 2048
        self.public_exponent = 65537
        
    def generate_key_pair(self) -> tuple:
        """
        Generate RSA-2048 key pair.
        
        Returns:
            tuple: (private_key, public_key)
        """
        private_key = rsa.generate_private_key(
            public_exponent=self.public_exponent,
            key_size=self.key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        return private_key, public_key
    
    def encrypt(self, plaintext: bytes, public_key) -> bytes:
        """
        Encrypt data using RSA public key with OAEP padding.
        
        Args:
            plaintext: Data to encrypt (max 190 bytes for RSA-2048)
            public_key: RSA public key object
            
        Returns:
            bytes: Encrypted data
        """
        ciphertext = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext
    
    def decrypt(self, ciphertext: bytes, private_key) -> bytes:
        """
        Decrypt data using RSA private key.
        
        Args:
            ciphertext: Encrypted data
            private_key: RSA private key object
            
        Returns:
            bytes: Decrypted plaintext
        """
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext
    
    def save_private_key(self, private_key, filepath: str, password: bytes = None) -> None:
        """
        Save private key to file in PEM format.
        
        Args:
            private_key: RSA private key object
            filepath: Path to save the key
            password: Optional password to encrypt the key
        """
        if password:
            encryption_algorithm = serialization.BestAvailableEncryption(password)
        else:
            encryption_algorithm = serialization.NoEncryption()
        
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )
        
        with open(filepath, 'wb') as f:
            f.write(pem)
    
    def save_public_key(self, public_key, filepath: str) -> None:
        """
        Save public key to file in PEM format.
        
        Args:
            public_key: RSA public key object
            filepath: Path to save the key
        """
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        with open(filepath, 'wb') as f:
            f.write(pem)
    
    def load_private_key(self, filepath: str, password: bytes = None):
        """
        Load private key from file.
        
        Args:
            filepath: Path to the key file
            password: Optional password if key is encrypted
            
        Returns:
            RSA private key object
        """
        with open(filepath, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=password,
                backend=default_backend()
            )
        return private_key
    
    def load_public_key(self, filepath: str):
        """
        Load public key from file.
        
        Args:
            filepath: Path to the key file
            
        Returns:
            RSA public key object
        """
        with open(filepath, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        return public_key
    
    def public_key_to_pem(self, public_key) -> str:
        """
        Convert public key to PEM string.
        
        Args:
            public_key: RSA public key object
            
        Returns:
            str: PEM formatted public key
        """
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    
    def private_key_to_pem(self, private_key, password: bytes = None) -> str:
        """
        Convert private key to PEM string.
        
        Args:
            private_key: RSA private key object
            password: Optional password to encrypt the key
            
        Returns:
            str: PEM formatted private key
        """
        if password:
            encryption_algorithm = serialization.BestAvailableEncryption(password)
        else:
            encryption_algorithm = serialization.NoEncryption()
        
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )
        return pem.decode('utf-8')
    
    def pem_to_public_key(self, pem_str: str):
        """
        Convert PEM string to public key object.
        
        Args:
            pem_str: PEM formatted public key string
            
        Returns:
            RSA public key object
        """
        return serialization.load_pem_public_key(
            pem_str.encode('utf-8'),
            backend=default_backend()
        )
    
    def pem_to_private_key(self, pem_str: str, password: bytes = None):
        """
        Convert PEM string to private key object.
        
        Args:
            pem_str: PEM formatted private key string
            password: Optional password if key is encrypted
            
        Returns:
            RSA private key object
        """
        return serialization.load_pem_private_key(
            pem_str.encode('utf-8'),
            password=password,
            backend=default_backend()
        )
