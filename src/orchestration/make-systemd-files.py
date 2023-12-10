from string import Template
import os
import sys
script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
install_dir = os.path.join(script_path, '../..')
tmp_dir = os.path.join(script_path, 'tmp')
os.makedirs(tmp_dir, exist_ok=True)
print(f"Installation directory: {install_dir}")

unit_template = Template('''
[Unit]
Description=Heart Animation: $bin
After=multi-user.target
Conflicts=$conflicts

[Service]
Type=simple
Restart=no
User=root
Group=root
ExecStart=/usr/bin/python3 $install_dir/src/animation/$bin.py

[Install]
WantedBy=multi-user.target
''')

animations = ["heartbeat", "heartbeat-orange", "heartbeat-blue", "pendulum", "pendulum-orange", "pendulum-blue", "rainbow", "twinkle", "all-off", "random-animation"]
conflicts = " ".join(f'heart-{i}.service' for i in animations)

for a in animations:
    servicefile = f'heart-{a}.service'
    f = open(f'tmp/{servicefile}', "w")
    c = conflicts.replace(servicefile, '')
    c = c.replace('  ', ' ')
    f.write(unit_template.substitute(
        install_dir=install_dir, bin=a, conflicts=c))
    f.close()
