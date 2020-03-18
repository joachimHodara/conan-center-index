from conans import ConanFile, CMake, tools
import os


class CgnsConan(ConanFile):
    name = "cgns"
    description = "CGNS provides a standard for recording and recovering CFD data"
    topics = "conan", "cfd"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://cgns.github.io"
    license = "cgns"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "build_cgns_tools": [True, False],
               "build_testing": [True, False],
               "enable_64bit": [True, False],
               "enable_base_scope": [True, False],
               "enable_fortran": [True, False],
               "enable_hdf5": [True, False],
               "enable_legacy": [True, False],
               "enable_mem_debug": [True, False],
               "enable_scoping": [True, False],
               "enable_parallel": [True, False],
               "enable_tests": [True, False],
               "use_shared": [True, False],
               "hdf5_build_shared": [True, False],
               "hdf5_need_mpi": [True, False],
               "hdf5_need_zlib": [True, False],
               "hdf5_need_szip": [True, False]
               }
    default_options = {"shared": False,
                       "fPIC": True,
                       "build_cgns_tools": False,
                       "build_testing": False,
                       "enable_64bit": True,
                       "enable_base_scope": False,
                       "enable_fortran": False,
                       "enable_hdf5": True,
                       "enable_legacy": True,
                       "enable_mem_debug": False,
                       "enable_scoping": False,
                       "enable_parallel": False,
                       "enable_tests": True,
                       "use_shared": False,
                       "hdf5_build_shared": True,
                       "hdf5_need_mpi": False,
                       "hdf5_need_zlib": False,
                       "hdf5_need_szip": False
                       }

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.options.enable_hdf5:
            self.requires("hdf5/1.10.6")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version.replace('.', '_')
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CGNS_BUILD_CGNSTOOLS"] = self.options.build_cgns_tools
        cmake.definitions["CGNS_BUILD_SHARED"] = self.options.shared
        cmake.definitions["CGNS_BUILD_TESTING"] = self.options.build_testing
        cmake.definitions["CGNS_ENABLE_64BIT"] = self.options.enable_64bit
        cmake.definitions["CGNS_ENABLE_BASE_SCOPE"] = self.options.enable_base_scope
        cmake.definitions["CGNS_ENABLE_FORTRAN"] = self.options.enable_fortran
        cmake.definitions["CGNS_ENABLE_HDF5"] = self.options.enable_hdf5
        cmake.definitions["CGNS_ENABLE_LEGACY"] = self.options.enable_legacy
        cmake.definitions["CGNS_ENABLE_MEM_DEBUG"] = self.options.enable_mem_debug
        cmake.definitions["CGNS_ENABLE_PARALLEL"] = self.options.enable_parallel
        cmake.definitions["CGNS_ENABLE_SCOPING"] = self.options.enable_scoping
        cmake.definitions["CGNS_ENABLE_TESTS"] = self.options.enable_tests
        cmake.definitions["CGNS_USE_SHARED"] = self.options.use_shared
        cmake.definitions["HDF5_BUILD_SHARED_LIBS"] = self.options.hdf5_build_shared
        cmake.definitions["HDF5_NEED_MPI"] = self.options.hdf5_build_shared
        cmake.definitions["HDF5_NEED_ZLIB"] = self.options.hdf5_need_zlib
        cmake.definitions["HDF5_NEED_SZIP"] = self.options.hdf5_need_szip
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["cgns"]
