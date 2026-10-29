import math

class BitcoinPegAccounting:
    """Defines conversion rates from raw resource contributions to Bitcoin Satoshis."""
    
    # Conversion weights per base unit (versioned and authoritative)
    SATOSHIS_PER_STORAGE_BYTE = 0.0001
    SATOSHIS_PER_CPU_CYCLE = 0.000001
    SATOSHIS_PER_MEMORY_MB = 0.001

    @classmethod
    def calculate_sats(cls, resource_type: str, quantity: float) -> int:
        if not math.isfinite(quantity) or quantity < 0:
            raise ValueError("Quantity must be a finite, non-negative number.")
            
        if resource_type == "storage":
            sats = quantity * cls.SATOSHIS_PER_STORAGE_BYTE
        elif resource_type == "cpu":
            sats = quantity * cls.SATOSHIS_PER_CPU_CYCLE
        elif resource_type == "memory":
            sats = quantity * cls.SATOSHIS_PER_MEMORY_MB
        else:
            raise ValueError(f"Unknown resource type: {resource_type}")
            
        return round(sats)
