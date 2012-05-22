# For relative directories
import os
here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

PROJECT_ROOT = here()
config_path = lambda *x: os.path.join(here("config"), *x)

