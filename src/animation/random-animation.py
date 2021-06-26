import os
import glob
import secrets
import runpy

script = os.path.realpath(__file__)
os.chdir(os.path.dirname(script))

animations = glob.glob('*.py')
animations.remove(os.path.basename(script))  # remove this script
animations.remove('all-off.py')
random_script = secrets.choice(animations)
print(random_script)
runpy.run_path(path_name=random_script)