import sys
from os.path import dirname, abspath

sys.path.append(abspath(dirname(__file__)))

from nyapics import app as application

application.configure()
