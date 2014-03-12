import sass

from django.contrib.staticfiles.finders import get_finders
from compressor.filters.base import FilterBase

class SassCompiler(FilterBase):
    """A SASS compiler that uses the python libsass binding."""
    def __init__(self, content, attrs=None, filter_type=None, charset=None, filename=None):
        super(SassCompiler, self).__init__(content, filter_type, filename)

    def get_include_paths(self):
        """SASSlib will need include paths as a param to know where to find
        files and imported sheets."""
        include_paths = []
        # Use Django to build the paths from the get_finders generator
        for storages in [f.storages for f in get_finders() if hasattr(f, 'storages')]:
            include_paths += [s.path('.') for s in storages.itervalues() if hasattr(s, 'path')]

        return include_paths

    def input(self, **kwargs):
        kwargs['include_paths'] = kwargs.get('include_paths', [])
        kwargs['include_paths'] += self.get_include_paths()

        if self.filename:
            kwargs['filename'] = self.filename
        else:
            kwargs['string'] = self.content

        return sass.compile(**kwargs)
