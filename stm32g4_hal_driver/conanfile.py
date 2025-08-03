import os
from conan import ConanFile
from conan.tools.files import copy, load


class STM32HAL(ConanFile):
    name = "stm32g4_hal_driver"
    license = "STMicroelectronics BSD-3-Clause"
    author = "Adam Paleczny"
    description = "STM32G4 HAL drivers (e.g., GPIO, UART, etc.)"
    settings = "os", "arch", "compiler", "build_type"
    package_type = "header-library"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    exports_sources = (
        "Src/**",
        "Inc/**",
        "Inc/Legacy/**",
        "version.txt",
    )

    def requirements(self):
        self.requires("cmsis/1.0.0")

    def set_version(self):
        self.version = load(
            self, os.path.join(self.recipe_folder, "version.txt")
        ).strip()

    def build(self):
        pass

    def package(self):
        src_root = self.source_folder

        copy(self, "*", src=os.path.join(src_root, "Src"), dst=os.path.join(self.package_folder, "src"), keep_path=True)
        copy(self, "*.h", src=os.path.join(src_root, "Inc"), dst=os.path.join(self.package_folder, "include"), keep_path=True)
        copy(self, "*.h", src=os.path.join(src_root, "Inc", "Legacy"), dst=os.path.join(self.package_folder, "include", "Legacy"), keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/Legacy"]
        self.cpp_info.srcdirs = ["src"]
        self.cpp_info.set_property("cmake_target_name", "stm32g4_hal_driver::stm32g4_hal_driver")
