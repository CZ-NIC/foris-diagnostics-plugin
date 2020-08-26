#!/usr/bin/env python

import copy

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildCmd(build_py):
    def run(self):
        # build foris plugin files
        from foris_plugins_distutils import build
        cmd = build(copy.copy(self.distribution))
        cmd.ensure_finalized()
        cmd.run()

        # build package
        build_py.run(self)


setup(
    name="Foris Diagnostics Plugin",
    version="12.2",
    description="Diagnostics plugin for foris web interfce",
    author="CZ.NIC, z. s. p. o.",
    author_email="packaging@turris.cz",
    url="https://gitlab.nic.cz/turris/foris/foris-diagnostics-plugin/",
    license="GPL-3.0-only",
    install_requires=[
        "foris @ git+https://gitlab.nic.cz/turris/foris/foris.git#egg=foris",
    ],
    setup_requires=[
        'babel',
        'jinja2',
        'libsass',
        'foris-plugins-distutils',
    ],
    provides=[
        "foris_plugins.diagnostics",
    ],
    packages=[
        "foris_plugins.diagnostics",
    ],
    package_data={
        '': [
            "templates/**",
            "templates/**/*",
            "templates/javascript/**",
            "templates/javascript/**/*",
            "locale/**/LC_MESSAGES/*.mo",
            "static/css/*.css",
            "static/fonts/*",
            "static/img/*",
            "static/js/*.js",
            "static/js/contrib/*",
        ],
    },
    namespace_packages=[
        'foris_plugins',
    ],
    dependency_links=[
        "git+https://gitlab.nic.cz/turris/foris/foris-plugins-distutils.git#egg=foris-plugins-distutils",
    ],
    cmdclass={
        "build_py": BuildCmd,  # modify build_py to build the foris files as well
    }
)
