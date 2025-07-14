tokens = ["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", "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"]
current_token = 0

def rotate_token():
    global current_token
    current_token = (current_token + 1) % len(tokens)
    return tokens[current_token]

# Di setiap pemanggilan:
client = InferenceClient(token=rotate_token())