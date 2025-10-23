import sys
import tiktoken

# Read tool_call_response from file
if len(sys.argv) < 2:
    print("Usage: python get_size.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
with open(filename, 'r') as f:
    tool_call_response = f.read()

encoder = tiktoken.encoding_for_model("gpt-4")
num_tokens = len(encoder.encode(tool_call_response))
print(num_tokens)
