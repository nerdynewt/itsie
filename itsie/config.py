import os
import sys
from configurator import Config

cdir = str(os.path.dirname(os.path.realpath(sys.argv[0])))

config = Config({
    'mysql': False,
    'locations': {
        '/etc/itsie.yaml',
        '~/.itsie/config.yaml',
        '~/.config/itsie/config.yaml',
        '~/AppData/Local/Programs/magna/itsie.yaml',
        },
    })

config.location = ""

for dirs in config.locations:
    config = config + Config.from_path(dirs, optional=True)


for dirs in config.locations:
    dirs = os.path.expanduser(dirs)
    if os.path.exists(dirs):
        config.location = dirs
        break

