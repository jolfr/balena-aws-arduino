diff /usr/src/app/arduino/analogToAWS.ino /data/analogToAWS.ino || PROGRAMMER=1
if [ "${PROGRAMMER:-}" == "1" ]
then
  echo $PROGRAMMER
  pushd /usr/src/app/arduino
  make upload && cp analogToAWS.ino /data/
  unset PROGRAMMER
  popd
fi
python -u main.py