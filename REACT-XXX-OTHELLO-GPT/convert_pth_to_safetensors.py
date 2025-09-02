#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# convert_pth_to_safetensors.py
# A script to convert PyTorch .pth files to safetensors format
#

import os
import sys
import argparse
import torch
import datetime
from typing import Dict, Any, Optional


def convert_to_safetensors(
    input_file: str, 
    output_file: Optional[str] = None, 
    metadata: Optional[Dict[str, str]] = None
) -> str:
    """
    Convert a PyTorch .pth file to safetensors format.
    
    Args:
        input_file: Path to the input .pth file
        output_file: Path to the output .safetensors file (if None, will use input_file with .safetensors extension)
        metadata: Optional metadata to include in the safetensors file
        
    Returns:
        Path to the created safetensors file
    """
    try:
        # Try to import safetensors
        from safetensors.torch import save_file
    except ImportError:
        print("Error: safetensors package not found. Please install it with:")
        print("pip install safetensors")
        sys.exit(1)
    
    # Set default output file if not provided
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.safetensors"
    
    print(f"Loading PyTorch file: {input_file}")
    try:
        # Load the PyTorch file
        state_dict = torch.load(input_file, map_location="cpu")
        
        # Check if it's a state_dict or a model
        if not isinstance(state_dict, dict):
            if hasattr(state_dict, 'state_dict') and callable(getattr(state_dict, 'state_dict')):
                print("Loaded a model, extracting state_dict...")
                state_dict = state_dict.state_dict()
            else:
                print(f"Error: The file contains an object of type {type(state_dict)}, which is not a state_dict or a model.")
                sys.exit(1)
        
        # Ensure all values are tensors
        tensor_dict = {}
        for key, value in state_dict.items():
            if isinstance(value, torch.Tensor):
                tensor_dict[key] = value
            else:
                print(f"Warning: Skipping non-tensor value for key '{key}' of type {type(value)}")
        
        if not tensor_dict:
            print("Error: No tensor found in the state_dict.")
            sys.exit(1)
        
        # Add metadata if provided
        if metadata is None:
            metadata = {}
        
        # Add some default metadata
        metadata.update({
            "source": "PyTorch",
            "original_file": os.path.basename(input_file),
            "conversion_date": datetime.datetime.now().isoformat(),
        })
        
        print(f"Saving to safetensors format: {output_file}")
        # Save to safetensors format
        save_file(tensor_dict, output_file, metadata=metadata)
        
        print(f"Successfully converted to {output_file}")
        
        # Print some stats
        total_size = sum(tensor.numel() * tensor.element_size() for tensor in tensor_dict.values())
        print(f"Total tensors: {len(tensor_dict)}")
        print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
        
        return output_file
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert PyTorch .pth files to safetensors format")
    parser.add_argument("input_file", help="Path to the input .pth file")
    parser.add_argument("-o", "--output", help="Path to the output .safetensors file (default: same as input with .safetensors extension)")
    parser.add_argument("-m", "--metadata", nargs="+", help="Additional metadata to include in the format key=value")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist.")
        return 1
    
    # Parse metadata if provided
    metadata = {}
    if args.metadata:
        for item in args.metadata:
            if "=" in item:
                key, value = item.split("=", 1)
                metadata[key] = value
            else:
                print(f"Warning: Ignoring metadata item '{item}' (format should be key=value)")
    
    convert_to_safetensors(args.input_file, args.output, metadata)
    return 0


if __name__ == "__main__":
    sys.exit(main())