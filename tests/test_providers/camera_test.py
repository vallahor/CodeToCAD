from .test_helper import *
from codetocad.tests_interfaces import CameraTestInterface


class CameraTest(TestProviderCase, CameraTestInterface):
    def test_create_perspective(self):
        instance = Camera("myCamera")

        value = instance.create_perspective()

        assert value.is_exists(), "Create method failed."

    def test_create_orthogonal(self):
        instance = Camera("myCamera")

        value = instance.create_orthogonal()

        assert value.is_exists(), "Create method failed."

    def test_set_focal_length(self):
        instance = Camera("myCamera")

        value = instance.set_focal_length(length=2)

        assert value, "Modify method failed."
