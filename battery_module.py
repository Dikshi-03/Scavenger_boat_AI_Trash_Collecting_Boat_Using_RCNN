# battery_module.py

class BatteryModule:
    """Simulated battery (no ADS1115 needed)."""
    def __init__(self, channel=0):
        self.channel = channel
        print("[BatteryModule] Using dummy voltage (12V).")

    def get_voltage(self):
        """Return dummy battery voltage."""
        return 12.0  # Always safe for simulation
