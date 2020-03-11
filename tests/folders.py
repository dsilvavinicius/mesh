import tempfile
from os.path import abspath, dirname, join

test_data_folder = abspath(join(dirname(__file__), '..', 'data', 'unittest'))

# folder used for creating temporary files
temporary_files_folder = tempfile.gettempdir()