# ros-rl

# Requirements

1. ros-kinetic, gazebo7

2. Crumb pkg

3. OpenAI Gym, environments for crumb learning - https://github.com/ermekaitygulov/gym-crumb

For fast start there is Dockerfile with all needed packages installed.

# Installation of CRUMB

1. Create workspapce (for example catkin_ws);

2. Gitclone into catkin_ws/src https://github.com/ermekaitygulov/Crumb; https://github.com/vanadiumlabs/arbotix_ros.git

3. Add to CmakeList:
```bash
add_compile_options(-std=c++11)
add_compile_options(-std=gnu++11)
```

4. Intall (sudo apt-get): ros-kinetic-position-controllers, ros-kinetic-effort-controllers, ros-kinetic-joint-state-controller, ros-kinetic-gazebo-ros-control;

Install (pip): rospkg, msgpack, defusedxml, empy

5. Build package with catkin_make (I had got message told me to use "find . -iname "*.xacro" | xargs sed -i 's#<\([/]\?\)\(if\|unless\|include\|arg\|property\|macro\|insert_block\)#<\1xacro:\2#g' /home/airan/kinetic/src/Crumb/crumb_description/urdf/crumb.xacro" and after using this command CRUMB had built)

If you have error: ‘setupClient’ is not a member of ‘gazebo’, change file catkin_ws/src/Crumb/crumb_listener/src/crumb_listener_gazebo.cpp : replace setupClient with gazebo::client::setup(_argc, _argv); add #include <gazebo/gazebo_client.hh>

6. There are some worlds in crumb_gazebo that uses camera. You should replace path in this file.world with path, in which you want to save the images.


# TRPOAgent

TRPOAgent is a class based on Turtlebot class from gazebo-planner (https://github.com/cog-isa/gazebo-planner). Now the only workable agent is AgentSynth. Work with AgentImg is in progress.
