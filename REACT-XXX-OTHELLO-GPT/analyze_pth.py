#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# analyze_pth.py
# A script to analyze the contents of a PyTorch .pth file
#

import os
import sys
import argparse
import torch
import numpy as np
from collections import defaultdict


def analyze_tensor(name, tensor):
    """Analyze a single tensor and return its properties."""
    result = {
        "shape": list(tensor.shape),
        "dtype": str(tensor.dtype),
        "numel": tensor.numel(),
        "memory_size_mb": tensor.element_size() * tensor.numel() / (1024 * 1024)
    }
    
    # Handle different dtypes for statistical calculations
    if tensor.numel() > 0:
        # Always safe operations
        result["min"] = float(tensor.min().item())
        result["max"] = float(tensor.max().item())
        
        # Operations that require numeric types
        if tensor.dtype in [torch.float16, torch.float32, torch.float64, 
                           torch.int8, torch.int16, torch.int32, torch.int64]:
            result["mean"] = float(tensor.mean().item())
            result["std"] = float(tensor.std().item()) if tensor.numel() > 1 else 0.0
        elif tensor.dtype == torch.bool:
            # For boolean tensors, calculate mean as percentage of True values
            # and std doesn't really make sense
            float_tensor = tensor.float()
            result["mean"] = float(float_tensor.mean().item())
            result["std"] = float(float_tensor.std().item()) if tensor.numel() > 1 else 0.0
        else:
            # For other types, skip these calculations
            result["mean"] = None
            result["std"] = None
    else:
        result["min"] = None
        result["max"] = None
        result["mean"] = None
        result["std"] = None
        
    return result


def analyze_pth_file(file_path, verbose=False, filter_key=None):
    """
    Analyze a .pth file and print information about its contents.
    """
    print(f"Analyzing {file_path}...")
    
    try:
        # Load the .pth file
        state_dict = torch.load(file_path, map_location=torch.device('cpu'))
        print(f"File loaded successfully.")
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    # Check if it's a state_dict or something else
    if isinstance(state_dict, dict):
        print("File contains a dictionary (likely a state_dict).")
        
        # Collect statistics
        total_params = 0
        total_size_mb = 0
        layer_stats = defaultdict(lambda: {"count": 0, "params": 0, "size_mb": 0})
        
        # Filter keys if specified
        keys = state_dict.keys()
        if filter_key:
            keys = [k for k in keys if filter_key in k]
            if not keys:
                print(f"No keys found matching filter: {filter_key}")
                return
        
        # Print header for the table
        if verbose:
            print("\n{:<50} {:<20} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
                "Key", "Shape", "Dtype", "Min", "Max", "Mean", "Std"))
            print("-" * 120)
        
        # Analyze each tensor
        for key in sorted(keys):
            value = state_dict[key]
            
            if isinstance(value, torch.Tensor):
                stats = analyze_tensor(key, value)
                
                # Extract layer name (assuming common naming patterns)
                layer_name = key.split('.')[0] if '.' in key else 'other'
                
                # Update statistics
                total_params += stats["numel"]
                total_size_mb += stats["memory_size_mb"]
                layer_stats[layer_name]["count"] += 1
                layer_stats[layer_name]["params"] += stats["numel"]
                layer_stats[layer_name]["size_mb"] += stats["memory_size_mb"]
                
                # Print detailed information if verbose
                if verbose:
                    print("{:<50} {:<20} {:<10} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(
                        key, str(stats["shape"]), stats["dtype"], 
                        stats["min"], stats["max"], stats["mean"], stats["std"]))
            else:
                if verbose:
                    print(f"{key}: Not a tensor, type: {type(value)}")
        
        # Print summary
        print("\nSummary:")
        print(f"Total number of keys: {len(keys)}")
        print(f"Total parameters: {total_params:,}")
        print(f"Total size: {total_size_mb:.2f} MB")
        
        # Print layer statistics
        print("\nLayer Statistics:")
        print("{:<20} {:<10} {:<15} {:<10}".format("Layer", "Count", "Parameters", "Size (MB)"))
        print("-" * 55)
        for layer_name, stats in sorted(layer_stats.items()):
            print("{:<20} {:<10} {:<15,} {:<10.2f}".format(
                layer_name, stats["count"], stats["params"], stats["size_mb"]))
    
    elif isinstance(state_dict, torch.nn.Module):
        print("File contains a full model (torch.nn.Module).")
        print(f"Model type: {type(state_dict)}")
        
        # Try to get the model's state_dict
        try:
            model_state_dict = state_dict.state_dict()
            print(f"Model has {len(model_state_dict)} parameters/buffers.")
            print("To analyze the model's parameters, save the state_dict directly.")
        except Exception as e:
            print(f"Could not access state_dict: {e}")
    
    else:
        print(f"File contains an object of type: {type(state_dict)}")
        print("Contents cannot be analyzed as a standard PyTorch state dictionary.")


def main():
    parser = argparse.ArgumentParser(description="Analyze the contents of a PyTorch .pth file")
    parser.add_argument("file_path", help="Path to the .pth file to analyze")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed information for each tensor")
    parser.add_argument("-f", "--filter", help="Filter keys containing this string")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File {args.file_path} does not exist.")
        return 1

    
    analyze_pth_file(args.file_path, args.verbose, args.filter)
    return 0


if __name__ == "__main__":
    sys.exit(main())