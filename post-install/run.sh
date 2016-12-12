#!/bin/sh

cd /opt/metronome/post-install ;
cp /opt/metronome/post-install/metronome.service /usr/lib/systemd/system/ ;
mkdir -p /etc/metronome/certs ;
cp /opt/metronome/post-install/metronome.cfg /etc/metronome/metronome.cfg ;
chmod 751 /usr/lib/systemd/system/metronome.service ;
ln -s /usr/lib/systemd/system/metronome.service /etc/systemd/system/multi-user.target.wants/metronome.service ;
systemctl daemon-reload ;
systemctl enable metronome ;
systemctl start metronome ;
