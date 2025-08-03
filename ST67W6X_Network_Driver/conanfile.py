import os
from conan import ConanFile
from conan.tools.files import copy, load


class STM32HAL(ConanFile):
    name = "st67w6x_network_driver"
    license = "STMicroelectronics BSD-3-Clause"
    author = "Adam Paleczny"
    description = "ST67W6X Network drivers (Bluetooth, Wi-Fi)"
    settings = "os", "arch", "compiler", "build_type"
    package_type = "header-library"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    exports_sources = (
        "Api/**",
        "Core/**",
        "Driver/W61_at/**",
        "Driver/W61_bus/**",
        "version.txt",
    )

    def set_version(self):
        self.version = load(
            self, os.path.join(self.recipe_folder, "version.txt")
        ).strip()

    def build(self):
        pass

    def package(self):
        src_root = self.source_folder

        copy(self, "*", src=os.path.join(src_root, "Api"), dst=os.path.join(self.package_folder, "Api"), keep_path=True)
        copy(self, "*", src=os.path.join(src_root, "Core"), dst=os.path.join(self.package_folder, "Core"), keep_path=True)
        copy(self, "*", src=os.path.join(src_root, "Driver/W61_at"), dst=os.path.join(self.package_folder, "Driver/W61_at"), keep_path=True)
        copy(self, "*", src=os.path.join(src_root, "Driver/W61_bus"), dst=os.path.join(self.package_folder, "Driver/W61_bus"), keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ["Api", "Core", "Driver/W61_at", "Driver/W61_bus"]
        self.cpp_info.srcdirs = ["Core", "Driver/W61_at", "Driver/W61_bus"]
        self.cpp_info.set_property("cmake_target_name", "st67w6x_network_driver::st67w6x_network_driver")
