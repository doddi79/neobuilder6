from .renderer import TemplateRenderer
from typing import *


def to_file(file: str, content: str):
    with open(file, 'w', encoding='utf-8') as fout:
        fout.write(content)
        fout.write('\n')


def init() -> str:
    return TemplateRenderer().render_file('init')


def package_aliases(proto_package: str, dc_modules: List[Tuple[str, List[str]]]) -> str:
    """Renders the "proto package alias imports" for a Python package's
    `__init__.py` file, i.e. star imports of every dataclass module of every
    proto file in the given proto package, so that everything in a proto
    package can be imported from the corresponding Python package (e.g.
    `from myshop.orders import *`).
    """
    import logging
    log = logging.getLogger(__name__)

    dc_modules = sorted(dc_modules)
    names = []
    seen = {}
    for module_name, all_list in dc_modules:
        for name in all_list:
            if name in seen:
                log.warning(f'Name "{name}" in proto package "{proto_package}" found in both {seen[name]} '
                            f'and {module_name}... skipping the latter in __all__')
                continue
            seen[name] = module_name
            names.append(name)

    return TemplateRenderer().render_file('package_aliases',
                                          proto_package=proto_package,
                                          modules=[m for m, _ in dc_modules],
                                          names=names)


def root_init(package_name: str,
              version_str,
              alias_init: str = '') -> str:
    from protoplasm6 import __version__ as ppv
    from neobuilder6 import __version__ as nbv
    if isinstance(ppv, tuple):
        if len(ppv) > 3:
            ppv = '.'.join(str(i) for i in ppv[:3])
        else:
            ppv = '.'.join(str(i) for i in ppv)
    if isinstance(nbv, tuple):
        if len(nbv) > 3:
            nbv = '.'.join(str(i) for i in nbv[:3])
        else:
            nbv = '.'.join(str(i) for i in nbv)

    return TemplateRenderer().render_file('root_init',
                                          version=version_str,
                                          protoplasm_version=ppv,
                                          neobuilder_version=nbv,
                                          package_name=package_name,
                                          alias_init=alias_init)


