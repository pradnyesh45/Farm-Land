from typing import Dict

# Define fertilizer prices
FERTILIZER_PRICES: Dict[str, float] = {
    'Urea': 100,
    'DAP': 150,
    'NPK': 200,
    'Micronutrient': 250,
}

def calculate_fertilizer_cost(fertilizer_type: str, quantity: float, area: float) -> float:
    """Calculate the cost of fertilizer for a given area"""
    base_price = FERTILIZER_PRICES.get(fertilizer_type, 0)
    return base_price * quantity * area