import os
import sys
import importlib.util

sys.path.insert(0, os.path.dirname(__file__))

spec = importlib.util.spec_from_file_location('app', 'app.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
application = app.app
