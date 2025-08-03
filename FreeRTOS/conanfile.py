from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools.files import copy, load
import os

class FreeRTOSConan(ConanFile):
    name            = "freertos"

    license         = "MIT"
    url             = "https://github.com/FreeRTOS/FreeRTOS-Kernel"
    description     = "Real-Time Operating System for embedded devices."
    topics          = ("rtos", "freertos", "embedded")

    settings        = "os", "arch", "compiler", "build_type"
    package_type    = "header-library"

    exports_sources = "*"

    def set_version(self):
        self.version = load(
            self, os.path.join(self.recipe_folder, "version.txt")
        ).strip()
        
    def layout(self):
        cmake_layout(self)

    def package(self):
     # Kernel headers and source files
     src, dst = self.source_folder, self.package_folder

     # 1) Public headers
     for sub in ("include", "CMSIS_RTOS", "CMSIS_RTOS_V2", "portable/GCC"):
          copy(self, "*.h",
               src=os.path.join(src, sub),
               dst=os.path.join(dst, sub),
               keep_path=True)

     # 2) Ship .c files so the consumer can build an OBJECT library
     for sub in ("source", "portable/GCC", "portable/MemMang",
               "CMSIS_RTOS", "CMSIS_RTOS_V2"):
          copy(self, "*.c",
               src=os.path.join(src, sub),
               dst=os.path.join(dst, sub),
               keep_path=True)
     
    def package_info(self):
        self.cpp_info.libdirs = []            
        self.cpp_info.bindirs = []
        self.cpp_info.includedirs.append("include")