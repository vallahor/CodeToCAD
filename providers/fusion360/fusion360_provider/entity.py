from typing import Optional

from codetocad.interfaces import EntityInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

from providers.fusion360.fusion360_provider.fusion_actions.base import get_component

from .fusion_actions.fusion_landmark import FusionLandmark

from .fusion_actions.fusion_body import FusionBody

from .fusion_actions.fusion_sketch import FusionSketch

if TYPE_CHECKING:
    from . import Landmark


class Entity(EntityInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.fusion_sketch = FusionSketch(name)
        self.fusion_body = FusionBody(name)

    @property
    def center(self):
        from . import Part, Sketch
        if isinstance(self, Part):
            return self.fusion_body.center
        if isinstance(self, Sketch):
            return self.fusion_sketch.center

    def is_exists(self) -> bool:
        print(
            "is_exists called:",
        )
        return True

    def rename(self, new_name: str, renamelinked_entities_and_landmarks: bool = True):
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            self.fusion_body.rename(new_name)
        if isinstance(self, Sketch):
            self.fusion_sketch.rename(new_name)
        if isinstance(self, Landmark):
            self.fusion_landmark.rename(new_name)
        return self

    def delete(self, remove_children: bool = True):
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            self.fusion_body.delete()
        if isinstance(self, Sketch):
            self.fusion_sketch.delete()
        if isinstance(self, Landmark):
            self.fusion_landmark.delete()
        return self

    def is_visible(self) -> bool:
        print(
            "is_visible called:",
        )
        return True

    def set_visible(self, is_visible: bool):
        print("set_visible called:", is_visible)
        return self

    def apply(
        self,
        rotation: bool = True,
        scale: bool = True,
        location: bool = False,
        modifiers: bool = True,
    ):
        print("apply called:", rotation, scale, location, modifiers)
        return self

    def get_native_instance(self) -> object:
        print(
            "get_native_instance called:",
        )
        return "instance"

    def get_location_world(self) -> "Point":
        print(
            "get_location_world called:",
        )
        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_location_local(self) -> "Point":
        # check the correct behavior
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            pos = self.fusion_body.center
        elif isinstance(self, Sketch):
            pos = self.fusion_sketch.center
        elif isinstance(self, Landmark):
            pos = self.fusion_landmark.get_point()

        return Point(pos.x, pos.y, pos.z)

    def select(self):
        print(
            "select called:",
        )
        return self

    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            self.fusion_body.translate(x, y, z)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(x, y, z)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(x, y, z)
        return self

    def translate_x(self, amount: DimensionOrItsFloatOrStringValue):
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            self.fusion_body.translate(amount, 0, 0)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(amount, 0, 0)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(amount, 0, 0)
        return self

    def translate_y(self, amount: DimensionOrItsFloatOrStringValue):
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            self.fusion_body.translate(0, amount, 0)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(0, amount, 0)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(0, amount, 0)
        return self

    def translate_z(self, amount: DimensionOrItsFloatOrStringValue):
        from . import Part, Sketch, Landmark
        if isinstance(self, Part):
            self.fusion_body.translate(0, 0, amount)
        elif isinstance(self, Sketch):
            self.fusion_sketch.translate(0, 0, amount)
        elif isinstance(self, Landmark):
            self.fusion_landmark.translate(0, 0, amount)
        return self

    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        print("rotate_xyz called:", x, y, z)
        return self

    def rotate_x(self, rotation: AngleOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.rotate("x", rotation)
        else:
            self.fusion_sketch.rotate("x", rotation)
        return self

    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.rotate("y", rotation)
        else:
            self.fusion_sketch.rotate("y", rotation)
        return self

    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        from . import Part
        if isinstance(self, Part):
            self.fusion_body.rotate("z", rotation)
        else:
            self.fusion_sketch.rotate("z", rotation)
        return self

    def get_bounding_box(self) -> "BoundaryBox":
        from . import Part
        if isinstance(self, Part):
            boundaryBox = self.fusion_body.get_bounding_box()
        else:
            boundaryBox = self.fusion_sketch.get_bounding_box()
        return boundaryBox

    def get_dimensions(self) -> "Dimensions":
        print(
            "get_dimensions called:",
        )
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    def create_landmark(
        self,
        landmark_name: "str",
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "Landmark":
        from . import Landmark
        boundingBox =  self.fusion_body.get_bounding_box()

        localPositions = [
            Dimension.from_dimension_or_its_float_or_string_value(x, boundingBox.x),
            Dimension.from_dimension_or_its_float_or_string_value(y, boundingBox.y),
            Dimension.from_dimension_or_its_float_or_string_value(z, boundingBox.z),
        ]

        landmark = Landmark(landmark_name, self)
        landmark.fusion_landmark.create_landmark(
            localPositions[0].value,
            localPositions[1].value,
            localPositions[2].value,
        )

        return landmark

    def get_landmark(self, landmark_name: PresetLandmarkOrItsName) -> "Landmark":
        if isinstance(landmark_name, LandmarkInterface):
            landmark_name = landmark_name.name

        preset: Optional[PresetLandmark] = None

        if isinstance(landmark_name, str):
            preset = PresetLandmark.from_string(landmark_name)

        if isinstance(landmark_name, PresetLandmark):
            preset = landmark_name
            landmark_name = preset.name

        landmark = Landmark(landmark_name, self.name)

        if preset is not None:
            component = get_component(landmark.get_landmark_entity_name())

            if component is None:
                presetXYZ = preset.get_xyz()
                self.create_landmark(
                    landmark_name, presetXYZ[0], presetXYZ[1], presetXYZ[2]
                )

                return landmark
        return landmark
