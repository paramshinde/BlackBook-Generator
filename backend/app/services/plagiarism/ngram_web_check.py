# Optional external n-gram lookup hook.
# In production this can call search APIs to compare sampled phrases.

def web_ngram_hits(_: str) -> int:
    return 0
