# PyTorch Model File Tools

This directory contains tools for working with PyTorch model files (.pth):

1. `analyze_pth.py` - A script to analyze the contents of a PyTorch .pth file
2. `convert_pth_to_safetensors.py` - A script to convert PyTorch .pth files to safetensors format

## Requirements

These scripts require the following Python packages:

- torch (already in requirements.txt)
- numpy (already in requirements.txt)
- safetensors (for conversion to safetensors format)

To install the safetensors package:

```bash
pip install safetensors
```

## Analyzing .pth Files

The `analyze_pth.py` script allows you to inspect the contents of a PyTorch .pth file, showing information about the tensors it contains.

### Usage

```bash
python analyze_pth.py [options] file_path
```

### Options

- `-v, --verbose`: Show detailed information for each tensor
- `-f, --filter FILTER`: Filter keys containing this string

### Examples

Basic usage:

```bash
python analyze_pth.py checkpoints/synthetic_model.pth
```

Verbose output:

```bash
python analyze_pth.py --verbose checkpoints/synthetic_model.pth
```

Filter by layer name:

```bash
python analyze_pth.py --filter "blocks.0" checkpoints/synthetic_model.pth
```

### Output

The script provides:

1. Basic information about the file type (state_dict, model, etc.)
2. Summary statistics (total parameters, size)
3. Layer-by-layer breakdown of parameters and size
4. Detailed tensor information (shape, dtype, min/max/mean/std) when using verbose mode

## Converting .pth Files to Safetensors

The `convert_pth_to_safetensors.py` script converts PyTorch .pth files to the safetensors format, which offers better security and faster loading times.

### Usage

```bash
python convert_pth_to_safetensors.py [options] input_file
```

### Options

- `-o, --output OUTPUT`: Path to the output .safetensors file (default: same as input with .safetensors extension)
- `-m, --metadata KEY=VALUE [KEY=VALUE ...]`: Additional metadata to include in the format key=value

### Examples

Basic usage:

```bash
python convert_pth_to_safetensors.py checkpoints/synthetic_model.pth
```

Specify output file:

```bash
python convert_pth_to_safetensors.py checkpoints/synthetic_model.pth -o models/synthetic_model.safetensors
```

Add metadata:

```bash
python convert_pth_to_safetensors.py checkpoints/synthetic_model.pth -m model_type=transformer version=1.0
```

## Why Use Safetensors?

The safetensors format offers several advantages over the standard PyTorch .pth format:

1. **Security**: Safetensors prevents arbitrary code execution during loading, making it safer to load models from untrusted sources.
2. **Speed**: Safetensors can be memory-mapped, allowing for faster loading of large models.
3. **Compatibility**: Safetensors files can be easily shared across different frameworks.
4. **Metadata**: Safetensors supports storing metadata alongside the model weights.

## Notes

- Both scripts handle different types of .pth files, including state dictionaries and full models.
- The conversion script will extract the state dictionary from a full model if needed.
- Non-tensor values in the state dictionary will be skipped during conversion to safetensors.