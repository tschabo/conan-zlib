from conans import ConanFile, CMake, tools
import os


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Zlib here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports_sources = "*.zip", "*.patch"

    def source(self):
        tools.check_sha256("zlib1211.zip", "d7510a8ee1918b7d0cad197a089c0a2cd4d6df05fee22389f67f115e738b178d")
        tools.unzip("zlib1211.zip")
        os.remove("zlib1211.zip")
        if self.settings.os == "Windows" and self.settings.compiler.runtime in ["MD", "MDd"]:
            tools.patch(patch_file="static_rt.patch", base_path="zlib-1.2.11")

    def build(self):
        cmake = CMake(self, toolset=self.settings.compiler.toolset)
        cmake.configure(source_folder="zlib-1.2.11", build_folder="build", defs={"CMAKE_INSTALL_PREFIX" : self.install_folder + "/install"})
        cmake.build()
        cmake.install()

    def package(self):
        if self.options.shared:
            self.copy("lib/zlib.lib", src="install")
            self.copy("*.dll", src="install")
        else:
            self.copy("lib/zlibstatic.lib", src="install")
        self.copy("*.h", src="install")

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        if self.options.shared:
            self.cpp_info.libs = ["zlib"]  # The libs to link against
        else:
            self.cpp_info.libs = ["zlibshared"] # The libs to link against
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        
