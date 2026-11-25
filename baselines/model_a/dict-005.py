def top_k(d, k):
    return [key for key, _ in sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:k]]
