VERSION 0.8

# list of supported platforms per https://www.ros.org/reps/rep-2000.html.
# This reflects supported platforms for humble, jazzy, kilted and rolling.
ARG --global supported_ros2_platforms = debian:bullseye debian:bookworm ubuntu:jammy ubuntu:noble

dpkgbuild:
  ARG distro = debian:bookworm
  FROM ${distro}
  RUN apt-get update
  RUN apt-get install -y debhelper lintian

INSTALL_PACKAGE: 
  FUNCTION
  ARG --required package_dir
  ARG --required package
  COPY ${package_dir}/${package}*.deb ./
  RUN ls
  RUN apt-get install ./${package}*.deb -y

BUILD_PACKAGE: 
  FUNCTION
  ARG package
  ARG target
  COPY ${package}/debian debian
  COPY ${package}/README .
  RUN dpkg-buildpackage
  RUN lintian 
  SAVE ARTIFACT ../*.deb AS LOCAL output/${target}/

build-ros-apt-source:
  ARG --required distro
  FROM +dpkgbuild --distro=${distro}
  RUN mkdir /tmp/pkg
  WORKDIR /tmp/pkg
  DO +BUILD_PACKAGE --package=ros-apt-source --target=${distro}

ros-archive-keyring:
  FROM +dpkgbuild
  RUN mkdir /tmp/pkg
  WORKDIR /tmp/pkg
  # add additional folders outside of standard debian packaging ones
  COPY ros-archive-keyring/keys keys
  DO +BUILD_PACKAGE --package=ros-archive-keyring

ros-apt-source:
  FROM debian:bookworm
  FOR distro IN $supported_ros2_platforms
        BUILD  +build-ros-apt-source --distro=${distro}
  END

test-keyring-pkg-install:
  # Test that keyring package can be installed and configures the keys appropiately
  ARG distro = ubuntu:noble
  FROM ${distro}
  LET install_key_path = /usr/share/keyrings/ros-archive-keyring.gpg
  DO +INSTALL_PACKAGE --package=ros-archive-keyring
  RUN if  [ -f ${install_key_path} ] && \ 
          [ -e ${install_key_path} ] && \ 
          [ -s ${install_key_path} \
  ]; then exit 0; else exit 1; fi;

test-aptsource-pkg-install:
  # Test that apt source package is installable and that it configures the necessary files
  ARG distro = ubuntu:noble
  FROM ${distro}
  DO +INSTALL_PACKAGE --package=ros-apt-source --package_dir=./output/${distro}
  RUN if  [ -f /etc/apt/sources.list.d/ros2.sources ] && \ 
          [ -e /etc/apt/sources.list.d/ros2.sources ] && \ 
          [ -s /etc/apt/sources.list.d/ros2.sources \
  ]; then exit 0; else exit 1; fi;
  RUN if  [ -f /etc/apt/preferences.d/ros2.pref ] && \ 
          [ -e /etc/apt/preferences.d/ros2.pref ] && \ 
          [ -s /etc/apt/preferences.d/ros2.pref \
  ]; then exit 0; else exit 1; fi;

integration-test-main-repos:
  # Test that repo configuration is complete when installing keyring and apt-source packages. 
  ARG distro = ubuntu:noble
  FROM ${distro}
  DO +INSTALL_PACKAGE --package=ros-archive-keyring --package_dir=./output
  DO +INSTALL_PACKAGE --package=ros-apt-source --package_dir=./output/${distro}
  RUN apt update
  RUN apt install ros-rolling-desktop -y
integration-test-testing-repos:
  ARG distro = ubuntu:noble
  FROM ${distro}
  DO +INSTALL_PACKAGE --package=ros-archive-keyring --package_dir=./output
  DO +INSTALL_PACKAGE --package=ros-testing-apt-source --package_dir=./output/${distro}
  RUN apt update
  RUN apt install ros-rolling-desktop -y

integration-check-switch: 
  # Test users are expected to be able to switch between the testing and main repositories seamlessly. 
  ARG distro = ubuntu:noble
  FROM ${distro}
  DO +INSTALL_PACKAGE --package=ros-archive-keyring --package_dir=./output
  DO +INSTALL_PACKAGE --package=ros-apt-source --package_dir=./output/${distro}
  RUN apt update
  RUN if  [ -f /etc/apt/sources.list.d/ros2.sources ] && \ 
          [ -e /etc/apt/sources.list.d/ros2.sources ] && \ 
          [ -s /etc/apt/sources.list.d/ros2.sources \
  ]; then exit 0; else exit 1; fi;
  RUN apt purge ros-apt-source -y
  RUN apt update
  DO +INSTALL_PACKAGE --package=ros-testing-apt-source --package_dir=./output/${distro}
  RUN if  [ -f /etc/apt/sources.list.d/ros2-testing.sources ] && \ 
          [ -e /etc/apt/sources.list.d/ros2-testing.sources ] && \ 
          [ -s /etc/apt/sources.list.d/ros2-testing.sources \
  ]; then exit 0; else exit 1; fi;
  RUN if  ! [ -f /etc/apt/sources.list.d/ros2.sources]; then exit 0; else exit 1; fi;
  RUN exit 1;
