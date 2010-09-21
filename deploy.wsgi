import sys
from os.path import abspath, dirname, join

# path to applications
ROOT_PATH = abspath(join(dirname(__file__), "../"))

# activate the python environment
activate_this = join(ROOT_PATH,'tweetfeed-env','Scripts','activate_this.py') # change this to the correct environment path
execfile(activate_this, dict(__file__=activate_this))

# add tweetfeed to the python path
sys.path.insert(0, ROOT_PATH)

# start the WSGI application
from tweetfeed.tweetfeedapp import app as application