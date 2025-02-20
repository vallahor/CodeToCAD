from abc import ABC


class FusionInterface(ABC):
    def translate(self, x: float, y: float, z: float):
        ...

    def rotate(self, axis_input: str, angle: float):
        ...

    def scale(self, x: float, y: float, z: float):
        ...

    def scale_by_factor(self, x: float, y: float, z: float):
        ...

    def scale_uniform(self, x: float, y: float, z: float):
        ...

    def clone(self):
        ...

    def rename(self, new_name):
        ...

    def delete(self):
        ...

    @property
    def center(self):
        ...
