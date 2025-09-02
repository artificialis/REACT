

# Imports
import argparse
from model import GPT, GPTConfig

# Config
vocab_size = 61
n_layers = 8
block_size = 64
n_head = 8
n_embd = 512

cfg = GPTConfig(
    vocab_size=vocab_size,
    block_size=block_size,
    n_layer=n_layers,
    n_head=n_head,
    n_embd=n_embd,
    bias=False
)

parser = argparse.ArgumentParser("OthelloGPT")
parser.add_argument("--safetensors", required=True, type=str, help="path to safetensors")
args = parser.parse_args()

gpt = GPT(cfg)
gpt.load_safetensors(args.safetensors)
