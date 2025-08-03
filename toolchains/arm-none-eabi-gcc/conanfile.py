# toolchains/arm-none-eabi-gcc/conanfile.py
from conan import ConanFile
from conan.tools.files import get, copy, load
import os

class ArmGnuToolchain(ConanFile):
    name        = "arm-none-eabi-gcc"
    license     = "GPL‑3.0‑with‑exception"
    description = "Pre‑built GNU Arm Embedded bare‑metal tool‑chain"
    url         = "https://developer.arm.com/"
    settings    = "os", "arch"
    package_type = "application"                    # <<< the important change
    package_id_compatible_mode = True        # one binary works for any host

    def set_version(self):
        self.version = load(
            self, os.path.join(self.recipe_folder, "version.txt")
        ).strip()

    def build(self):
        get(self,
            url="https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz",
            sha256="6cd1bbc1d9ae57312bcd169ae283153a9572bd6a8e4eeae2fedfbc33b115fdbb",
            strip_root=True)

    def package(self):
        copy(self, "*", src=self.build_folder, dst=self.package_folder)

    # ------------------------------------------------------------------ #
    # Tell Conan *how* to call the compiler and where to find it.
    # ------------------------------------------------------------------ #
    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.buildenv_info.append_path("PATH", bin_path)

        self.conf_info.define("tools.build:compiler_executables", {
            "c"      : "arm-none-eabi-gcc",
            "cpp"    : "arm-none-eabi-g++",
            "asm"    : "arm-none-eabi-gcc",
            "ar"     : "arm-none-eabi-ar",
            "objcopy": "arm-none-eabi-objcopy",
            "objdump": "arm-none-eabi-objdump",
            "nm"     : "arm-none-eabi-nm",
            "ranlib" : "arm-none-eabi-ranlib",
            "strip"  : "arm-none-eabi-strip",
            "size"   : "arm-none-eabi-size",
        })

        common_flags = [
            "-mcpu=cortex-m7",
            "-mthumb",
            "-mfloat-abi=hard",
            "-mfpu=fpv5-d16",
            "-specs=nosys.specs"
        ]

        self.conf_info.define("tools.build:cflags", common_flags)
        self.conf_info.define("tools.build:cxxflags", common_flags + [
            "-fno-exceptions",
            "-fno-rtti"
        ])
        self.conf_info.define("tools.build:linkflags", [
            "-Wl,--gc-sections",
            "-Wl,--cref"
        ])

