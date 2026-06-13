"""
Functional tests for the ctypes/comtypes wrappers.

Static type checkers can't validate ctypes declarations against the real C signatures.
These tests run headless: they need neither a display nor a real GPU,
but can't cover output duplication itself.
"""

from __future__ import annotations

import unittest

from d3dshot.dll.d3d import initialize_d3d_device
from d3dshot.dll.dxgi import (
    describe_dxgi_adapter,
    describe_dxgi_output,
    discover_dxgi_adapters,
    discover_dxgi_outputs,
    initialize_dxgi_factory,
)


class TestDXGI(unittest.TestCase):
    def test_initialize_dxgi_factory(self) -> None:
        dxgi_factory = initialize_dxgi_factory()
        self.assertTrue(dxgi_factory)

    def test_discover_and_describe_dxgi_adapters(self) -> None:
        dxgi_factory = initialize_dxgi_factory()
        dxgi_adapters = discover_dxgi_adapters(dxgi_factory)
        # At least the Microsoft Basic Render Driver should always be present
        self.assertTrue(dxgi_adapters)

        for dxgi_adapter in dxgi_adapters:
            description = describe_dxgi_adapter(dxgi_adapter)
            self.assertIsInstance(description, str)
            self.assertTrue(description)

    def test_discover_and_describe_dxgi_outputs(self) -> None:
        dxgi_factory = initialize_dxgi_factory()
        for dxgi_adapter in discover_dxgi_adapters(dxgi_factory):
            # Headless runners may have no attached output, so only validate shape
            for dxgi_output in discover_dxgi_outputs(dxgi_adapter):
                output_description = describe_dxgi_output(dxgi_output)
                self.assertTrue(output_description["name"])
                self.assertIn(output_description["rotation"], {0, 90, 180, 270})
                width, height = output_description["resolution"]
                self.assertGreaterEqual(width, 0)
                self.assertGreaterEqual(height, 0)
                self.assertIsInstance(output_description["is_attached_to_desktop"], bool)


class TestD3D(unittest.TestCase):
    def test_initialize_d3d_device(self) -> None:
        dxgi_factory = initialize_dxgi_factory()
        dxgi_adapters = discover_dxgi_adapters(dxgi_factory)
        self.assertTrue(dxgi_adapters)

        d3d_device, d3d_device_context = initialize_d3d_device(dxgi_adapters[0])
        self.assertTrue(d3d_device)
        self.assertTrue(d3d_device_context)


if __name__ == "__main__":
    unittest.main()
