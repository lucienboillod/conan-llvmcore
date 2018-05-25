#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os, platform

class llvmConan(ConanFile):
    name = "llvm"
    version = "5.0.1"
    description = "Conan.io package for LLVM Core library."
    url = "https://github.com/lucienboillod/conan-llvmcore"
    license = "http://releases.llvm.org/2.8/LICENSE.TXT"
    exports = ["LICENSE.md"]
    source_dir = "{name}-{version}.src".format(name=name, version=version)
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {'shared': [True, False]}
    default_options = 'shared=False'
    short_paths = True

    def build_requirements(self):
        if platform.system() == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")

    def extractFromUrl(self, url, dest, name):
        self.output.info('download {}'.format(url))
        sources = os.path.basename(url).rsplit('.', 2)[0]
        tools.download(url, sources + '.tar.xz')
        if platform.system() != "Windows":
            cmd = "tar -xJf {sources}".format(sources=sources) + '.tar.xz -C ' + dest
            self.run(cmd)            
        else:
            cmd = "7z.exe e {sources}".format(sources=sources) + '.tar.xz'
            self.run(cmd)
            tools.unzip(sources + ".tar", dest)
            os.unlink(sources + ".tar")
        os.rename(dest + sources, dest + name)
        os.unlink(sources + '.tar.xz')

    def source(self):
        llvm = 'http://releases.llvm.org/' + self.version + '/llvm-' + self.version + '.src.tar.xz'
        self.extractFromUrl(llvm, './', self.source_dir)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.source_dir)):
            cmake = CMake(self)
            cmake.verbose = True
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
            cmake.definitions["LLVM_ENABLE_LIBCXX"] = "ON"
            cmake.definitions["LIBCXX_INCLUDE_TESTS"] = "OFF"
            cmake.definitions["LIBCXX_INCLUDE_DOCS"] = "OFF"
            cmake.definitions["LLVM_INCLUDE_TOOLS"] = "ON"
            cmake.definitions["LLVM_INCLUDE_TESTS"] = "OFF"
            cmake.definitions["LLVM_INCLUDE_EXAMPLES"] = "OFF"
            cmake.definitions["LLVM_INCLUDE_GO_TESTS"] = "OFF"
            cmake.definitions["LLVM_BUILD_TOOLS"] = "ON"
            cmake.definitions["LLVM_BUILD_TESTS"] = "OFF"
            cmake.configure(source_dir=os.path.join(self.source_folder, self.source_dir))
            cmake.build()
            cmake.install()

    def package(self):
        self.copy('*', dst='', src='install')
