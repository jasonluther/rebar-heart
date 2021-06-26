from string import Template

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
ExecStart=/usr/bin/python3 $installdir/src/animation/$bin.py

[Install]
WantedBy=multi-user.target
''')

installdir = "/home/pi/rebar-heart"
animations = ["heartbeat", "pendulum", "rainbow", "twinkle", "all-off", "random-animation"]
conflicts = " ".join(f'heart-{i}.service' for i in animations)

for a in animations:
    servicefile = f'heart-{a}.service'
    f = open(f'tmp/{servicefile}', "w")
    c = conflicts.replace(servicefile, '')
    c = c.replace('  ', ' ')
    f.write(unit_template.substitute(
        installdir=installdir, bin=a, conflicts=c))
    f.close()
