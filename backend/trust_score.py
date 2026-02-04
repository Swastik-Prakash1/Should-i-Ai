# trust_score.py

def calculate_trust_score(fake_count, genuine_count, rating):
    """
    Calculates trust score (0–100) based on fake/genuine ratio and average rating.
    Higher score = more trustworthy product.
    """
    total_reviews = fake_count + genuine_count

    # Prevent division by zero
    if total_reviews == 0:
        return 50  # neutral default

    # Ratio of genuine reviews
    genuine_ratio = genuine_count / total_reviews

    # Rating normalization (0–1)
    normalized_rating = min(max(rating / 5, 0), 1)

    # Weighted formula: 80% genuine ratio + 20% rating
    score = int((genuine_ratio * 80) + (normalized_rating * 20))

    # Clamp between 0 and 100
    return min(100, max(0, score))
