from typing import Optional
from adsk.fusion import adsk

from codetocad.interfaces import PartInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from .fusion_actions.actions import chamfer_all_edges, combine, create_circular_pattern_sketch, create_rectangular_pattern, fillet_all_edges, hole, hollow, intersect, mirror, set_material, subtract
from .fusion_actions.fusion_sketch import FusionSketch

from .fusion_actions.base import delete_occurrence, get_body, get_component
from .fusion_actions.curve import make_arc, make_circle, make_lines, make_rectangle
from .fusion_actions.modifiers import make_loft, make_revolve

from .fusion_actions.fusion_body import FusionBody

from . import Entity

from .fusion_actions.common import (
    make_point3d,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Landmark
    from . import Entity
    from . import Material


class Part(Entity, PartInterface):
    def __init__(self, name: str):
        self.fusion_body = FusionBody(name)
        self.name = name

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        from . import Sketch
        if isinstance(mirror_across_entity, str):
            component = get_component(mirror_across_entity)
            if get_body(component, mirror_across_entity):
                mirror_across_entity = Part(mirror_across_entity).fusion_body
            else:
                mirror_across_entity = Sketch(mirror_across_entity).fusion_sketch

        body, newPosition = mirror(
            self.fusion_body,
            mirror_across_entity.center,
            axis
        )
        part = self.__class__(body.name)
        part.fusion_body.instance = body
        part.translate_xyz(newPosition.x, newPosition.y, newPosition.z)
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        create_rectangular_pattern(
            self.fusion_body.component,
            instance_count,
            offset,
            direction_axis
        )
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        from . import Sketch
        if isinstance(center_entity_or_landmark, str):
            component = get_component(center_entity_or_landmark)
            if get_body(component, center_entity_or_landmark):
                center_entity_or_landmark = Part(center_entity_or_landmark).fusion_body
            else:
                center_entity_or_landmark = Sketch(center_entity_or_landmark).fusion_sketch

        center = center_entity_or_landmark.center
        create_circular_pattern_sketch(
            self.fusion_body,
            center,
            instance_count,
            separation_angle,
            normal_direction_axis,
        )

        return self

    def remesh(self, strategy: str, amount: float):
        print("remesh called:", strategy, amount)
        return self

    def subdivide(self, amount: float):
        print("subdivide called:", amount)
        return self

    def decimate(self, amount: float):
        print("decimate called:", amount)
        return self

    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        print("create_from_file called:", file_path, file_type)
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        print("export called:", file_path, overwrite, scale)
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        self.fusion_body.scale(x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_body.scale(scale.value, 0, 0)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_body.scale(0, scale.value, 0)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_body.scale(0, 0, scale.value)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(scale_factor, None)
        self.fusion_body.scale_by_factor(scale_factor.value, 1, 1)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(scale_factor, None)
        self.fusion_body.scale_by_factor(1, scale_factor.value, 1)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(scale_factor, None)
        self.fusion_body.scale_by_factor(1, 1, scale_factor.value)
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_body.scale_uniform(scale.value)
        return self

    def create_cube(
        self,
        width: DimensionOrItsFloatOrStringValue,
        length: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        width = Dimension.from_dimension_or_its_float_or_string_value(width, None)
        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        height = Dimension.from_dimension_or_its_float_or_string_value(height, None)

        sketch = FusionSketch(self.fusion_body.sketch.name)
        _ = make_rectangle(sketch.instance, width.value, length.value)
        self.fusion_body.instance = sketch.extrude(height.value)

        return self

    def create_cone(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        draft_radius: DimensionOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        height = Dimension.from_dimension_or_its_float_or_string_value(height, None)
        draft_radius = Dimension.from_dimension_or_its_float_or_string_value(draft_radius, None)

        if draft_radius == Dimension(0):
            import math

            points = [
                make_point3d(0, 0, 0),
                make_point3d(0, 0, height.value),
                make_point3d(radius.value, 0, 0),
                make_point3d(0, 0, 0),
            ]

            _ = make_lines(self.fusion_body.sketch, points)
            self.fusion_body.instance = make_revolve(
                self.fusion_body.component,
                self.fusion_body.sketch,
                math.pi * 2,
                make_point3d(0, 0, 0),
                make_point3d(0, 0, radius.value)
            )
        else:
            base = Sketch(self.fusion_body.sketch.name + "_temp_base")
            _ = base.create_circle(radius)

            top = Sketch(self.fusion_body.sketch.name + "_temp_top")
            _ = top.create_circle(draft_radius)
            top.translate_z(height.value)

            self.fusion_body.instance = make_loft(
                self.fusion_body.component,
                base.fusion_sketch.instance,
                top.fusion_sketch.instance
            )

            delete_occurrence(base.fusion_sketch.instance.name)
            delete_occurrence(top.fusion_sketch.instance.name)

        return self

    def create_cylinder(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        height = Dimension.from_dimension_or_its_float_or_string_value(height, None)

        sketch = FusionSketch(self.fusion_body.sketch.name)
        _ = make_circle(sketch.instance, radius.value, 4)
        self.fusion_body.instance = sketch.extrude(height.value)

        return self

    def create_torus(
        self,
        inner_radius: DimensionOrItsFloatOrStringValue,
        outer_radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch
        import math

        inner_radius = Dimension.from_dimension_or_its_float_or_string_value(
            inner_radius
        )
        outer_radius = Dimension.from_dimension_or_its_float_or_string_value(
            outer_radius
        )

        sketch = Sketch(self.fusion_body.sketch.name).fusion_sketch.instance

        circles = sketch.sketchCurves.sketchCircles
        _ = circles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), inner_radius.value
        )

        self.fusion_body.instance = make_revolve(
            self.fusion_body.component,
            sketch,
            math.pi * 2,
            "x",
            start=make_point3d(-inner_radius.value, -outer_radius.value, 0),
            end=make_point3d(inner_radius.value, -outer_radius.value, 0),
        )

        return self

    def create_sphere(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch
        import math

        radius = Dimension.from_dimension_or_its_float_or_string_value(
            radius
        )

        start = make_point3d(radius.value, 0, 0)
        end = make_point3d(-radius.value, 0, 0)

        sketch = Sketch(self.fusion_body.sketch.name)

        make_arc(sketch.fusion_sketch.instance, start, end, radius.value, True)

        self.fusion_body.instance = make_revolve(
            self.fusion_body.component,
            sketch.fusion_sketch.instance,
            math.pi * 2,
            start=make_point3d(0, 0, 0),
            end=end,
        )

        return self

    def create_gear(
        self,
        outer_radius: DimensionOrItsFloatOrStringValue,
        addendum: DimensionOrItsFloatOrStringValue,
        inner_radius: DimensionOrItsFloatOrStringValue,
        dedendum: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        pressure_angle: AngleOrItsFloatOrStringValue = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: AngleOrItsFloatOrStringValue = 0,
        conical_angle: AngleOrItsFloatOrStringValue = 0,
        crown_angle: AngleOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        print(
            "create_gear called:",
            outer_radius,
            addendum,
            inner_radius,
            dedendum,
            height,
            pressure_angle,
            number_of_teeth,
            skew_angle,
            conical_angle,
            crown_angle,
            keyword_arguments,
        )
        return self

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Part":
        body, sketch = self.fusion_body.clone(new_name, copy_landmarks)
        part = Part(body.name)
        part.fusion_body.instance = body
        part.fusion_body.sketch = sketch
        return part

    def union(
        self,
        with_part: PartOrItsName,
        delete_after_union: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        combine(self.fusion_body.instance, with_part.fusion_body.instance, delete_after_union)
        return self

    def subtract(
        self,
        with_part: PartOrItsName,
        delete_after_subtract: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        subtract(self.fusion_body.instance, with_part.fusion_body.instance, delete_after_subtract)
        return self

    def intersect(
        self,
        with_part: PartOrItsName,
        delete_after_intersect: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        intersect(self.fusion_body.instance, with_part.fusion_body.instance, delete_after_intersect)
        return self

    def hollow(
        self,
        thickness_x: DimensionOrItsFloatOrStringValue,
        thickness_y: DimensionOrItsFloatOrStringValue,
        thickness_z: DimensionOrItsFloatOrStringValue,
        start_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
    ):
        hollow(
            self.fusion_body.component,
            self.fusion_body.instance,
            thickness_x
        )
        return self

    def thicken(self, radius: DimensionOrItsFloatOrStringValue):
        print("thicken called:", radius)
        return self

    def hole(
        self,
        hole_landmark: LandmarkOrItsName,
        radius: DimensionOrItsFloatOrStringValue,
        depth: DimensionOrItsFloatOrStringValue,
        normal_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
        initial_rotation_x: AngleOrItsFloatOrStringValue = 0.0,
        initial_rotation_y: AngleOrItsFloatOrStringValue = 0.0,
        initial_rotation_z: AngleOrItsFloatOrStringValue = 0.0,
        mirror_about_entity_or_landmark: Optional[EntityOrItsName] = None,
        mirror_axis: AxisOrItsIndexOrItsName = "x",
        mirror: bool = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: AngleOrItsFloatOrStringValue = 0.0,
        circular_pattern_instance_axis: AxisOrItsIndexOrItsName = "z",
        circular_pattern_about_entity_or_landmark: Optional[EntityOrItsName] = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: DimensionOrItsFloatOrStringValue = 0.0,
        linear_pattern_instance_axis: AxisOrItsIndexOrItsName = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: DimensionOrItsFloatOrStringValue = 0.0,
        linear_pattern2nd_instance_axis: AxisOrItsIndexOrItsName = "y",
    ):
        from . import Sketch
        if isinstance(hole_landmark, str):
            component = get_component(hole_landmark)
            if get_body(component, hole_landmark):
                hole_landmark = Part(hole_landmark).fusion_body
            else:
                hole_landmark = Sketch(hole_landmark).fusion_sketch



        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        depth = Dimension.from_dimension_or_its_float_or_string_value(depth, None)

        point = hole_landmark.center

        hole(
            self.fusion_body.component,
            self.fusion_body.instance,
            point,
            radius.value,
            depth.value,
        )
        return self

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        iterations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    def set_material(self, material_name: MaterialOrItsName):
        set_material(self.fusion_body, material_name)
        return self

    def is_colliding_with_part(self, other_part: PartOrItsName) -> bool:
        print("is_colliding_with_part called:", other_part)
        return True

    def fillet_all_edges(
        self, radius: DimensionOrItsFloatOrStringValue, use_width: bool = False
    ):
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        fillet_all_edges(
            self.fusion_body.component,
            self.fusion_body.instance,
            radius.value,
        )
        return self

    def fillet_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
        use_width: bool = False,
    ):
        print("fillet_edges called:", radius, landmarks_near_edges, use_width)
        return self

    def fillet_faces(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_faces: list[LandmarkOrItsName],
        use_width: bool = False,
    ):
        print("fillet_faces called:", radius, landmarks_near_faces, use_width)
        return self

    def chamfer_all_edges(self, radius: DimensionOrItsFloatOrStringValue):
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        chamfer_all_edges(
            self.fusion_body.component,
            self.fusion_body.instance,
            radius.value
        )
        return self

    def chamfer_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
    ):
        return self

    def chamfer_faces(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_faces: list[LandmarkOrItsName],
    ):
        print("chamfer_faces called:", radius, landmarks_near_faces)
        return self

    def select_vertex_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        print("select_vertex_near_landmark called:", landmark_name)
        return self

    def select_edge_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        print("select_edge_near_landmark called:", landmark_name)
        return self

    def select_face_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        print("select_face_near_landmark called:", landmark_name)
        return self
