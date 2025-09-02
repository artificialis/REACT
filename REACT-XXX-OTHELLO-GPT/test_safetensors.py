#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_safetensors.py
# A script to test the load_safetensors method in the GPT class
#

import torch
from model import GPT, GPTConfig

def test_load_safetensors():
    """
    Test the load_safetensors method in the GPT class.
    """
    # Path to the safetensors file
    safetensors_path = "checkpoints/synthetic_model.safetensors"
    
    # Create a GPT model with default configuration
    config = GPTConfig()
    model = GPT(config)
    
    # Print model parameters before loading
    print(f"Model parameters before loading: {model.get_num_params():,}")
    
    # Load the safetensors file
    try:
        model.load_safetensors(safetensors_path)
        print("Successfully loaded safetensors file!")
    except Exception as e:
        print(f"Error loading safetensors file: {e}")
        return
    
    # Print model parameters after loading
    print(f"Model parameters after loading: {model.get_num_params():,}")
    
    # Generate a simple sequence to verify the model works
    print("\nGenerating a sample sequence...")
    
    # Create a simple input tensor
    idx = torch.zeros((1, 1), dtype=torch.long)
    
    # Generate 10 tokens
    with torch.no_grad():
        output = model.generate(idx, max_new_tokens=10, temperature=0.8)
    
    print(f"Generated sequence shape: {output.shape}")
    print(f"Generated tokens: {output[0].tolist()}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_load_safetensors()