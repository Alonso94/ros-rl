FROM ros:kinetic

#Turtlebot
RUN . /opt/ros/kinetic/setup.sh && apt-get update && apt-get install -y ros-kinetic-turtlebot #ros-kinetic-turtlebot-apps ros-kinetic-turtlebot-interactions ros-kinetic-turtlebot-simulator ros-kinetic-kobuki-ftdi ros-kinetic-ar-track-alvar-msgs

#Utils
RUN apt-get update && apt-get install -y vim net-tools iputils-ping

#Controllers for Crumb
RUN apt-get update && apt-get install -y ros-kinetic-gazebo-ros-control ros-kinetic-position-controllers ros-kinetic-effort-controllers ros-kinetic-joint-state-controller

#Crumb installing

ADD . /RLProject
#RUN cd RLProject && python get-pip.py
#RUN pip install msgpack
RUN . /opt/ros/kinetic/setup.sh && cd RLProject && cd kinetic && ls && catkin_make


#XVFB

RUN apt-get update && \
apt-get install -q -y \
xvfb


#Reinstalling Gazebo

RUN apt-get remove -y gazebo7
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
RUN apt-get update && apt-get install -y wget && wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - && \
apt-get update && \
apt-get install -y gazebo7 \
libgazebo7-dev \
ros-kinetic-gazebo-ros-pkgs \
ros-kinetic-gazebo-ros-control


#Anaconda

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean


#Theano and Lasagne

RUN . /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    conda create -y -n py27 python=2.7 && \
    pip install --upgrade pip && \
    pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git && \
    pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip && \
    pip install gym && \
    pip install opencv-python && \
    pip install rospkg 

RUN . /opt/conda/etc/profile.d/conda.sh && \
    conda activate py27 && \
    pip install rospkg && \
    pip install defusedxml && \
    pip install numpy && \
    pip install msgpack

RUN cd /opt/ros/kinetic/lib/python2.7/dist-packages/ && rm cv2.so

COPY entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]
CMD ["bash"]



