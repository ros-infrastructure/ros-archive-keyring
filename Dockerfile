FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git dpkg-dev debhelper sudo

RUN git clone https://github.com/j-rivero/ros-keyring.git && cd ros-keyring && dpkg-buildpackage -us -uc
RUN cd .. && dpkg -i ros-keyring_2024.03.17_all.deb

RUN ls "/usr/share/keyrings"
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-ros2-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN apt-get update
RUN apt-get install -y ros-iron-desktop