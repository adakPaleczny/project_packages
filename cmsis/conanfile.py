import os
from conan import ConanFile
from conan.tools.files import copy, load

class CmsisHeaderOnly(ConanFile):
    name = "cmsis"
    package_type = "header-library"
    description = "CMSIS headers (Core, device, etc.)"
    license = "Apache-2.0"
    author = "Adam Paleczny"
    exports_sources = "Include/*"
    no_copy_source = True

    def set_version(self):
        self.version = load(
            self, os.path.join(self.recipe_folder, "version.txt")
        ).strip()

    def package(self):
        copy(self, pattern="*.h",
             dst=os.path.join(self.package_folder, "include"),
             src=os.path.join(self.source_folder, "Include"),
             keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.set_property("cmake_target_name", "cmsis")
        self.cpp_info.set_property("cmake_target_type", "interface")