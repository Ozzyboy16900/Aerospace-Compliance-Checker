# Aerospace Compliance Rules Database
# Add your own rules here based on your experience at Greenpoint Technologies!

AS9100_RULES = {
    "material_restrictions": {
        "crew_areas": [
            "beryllium copper",  # Can cause berylliosis
            "cadmium plating",   # Toxic fumes
            "lead solder"        # Lead poisoning risk
        ],
        "fuel_systems": [
            "aluminum-lithium alloys",  # Fire risk
            "magnesium alloys"          # Highly flammable
        ],
        "electrical": [
            "tin whiskers",      # Short circuit risk
            "pure tin plating"   # Whisker growth
        ]
    },
    
    "documentation_requirements": {
        "mandatory_fields": [
            "part_number",
            "revision",
            "material_specification",
            "surface_treatment",
            "heat_treatment"
        ],
        "traceability": [
            "serial_number",
            "lot_number",
            "batch_code",
            "manufacturer_code"
        ]
    },
    
    "supplier_requirements": {
        "certifications_needed": [
            "AS9100 Rev D",
            "ISO 9001:2015",
            "NADCAP (for special processes)"
        ],
        "blacklisted_countries": [
            # Add countries your company cannot source from
        ]
    }
}

ITAR_RULES = {
    "controlled_categories": {
        "CAT_VIII": "Aircraft and related equipment",
        "CAT_XII": "Fire control, guidance and control equipment",
        "CAT_XV": "Spacecraft and related articles"
    },
    
    "required_markings": [
        "Export of this data is restricted by ITAR",
        "22 CFR 120-130",
        "Controlled by DDTC"
    ],
    
    "restricted_countries": [
        "China", "Russia", "Iran", "North Korea",
        "Syria", "Cuba", "Venezuela"
    ]
}

FAR_RULES = {
    "domestic_content": {
        "minimum_percentage": 51,  # Buy American Act
        "specialty_metals": [
            "titanium",
            "zirconium",
            "beryllium"
        ]
    },
    
    "small_business_requirements": {
        "set_aside_threshold": 250000,  # Contracts over this must consider small business
        "subcontracting_minimum": 23    # Percentage for large contractors
    }
}

# Part numbering patterns (add your Greenpoint patterns here!)
PART_NUMBER_PATTERNS = {
    "boeing": r"^\d{3}-\d{5}-\d{3}$",           # Boeing format
    "airbus": r"^[A-Z]\d{6}[A-Z]{2}\d{3}$",    # Airbus format
    "military": r"^(MS|NAS|AN|MIL)-\d+.*$",    # Military standards
    # Add Greenpoint patterns:
    # "greenpoint": r"^GPT-\d{4}-[A-Z]\d$",    # Example
}

# Cost impact estimates (customize based on your experience)
VIOLATION_COSTS = {
    "ITAR": {
        "missing_marking": (10000, 100000),      # Min, Max fine
        "unauthorized_export": (100000, 1000000),
        "record_keeping": (5000, 50000)
    },
    "AS9100": {
        "material_violation": "Batch rejection + rework",
        "documentation": (1000, 10000),
        "supplier_issue": "Potential contract loss"
    },
    "FAR": {
        "false_claims": (5500, 11000),  # Per violation
        "buy_american": "Contract termination"
    }
}

# YOUR TURN TO ADD:
# Based on your experience at Greenpoint Technologies, add:

# 1. VIP aircraft specific requirements
VIP_AIRCRAFT_RULES = {
    # Example: "flammability": ["FAR 25.853", "burn test required"],
    # Add your rules here!
}

# 2. Common violations you've seen
COMMON_VIOLATIONS_SEEN = {
    # Example: "missing_heat_treatment": "Happens 30% of the time on brackets",
    # Add violations you've encountered!
}

# 3. Greenpoint-specific checks
COMPANY_SPECIFIC = {
    # Example: "vip_interior": ["leather must be aviation grade"],
    # Add company-specific requirements!
}
