#!/bin/bash
# run this as the rhodecode user!

WDIR=/opt/red/conector
VIRTUALENV_DIR=/opt/red/

source $WDIR/bin/activate

cd $VIRTUALENV_DIR
python proxy.py > ./var.log
