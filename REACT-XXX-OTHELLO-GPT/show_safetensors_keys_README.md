# Show SafeTensors Keys

A utility script to display the keys present in a SafeTensors file.

## Overview

The `show_safetensors_keys.py` script allows you to inspect the contents of a SafeTensors file by displaying all the keys (tensor names) present in the file. This can be useful for understanding the structure of a model saved in the SafeTensors format.

SafeTensors is a safer alternative to PyTorch's native format, preventing arbitrary code execution during model loading.

## Requirements

- Python 3.6+
- safetensors package (`pip install safetensors`)

## Usage

Basic usage:

```bash
python show_safetensors_keys.py path/to/your/model.safetensors
```

This will display a list of all keys in the SafeTensors file.

### Options

The script supports the following command-line options:

- `--shapes`: Show the shape of each tensor alongside its key
- `--group`: Group keys by common prefixes for better organization

Example with all options:

```bash
python show_safetensors_keys.py path/to/your/model.safetensors --shapes --group
```

## Example Output

### Basic Output

```
Loading safetensors file: model.safetensors
Found 116 keys:
blocks.0.attn.IGNORE
blocks.0.attn.W_K
blocks.0.attn.W_O
...
```

### With --shapes and --group Options

```
Loading safetensors file: model.safetensors
Found 116 keys in 4 groups:
[blocks] (112 keys):
  blocks.0.attn.IGNORE - Shape: ()
  blocks.0.attn.W_K - Shape: (8, 512, 64)
  blocks.0.attn.W_O - Shape: (8, 64, 512)
...
[embed] (1 keys):
  embed.W_E - Shape: (61, 512)
...
```

## Integration

This script can be used as a standalone utility or integrated into your workflow for model inspection and debugging.