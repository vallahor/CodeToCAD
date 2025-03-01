from codetocad import *
from .actions import clone_sketch
from .common import make_axis_vector, make_collection, make_matrix, make_vector
from .fusion_interface import FusionInterface
from .base import delete_occurrence, get_or_create_component, get_or_create_sketch

import adsk.core


class FusionSketch(FusionInterface):
    def __init__(self, name):
        self.component = get_or_create_component(name)
        self.instance = get_or_create_sketch(self.component, name)

    def translate(self, x: float, y: float, z: float):
        matrix = make_matrix()
        matrix.translation = make_vector(x, y, z)

        sketch = self.instance

        entities = make_collection()

        if len(sketch.sketchCurves.sketchLines) > 0:
            for line in sketch.sketchCurves.sketchLines:
                entities.add(line)

        if len(sketch.sketchCurves.sketchArcs) > 0:
            for line in sketch.sketchCurves.sketchArcs:
                entities.add(line)

        if len(sketch.sketchCurves.sketchConicCurves) > 0:
            for line in sketch.sketchCurves.sketchConicCurves:
                entities.add(line)

        if len(sketch.sketchCurves.sketchFittedSplines) > 0:
            for line in sketch.sketchCurves.sketchFittedSplines:
                entities.add(line)

        if len(sketch.sketchCurves.sketchFixedSplines) > 0:
            for line in sketch.sketchCurves.sketchFixedSplines:
                entities.add(line)

        if len(sketch.sketchTexts) > 0:
            for line in sketch.sketchTexts:
                entities.add(line)

        sketch.move(entities, matrix)

    def rotate(self, axis_input: AxisOrItsIndexOrItsName, angle: AngleOrItsFloatOrStringValue):
        sketch = self.instance

        axis = make_axis_vector(axis_input)
        angle = Angle.from_angle_or_its_float_or_string_value(angle).to_radians().value

        origin = self.center

        matrix = make_matrix()
        matrix.setToRotation(angle, axis, origin)

        entities = make_collection()

        if len(sketch.sketchCurves.sketchLines) > 0:
            for line in sketch.sketchCurves.sketchLines:
                entities.add(line)

        if len(sketch.sketchCurves.sketchArcs) > 0:
            for line in sketch.sketchCurves.sketchArcs:
                entities.add(line)

        if len(sketch.sketchCurves.sketchConicCurves) > 0:
            for line in sketch.sketchCurves.sketchConicCurves:
                entities.add(line)

        if len(sketch.sketchCurves.sketchFittedSplines) > 0:
            for line in sketch.sketchCurves.sketchFittedSplines:
                entities.add(line)

        if len(sketch.sketchCurves.sketchFixedSplines) > 0:
            for line in sketch.sketchCurves.sketchFixedSplines:
                entities.add(line)

        if len(sketch.sketchTexts) > 0:
            for line in sketch.sketchTexts:
                entities.add(line)

        sketch.move(entities, matrix)

    def scale(self, x: float, y: float, z: float):
        sketch = self.instance

        boundBox = sketch.boundingBox

        xFactor = 0
        yFactor = 0
        zFactor = 0

        if x > 0:
            if 0 > boundBox.minPoint.x < 1:
                xFactor = (abs(boundBox.minPoint.x) + x) * abs(boundBox.minPoint.x)
            else:
                xFactor =  abs(boundBox.minPoint.x) / (abs(boundBox.minPoint.x) + x)

        if y > 0:
            if 0 > boundBox.minPoint.y < 1:
                yFactor = (abs(boundBox.minPoint.y) + y) * abs(boundBox.minPoint.y)
            else:
                yFactor = abs(boundBox.minPoint.y) / (abs(boundBox.minPoint.y) + y)

        if z > 0:
            if 0 > boundBox.minPoint.z < 1:
                zFactor = (abs(boundBox.minPoint.z) + z) * abs(boundBox.minPoint.z)
            else:
                zFactor = abs(boundBox.minPoint.z) / (abs(boundBox.minPoint.z) + z)

        for point in sketch.sketchPoints:
            transform = adsk.core.Vector3D.create(
                point.geometry.x * xFactor, point.geometry.y * yFactor, point.geometry.z * zFactor)
            point.move(transform)

    def scale_by_factor(self, x: float, y: float, z: float):
        sketch = self.instance

        for point in sketch.sketchPoints:
            transform = adsk.core.Vector3D.create(
                point.geometry.x * (x / 2),
                point.geometry.y * (y / 2),
                point.geometry.z * (z / 2)
            )
            point.move(transform)

    def scale_uniform(self, scale: float):
        sketch = self.instance

        inputColl = adsk.core.ObjectCollection.create()
        inputColl.add(sketch)

        scaleFactor = adsk.core.ValueInput.createByReal(scale)
        basePt = sketch.sketchPoints.item(0)

        scales = self.component.features.scaleFeatures
        scaleInput = scales.createInput(inputColl, basePt, scaleFactor)

        scale = scales.add(scaleInput)

    def extrude(self, length: float) -> str:
        sketch = self.instance

        prof = sketch.profiles.item(0)
        extrudes = self.component.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(length)
        extInput.setDistanceExtent(False, distance)
        extInput.isSolid = True
        ext = extrudes.add(extInput)

        body = self.component.bRepBodies.item(self.component.bRepBodies.count - 1)
        body.name = self.instance.name

        return body

    def clone(self, new_name: str, copy_landmarks) -> adsk.fusion.Sketch:
        sketch = clone_sketch(self.instance, new_name, copy_landmarks)
        return sketch

    def rename(self, new_name: str):
        self.component.name = new_name
        self.instance.name = new_name

    def delete(self):
        delete_occurrence(self.component.name)

    @property
    def center(self):
        boundBox = self.instance.boundingBox

        center = adsk.core.Point3D.create(
            (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
            (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
            (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
        )

        return center

    def get_bounding_box(self):
        minPoint = self.instance.boundingBox.minPoint
        maxPoint = self.instance.boundingBox.maxPoint
        return BoundaryBox(
            BoundaryAxis(minPoint.x, maxPoint.x),
            BoundaryAxis(minPoint.y, maxPoint.y),
            BoundaryAxis(minPoint.z, maxPoint.z),
        )
