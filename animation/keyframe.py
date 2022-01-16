class Keyframe:
    def __init__(self):
        self.values = {}

    def set_value(self, key: str, value: float):
        self.values[key] = value
