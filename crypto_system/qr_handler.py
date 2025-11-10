"""
QR Code Handler Module
Provides QR code generation and decoding functionality for encrypted data.
"""

import base64
import json
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode as pyzbar_decode
import cv2
import numpy as np


class QRHandler:
    """Handles QR code generation and decoding operations."""
    
    def __init__(self):
        """Initialize QR handler with default settings."""
        self.version = 1  # QR code version (1-40)
        self.error_correction = qrcode.constants.ERROR_CORRECT_H  # High error correction
        self.box_size = 10
        self.border = 4
    
    def generate_qr(self, data: str, output_path: str = None) -> Image:
        """
        Generate QR code from string data.
        
        Args:
            data: String data to encode
            output_path: Optional path to save QR code image
            
        Returns:
            PIL.Image: QR code image
        """
        qr = qrcode.QRCode(
            version=None,  # Auto-detect version
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if output_path:
            img.save(output_path)
        
        return img
    
    def decode_qr(self, image_path: str) -> str:
        """
        Decode QR code from image file.
        
        Args:
            image_path: Path to QR code image
            
        Returns:
            str: Decoded data from QR code
            
        Raises:
            ValueError: If no QR code found or decoding fails
        """
        # Read image using OpenCV
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Decode QR code
        decoded_objects = pyzbar_decode(img)
        
        if not decoded_objects:
            raise ValueError("No QR code found in image")
        
        # Return data from first QR code found
        return decoded_objects[0].data.decode('utf-8')
    
    def encode_binary_to_qr(self, binary_data: bytes, output_path: str = None) -> Image:
        """
        Encode binary data to QR code using base64.
        
        Args:
            binary_data: Binary data to encode
            output_path: Optional path to save QR code image
            
        Returns:
            PIL.Image: QR code image
        """
        # Convert binary to base64 string
        base64_str = base64.b64encode(binary_data).decode('utf-8')
        
        return self.generate_qr(base64_str, output_path)
    
    def decode_qr_to_binary(self, image_path: str) -> bytes:
        """
        Decode QR code and convert base64 string back to binary.
        
        Args:
            image_path: Path to QR code image
            
        Returns:
            bytes: Decoded binary data
        """
        base64_str = self.decode_qr(image_path)
        return base64.b64decode(base64_str)
    
    def encode_dict_to_qr(self, data_dict: dict, output_path: str = None) -> Image:
        """
        Encode dictionary to QR code as JSON.
        
        Args:
            data_dict: Dictionary to encode
            output_path: Optional path to save QR code image
            
        Returns:
            PIL.Image: QR code image
        """
        json_str = json.dumps(data_dict)
        return self.generate_qr(json_str, output_path)
    
    def decode_qr_to_dict(self, image_path: str) -> dict:
        """
        Decode QR code and parse as JSON dictionary.
        
        Args:
            image_path: Path to QR code image
            
        Returns:
            dict: Decoded dictionary
        """
        json_str = self.decode_qr(image_path)
        return json.loads(json_str)
    
    def create_multi_qr(self, data_list: list, output_dir: str, prefix: str = "qr") -> list:
        """
        Create multiple QR codes from a list of data.
        
        Args:
            data_list: List of data items to encode
            output_dir: Directory to save QR code images
            prefix: Prefix for output filenames
            
        Returns:
            list: List of output file paths
        """
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_paths = []
        for i, data in enumerate(data_list):
            output_path = os.path.join(output_dir, f"{prefix}_{i+1}.png")
            self.generate_qr(data, output_path)
            output_paths.append(output_path)
        
        return output_paths
    
    def split_large_data(self, data: str, max_size: int = 2000) -> list:
        """
        Split large data into chunks for multiple QR codes.
        
        Args:
            data: Large string data
            max_size: Maximum size per chunk
            
        Returns:
            list: List of data chunks
        """
        chunks = []
        for i in range(0, len(data), max_size):
            chunks.append(data[i:i+max_size])
        return chunks
    
    def encode_large_data_to_qr(self, data: str, output_dir: str, prefix: str = "qr") -> list:
        """
        Encode large data into multiple QR codes.
        
        Args:
            data: Large string data
            output_dir: Directory to save QR code images
            prefix: Prefix for output filenames
            
        Returns:
            list: List of output file paths
        """
        chunks = self.split_large_data(data)
        
        # Add metadata to each chunk
        chunk_data = []
        for i, chunk in enumerate(chunks):
            chunk_dict = {
                "index": i,
                "total": len(chunks),
                "data": chunk
            }
            chunk_data.append(json.dumps(chunk_dict))
        
        return self.create_multi_qr(chunk_data, output_dir, prefix)
    
    def decode_multi_qr(self, image_paths: list) -> str:
        """
        Decode and combine data from multiple QR codes.
        
        Args:
            image_paths: List of QR code image paths
            
        Returns:
            str: Combined decoded data
        """
        chunks = []
        
        for path in image_paths:
            json_str = self.decode_qr(path)
            chunk_dict = json.loads(json_str)
            chunks.append(chunk_dict)
        
        # Sort by index
        chunks.sort(key=lambda x: x["index"])
        
        # Combine data
        combined_data = "".join([chunk["data"] for chunk in chunks])
        
        return combined_data
