from typing import Optional

from codetocad.interfaces import JointInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

from providers.fusion360.fusion360_provider.fusion_actions.fusion_joint import FusionJoint

if TYPE_CHECKING:
    from . import Entity
    from . import Sketch


class Joint(JointInterface):
    entity1: EntityOrItsName
    entity2: EntityOrItsName
    fusion_joint: FusionJoint

    def __init__(self, entity1: EntityOrItsName, entity2: EntityOrItsName):
        from . import Landmark
        if isinstance(entity1, str):
            entity1 = Landmark(entity1)
        if isinstance(entity2, str):
            entity2 = Landmark(entity2)

        self.entity1 = entity1
        self.entity2 = entity2
        self.fusion_joint = FusionJoint(entity1, entity2)

    def translate_landmark_onto_another(self):
        if not isinstance(self.entity1, LandmarkInterface) or not isinstance(
            self.entity2, LandmarkInterface
        ):
            raise TypeError("Entities 1 and 2 should be landmarks.")

        landmark1: LandmarkInterface = self.entity1
        landmark2: LandmarkInterface = self.entity2
        entityForLandmark2 = self.entity2.get_parent_entity()

        translation = landmark1.get_location_world() - landmark2.get_location_world()

        entityForLandmark2.translate_xyz(translation.x, translation.y, translation.z)

        return self


    def pivot(self):
        return self

    def gear_ratio(self, ratio: float):
        print("gear_ratio called:", ratio)
        return self

    @staticmethod
    def _get_limit_location_pair(min, max) -> list[Optional[Dimension]]:
        locationPair: list[Optional[Dimension]] = [None, None]

        if min is not None:
            locationPair[0] = Dimension.from_string(min)
        if max is not None:
            locationPair[1] = Dimension.from_string(max)

        return locationPair

    def _limit_rotation_xyz(self, rotation_pair_x, rotation_pair_y, rotation_pair_z):
        if rotation_pair_x:
            self.fusion_joint.limit_rotation_motion("x", rotation_pair_x[0].value, rotation_pair_x[1].value)
        elif rotation_pair_y:
            self.fusion_joint.limit_rotation_motion("y", rotation_pair_y[0].value, rotation_pair_y[1].value)
        elif rotation_pair_z:
            self.fusion_joint.limit_rotation_motion("z", rotation_pair_z[0].value, rotation_pair_z[1].value)
        return self

    def limit_location_xyz(
        self,
        x: Optional[DimensionOrItsFloatOrStringValue] = None,
        y: Optional[DimensionOrItsFloatOrStringValue] = None,
        z: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        # offset = self.entity2.get_location_local() * -1
        offset = self.entity2.get_location_local()
        offset.x = offset.x * -1
        offset.y = offset.x * -1
        offset.z = offset.x * -1

        if x and x[0]:
            x[0] += offset.x
        if x and x[1]:
            x[1] += offset.x
        if y and y[0]:
            y[0] += offset.y
        if y and y[1]:
            y[1] += offset.y
        if z and z[0]:
            z[0] += offset.z
        if z and z[1]:
            z[1] += offset.z

        if x:
            self.fusion_join.limit_location("x", x[0], x[1])
        elif y:
            self.fusion_join.limit_location("y", y[0], y[1])
        elif z:
            self.fusion_join.limit_location("z", z[0], z[1])

        return self

    def limit_location_x(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)

        self._limit_location_xyz(dimensions, None, None)
        return self

    def limit_location_y(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)

        self._limit_location_xyz(None, dimensions, None)
        return self

    def limit_location_z(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)

        self._limit_location_xyz(None, None, dimensions)
        return self

    def limit_rotation_xyz(
        self,
        x: Optional[AngleOrItsFloatOrStringValue] = None,
        y: Optional[AngleOrItsFloatOrStringValue] = None,
        z: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotation_pair_x = (
            Joint._get_limit_rotation_pair(x, x) if x is not None else None
        )
        rotation_pair_y = (
            Joint._get_limit_rotation_pair(y, y) if y is not None else None
        )
        rotation_pair_z = (
            Joint._get_limit_rotation_pair(z, z) if z is not None else None
        )

        self._limit_rotation_xyz(rotation_pair_x, rotation_pair_y, rotation_pair_z)
        return self

    @staticmethod
    def _get_limit_rotation_pair(min, max) -> list[Optional[Angle]]:
        rotationPair: list[Optional[Angle]] = [None, None]

        if min is not None:
            rotationPair[0] = Angle.from_string(min).to_radians()
        if max is not None:
            rotationPair[1] = Angle.from_string(max).to_radians()

        return rotationPair

    def limit_rotation_x(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(rotationPair, None, None)

    def limit_rotation_y(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(None, rotationPair, None)

    def limit_rotation_z(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(None, None, rotationPair)

    @classmethod
    def get_dummy_obj(cls):
        from . import Sketch

        instance = Sketch("mySketch")

        edge = instance.create_line(end_at=(0, 5, 0), start_at=(5, 10, 0))

        instance = Sketch("mySketch")

        edge2 = instance.create_line(end_at=(5, 10, 0), start_at=(5, 5, 0))

        return cls(
            entity1="mySketch",
            entity2="mySketch2",
        )
