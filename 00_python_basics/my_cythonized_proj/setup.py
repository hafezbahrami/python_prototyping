"""setup.py"""

import os
from pathlib import Path
import shutil
import stat

from setuptools import setup
from setuptools.command.build_py import build_py as build_py_original
from Cython.Build import cythonize
from Cython.Distutils import build_ext


project_path = Path(__file__).parent


class build_py(build_py_original):
    def build_packages(self):
        pass


# https://bugs.python.org/issue35893
# https://github.com/python/cpython/blame/af46450bb97ab9bd38748e75aa849c29fdd70028/Lib/distutils/command/build_ext.py#L686
def get_export_symbols(self, ext):
    parts = ext.name.split(".")
    if parts[-1] == "__init__":
        initfunc_name = "PyInit_" + parts[-2]
    else:
        initfunc_name = "PyInit_" + parts[-1]
    if initfunc_name not in ext.export_symbols:
        ext.export_symbols.append(initfunc_name)
    return ext.export_symbols


build_ext.get_export_symbols = get_export_symbols


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def remove_dirs_and_files(rm_dist=False):
    remove_dirs = []
    remove_dirs = [Path(project_path, "build")]
    remove_dirs += [str(f) for f in Path(project_path, "src").glob("**/*.exp")]
    remove_dirs += [str(f) for f in Path(project_path, "src").glob("**/*.pyd")]
    remove_dirs += [str(f) for f in Path(project_path, "src").glob("**/*.lib")]
    remove_dirs += [str(f) for f in Path(project_path, "src").glob("**/*.so")]
    if rm_dist:
        remove_dirs += [str(f) for f in Path(project_path).glob("*{0}".format("dist"))]
    remove_dirs += [str(f) for f in Path(project_path).glob("*{0}".format("egg-info"))]

    for d in remove_dirs:
        if os.path.isdir(d):
            shutil.rmtree(d, onerror=on_rm_error)
        elif os.path.isfile(d):
            os.remove(d)


remove_dirs_and_files(True)

FILES_TO_CYTHONIZE = [str(i) for i in list(Path("src").glob("my_cythonized_package/**/*.py"))]

"""
Please use semantic versioning (https://semver.org/)
MAJOR.MINOR.PATCH-rc.PRERELEASE+build.BUILD
Increment criteria:
    MAJOR - when you make incompatible API changes
    MINOR - when you add functionality in a backwards compatible manner
    PATCH - when you make backwards compatible bug fixes
    PRELEASE - release candidates
    BUILD - (do not use)
"""

setup(
    ext_modules=cythonize(
        FILES_TO_CYTHONIZE,
        build_dir="build",
        compiler_directives=dict(always_allow_keywords=True, language_level="3"),
    ),
    cmdclass={"build_ext": build_ext, "build_py": build_py},
)

remove_dirs_and_files(False)
