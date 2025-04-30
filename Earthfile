VERSION 0.8

# list of supported platforms per https://www.ros.org/reps/rep-2000.html.
# This reflects supported platforms for humble, jazzy, kilted and rolling.
ARG --global supported_ros_platforms = ubuntu:jammy ubuntu:noble ubuntu:focal

dpkgbuild:
  ARG distro = debian:bookworm
  FROM ${distro}
  ENV DEBIAN_FRONTEND=noninteractive 
  ENV TZ=Etc/UTC 
  RUN apt-get update
  RUN apt-get install -y debhelper>=13 lintian 
INSTALL_PACKAGE: 
  FUNCTION
  ARG --required package_dir
  ARG --required package
  COPY ${package_dir}/${package}*.deb ./
  RUN apt-get install ./${package}*.deb -y

BUILD_PACKAGE: 
  FUNCTION
  ARG package
  ARG target
  COPY ${package}/debian debian
  RUN . /etc/os-release && sed -i "s:~\$CODENAME:~$VERSION_CODENAME:" debian/changelog 
  COPY ${package}/README .
  RUN dpkg-buildpackage 
  RUN lintian 
  SAVE ARTIFACT ../*.deb AS LOCAL output/${target}/

ros-apt-source:
  ARG --required distro
  FROM +dpkgbuild --distro=${distro}
  RUN mkdir /tmp/pkg
  WORKDIR /tmp/pkg
  # add additional folders outside of standard debian packaging ones
  COPY ros-apt-source/keys keys
  DO +BUILD_PACKAGE --package=ros-apt-source --target=${distro}

build-all:
  FROM debian:bookworm
  FOR distro IN $supported_ros_platforms
        BUILD  +ros-apt-source --distro=${distro} 
  END

test-aptsource-pkg-install:
  # Test that apt source package is installable and that it configures the necessary files
  ARG distro = ubuntu:noble
  ARG repo = ros2
  ARG version = ros2
  FROM ${distro}
  ENV DEBIAN_FRONTEND=noninteractive 
  ENV TZ=Etc/UTC 
  LET package = ${repo}-apt-source
  DO +INSTALL_PACKAGE --package=${package} --package_dir=./output/${distro}
  RUN echo ${repo}
  RUN if  [ -f /usr/share/ros-apt-source/${repo}.sources ] && \ 
          [ -e /usr/share/ros-apt-source/${repo}.sources ] && \ 
          [ -s /usr/share/ros-apt-source/${repo}.sources \
  ]; then exit 0; else exit 1; fi;
  # test that embbeded key is passed
  RUN if [ ${distro} != "ubuntu:focal" ]; then \
         cat /usr/share/ros-apt-source/${repo}.sources | grep 'BEGIN PGP PUBLIC KEY BLOCK'; \
        fi;
  RUN if  [ -f /usr/share/keyrings/${version}-archive-keyring.gpg ] && \ 
          [ -e /usr/share/keyrings/${version}-archive-keyring.gpg ] && \ 
          [ -s /usr/share/keyrings/${version}-archive-keyring.gpg \
  ]; then exit 0; else exit 1; fi; 

  RUN if  [ -h /etc/apt/sources.list.d/${version}.sources ]; then exit 0; else exit 1; fi;  

ros2-test-repos:
  # Test that repo configuration is complete when installing keyring and apt-source packages. 
  ARG distro = ubuntu:noble
  ARG package = ros2-apt-source

  FROM ${distro}
  ENV DEBIAN_FRONTEND=noninteractive 
  ENV TZ=Etc/UTC 
  DO +INSTALL_PACKAGE --package=${package} --package_dir=./output/${distro}
  RUN apt update
  RUN apt install ros-rolling-desktop -y

ros-test-repos:
  ARG distro = ubuntu:focal
  ARG package = ros-apt-source

  FROM ${distro}
  ENV DEBIAN_FRONTEND=noninteractive 
  ENV TZ=Etc/UTC 
  DO +INSTALL_PACKAGE --package=${package} --package_dir=./output/${distro}
  RUN apt update
  RUN apt install ros-noetic-desktop-full -y

integration-check-switch: 
  # Test users are expected to be able to switch between the testing and main repositories seamlessly. 
  ARG distro = ubuntu:noble
  ARG repo = ros2
  FROM ${distro}
  LET main_repo_regex = "packages.ros.org/"${repo}"/"
  LET testing_repo_regex = "packages.ros.org/"${repo}"-testing/"
  DO +INSTALL_PACKAGE --package=${repo}-apt-source --package_dir=./output/${distro}
  RUN apt update
  RUN apt policy | grep $main_repo_regex
  RUN apt remove ${repo}-apt-source -y
  RUN apt update
  DO +INSTALL_PACKAGE --package=${repo}-testing-apt-source --package_dir=./output/${distro}
  RUN apt update  
  RUN apt policy | grep $testing_repo_regex
  # Verify that main repo is not configured anymore
  # trailing / is important here to avoid matching ros2*
  RUN if ! apt policy | grep $main_repo_regex; then exit 0; else exit 1; fi;
