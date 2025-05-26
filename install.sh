#!/usr/bin/env bash

KDIR="${HOME}/klipper"
KENV="${HOME}/klippy-env"
BKDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if [ ! -d "$KDIR" ] || [ ! -d "$KENV" ]; then
  echo "push_notify: klipper or klippy does not appear to exist"
  exit 1
fi

# Install required python libraries
echo "Installing python requirements into klippy-env"
"${KENV}/bin/pip" install -r "${BKDIR}/requirements.txt"

echo "linking klippy to push_notify scripts"
# Remove old symlinks if they exist
if [ -e "${KDIR}/klippy/extras/fcm.py" ]; then
  rm "${KDIR}/klippy/extras/fcm.py"
fi
if [ -e "${KDIR}/klippy/extras/notify.py" ]; then
  rm "${KDIR}/klippy/extras/notify.py"
fi
if [ -e "${KDIR}/klippy/extras/pushbullet.py" ]; then
  rm "${KDIR}/klippy/extras/pushbullet.py"
fi

# Create symlinks to our scripts
ln -s "${BKDIR}/scripts/fcm.py" "${KDIR}/klippy/extras/fcm.py"
ln -s "${BKDIR}/scripts/notify.py" "${KDIR}/klippy/extras/notify.py"
ln -s "${BKDIR}/scripts/pushbullet.py" "${KDIR}/klippy/extras/pushbullet.py"

echo "push_notify installed!"
