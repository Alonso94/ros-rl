#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/RLProject/kinetic/src/arbotix_ros/arbotix_sensors"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/RLProject/kinetic/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/RLProject/kinetic/install/lib/python2.7/dist-packages:/RLProject/kinetic/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/RLProject/kinetic/build" \
    "/usr/bin/python" \
    "/RLProject/kinetic/src/arbotix_ros/arbotix_sensors/setup.py" \
    build --build-base "/RLProject/kinetic/build/arbotix_ros/arbotix_sensors" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/RLProject/kinetic/install" --install-scripts="/RLProject/kinetic/install/bin"
