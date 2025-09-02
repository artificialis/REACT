#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# show_safetensors_keys.py
# A script to show the keys present in a safetensors file
#

import argparse
import sys
from collections import defaultdict

def show_safetensors_keys(filepath, show_shapes=False, group_by_prefix=False):
    """
    Show the keys present in a safetensors file.
    
    Args:
        filepath (str): Path to the safetensors file
        show_shapes (bool): Whether to show tensor shapes
        group_by_prefix (bool): Whether to group keys by common prefixes
    """
    try:
        from safetensors.torch import load_file
    except ImportError:
        print("Error: Could not import safetensors. Please install safetensors with: pip install safetensors")
        sys.exit(1)
    
    try:
        # Load the safetensors file
        print(f"Loading safetensors file: {filepath}")
        state_dict = load_file(filepath)
        
        # Get the keys
        keys = list(state_dict.keys())
        
        if not keys:
            print("No keys found in the safetensors file.")
            return
        
        # Display the keys
        if group_by_prefix:
            # Group keys by common prefixes
            groups = defaultdict(list)
            for key in keys:
                # Split by first dot or use the whole key if no dot
                prefix = key.split('.', 1)[0]
                groups[prefix].append(key)
            
            print(f"\nFound {len(keys)} keys in {len(groups)} groups:")
            for prefix, group_keys in sorted(groups.items()):
                print(f"\n[{prefix}] ({len(group_keys)} keys):")
                for key in sorted(group_keys):
                    if show_shapes:
                        print(f"  {key} - Shape: {tuple(state_dict[key].shape)}")
                    else:
                        print(f"  {key}")
        else:
            # Display all keys in a flat list
            print(f"\nFound {len(keys)} keys:")
            for key in sorted(keys):
                if show_shapes:
                    print(f"{key} - Shape: {tuple(state_dict[key].shape)}")
                else:
                    print(key)
    
    except Exception as e:
        print(f"Error loading safetensors file: {e}")
        sys.exit(1)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Show keys in a safetensors file")
    parser.add_argument("filepath", type=str, help="Path to the safetensors file")
    parser.add_argument("--shapes", action="store_true", help="Show tensor shapes")
    parser.add_argument("--group", action="store_true", help="Group keys by common prefixes")
    
    args = parser.parse_args()
    
    # Show the keys
    show_safetensors_keys(args.filepath, args.shapes, args.group)

if __name__ == "__main__":
    main()