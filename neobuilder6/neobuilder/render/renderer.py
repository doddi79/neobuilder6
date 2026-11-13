__all__ = [
    'TemplateRenderer',
]
from batutils.structs import Singleton
import jinja2
import os
from importlib import resources

import logging
log = logging.getLogger(__name__)

def _get_resource_path():
    return str(resources.files('neobuilder6').joinpath('data'))


class TemplateRenderer(metaclass=Singleton):
    def __init__(self):
        self.template_dir = os.path.join(_get_resource_path(), 'templates')

        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=self.template_dir
            ),
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=jinja2.ChainableUndefined
        )

    def render_file(self, template_name: str, **kwargs) -> str:
        try:
            # log.debug(f'Rendering {template_name} with: {kwargs!r}')

            template = self._env.get_template(f'{template_name}.jinja2')
            return template.render(**kwargs)
        except Exception as ex:
            log.exception(f'Error in template: {template_name}: {ex!r}')
            raise ex
