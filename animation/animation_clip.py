from animation.keyframe import Keyframe
import csv
import math

class AnimationClip:
    def __init__(self, keyframes):
        self.keyframes = keyframes
        self.framerate = 1/24

    def sample(self, progress: float) -> Keyframe:
        frame = progress * 24
        whole_frame = math.floor(frame)
        subframe = frame - whole_frame
        
        key_a = self.keyframes[whole_frame % len(self.keyframes)]
        key_b = self.keyframes[(whole_frame + 1) % len(self.keyframes)]

        inter_frame = Keyframe()
        for (name, a_value) in key_a.values.items():
            b_value = key_b.values[name]

            inter_frame.set_value(name, a_value + (b_value - a_value) * subframe)

        return inter_frame

    @classmethod
    def from_csv(cls, filename):
        with open(filename) as csvfile:
            contents = csv.DictReader(csvfile)

            keyframes = []
            headers = None
            for row in contents:
                if headers is None:
                    headers = row
                else:
                    keyframe = Keyframe()

                    for name in headers:
                        keyframe.set_value(name, float(row[name]))

                    keyframes.append(keyframe)
            
            return cls(keyframes)