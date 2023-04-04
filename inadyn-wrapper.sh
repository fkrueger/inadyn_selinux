#!/bin/sh

CMD="help"
if [ "x$1" != "x" ]; then
  [ "x$1" == "xstart" ] && CMD="start"
  [ "x$1" == "xstop" ] && CMD="stop"
  [ "x$1" == "x--help" ] && CMD="help"
  [ "x$1" == "x-h" ] && CMD="help"
  [ "x$1" == "xhelp" ] && CMD="help"
fi


[ -e "/etc/default/inadyn" ] && . /etc/default/inadyn

if [ "x$CMD" == "xhelp" ]; then
  echo ""
  echo "$0 <start|stop|help>"
  echo ""
  echo "    Starting/Stopping inadyn service (PIDFILE=$PIDFILE, USER=$USER, GROUP=$GROUP, OPTS=$OPTS)"
  echo ""
  exit -1
fi


if [ "x$CMD" == "xstart" ]; then
  # XXX we set pid-dir hard-coded here, despite allowing to be set differently in /etc/default/inadyn, for obvious security reasons.
  PIDDIR="/var/run/inadyn"

  if [ ! -d $PIDDIR ]; then
    /bin/mkdir -p $PIDDIR
    /bin/chown -Rf $USER:$GROUP $PIDDIR
    /bin/chmod 2775 $PIDDIR
  fi

  # XXX the following is needed because inadyn just happily keeps starting itself, even after realizing it cannot write its pidfile.. or after finding an old pidfile.
  TMPWC=`ps axufw | grep "^$USER.*/usr/bin/[i]nadyn" | grep -v grep | wc -l`
  if [ $TMPWC -gt 0 ]; then
    echo ". Killing superflous inadyn processes via pkill -9 /usr/bin/inadyn :"
    /bin/pkill -efu $USER -TERM /usr/bin/inadyn
    # XXX similar security reasons as above, for inadyn.pid
    /bin/rm -f $PIDDIR/inadyn.pid
  fi
  
  /bin/sudo -u $USER -- /usr/bin/inadyn $OPTS
fi


if [ "x$CMD" == "xstop" ]; then
  TMPPROCS=""
  PIDPROCS=""
  [ -e "$PIDFILE" ] && PIDPROCS=`cat $PIDFILE | xargs`
  [ "x$PIDPROCS" == "x" ] && TMPPROCS=`ps axufw | grep "^$USER.*/usr/bin/[i]nadyn" | grep -v grep | awk '{ print $1 }' | xargs`

  #echo "pidprocs '$PIDPROCS', tmpprocs '$TMPPROCS'"
  if [ "x$PIDPROCS" != "x" ]; then
    echo ". Killing pidfile process (PIDPROCS=$PIDPROCS):"
    /bin/kill -TERM $PIDPROCS
  fi

  if [ "x$TMPPROCS" != "x" ]; then
    echo ". Killing superflous processes (TMPPROCS=$TMPPROCS):"
    /bin/kill -TERM $TMPPROCS
  fi
fi

