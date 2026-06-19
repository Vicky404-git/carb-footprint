# data/emission_factors.py
# all food factors are per GRAM of food (kg CO2 per gram)

FACTORS = {
    "transport": {
        "car":   0.21,    # kg CO2 per meter... nah per km
        "bike":  0.11,
        "bus":   0.089,
        "train": 0.037,
    },
    "food": {
        # kg CO2 per gram of food
        "rice":          0.0028,
        "dal":           0.0009,
        "roti":          0.0012,
        "sabzi":         0.0008,
        "paneer":        0.0035,
        "rajma":         0.0020,
        "chole":         0.0019,
        "idli":          0.0007,
        "dosa":          0.0009,
        "poha":          0.0006,
        "upma":          0.0007,
        "salad":         0.0004,
        # NON-VEG (not for vegiterians/vegans so donot see ts )
        "chicken_curry": 0.0035,
        "egg":           0.0043,
        "fish_curry":    0.0031,
        "mutton":        0.0100,
    },
    "energy": {
        "ac":          0.6,    # kg CO2 per hour (1.5 ton AC, India grid)
        "gas_stove":   0.21,   # kg CO2 per hour
        "fan":         0.035,  # kg CO2 per hour
        "geyser":      0.55,   # kg CO2 per hour
    },
    "shopping": {
        "clothing_item":     5.5,   # kg CO2 per item
        "electronics_item":  300.0, # kg CO2 per device (avg phone/laptop/other appliences)
        "plastic_bag":       0.012, # kg CO2 per bag
        "online_order":      0.5,   # kg CO2 per delivery (u can change)
    }
}

# units shown in UI per activity
UNITS = {
    "transport": {
        "car": "km", "bike": "km", "bus": "km", "train": "km"
    },
    "food": {
        "rice":"g","dal":"g","roti":"g","sabzi":"g","paneer":"g",
        "rajma":"g","chole":"g","idli":"g","dosa":"g","poha":"g",
        "upma":"g","salad":"g","chicken_curry":"g","egg":"g",
        "fish_curry":"g","mutton":"g"
    },
    "energy": {
        "ac":"hrs","gas_stove":"hrs","fan":"hrs","geyser":"hrs"
    },
    "shopping": {
        "clothing_item":"items","electronics_item":"items",
        "plastic_bag":"bags","online_order":"orders"
    }
}

# validation max per single log
MAX_QTY = {
    "transport": 1000,    # km
    "food":      10000,   # grams
    "energy":    24,      # hours
    "shopping":  50,      # items/bags/orders
}
