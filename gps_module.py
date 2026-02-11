# gps_module.py
class GPSModule:
    def __init__(self, use_dummy=True):
        # If True ? simulate GPS inside a 5x5 pool
        self.use_dummy = use_dummy
        self.start_coords = (0.0, 0.0) if use_dummy else None
        self.fake_position = [0.0, 0.0]  # (x,y) in meters for pool simulation

    def read_coordinates(self):
        """Return fake or real coordinates"""
        if self.use_dummy:
            return tuple(self.fake_position)
        return None  # Placeholder for real GPS (not used)

    def set_start_position(self):
        if self.use_dummy:
            self.start_coords = (0.0, 0.0)
            print(f"[GPS Dummy] Start position set at {self.start_coords}")
        else:
            print("[GPS] Waiting for fix... (real GPS not used)")
            self.start_coords = None

    def distance_from_start(self, coords):
        if not self.start_coords:
            return 0
        lat1, lon1 = self.start_coords
        lat2, lon2 = coords
        if self.use_dummy:
            dx = lat2 - lat1
            dy = lon2 - lon1
            return (dx**2 + dy**2) ** 0.5  # Euclidean distance in meters
        return 0
