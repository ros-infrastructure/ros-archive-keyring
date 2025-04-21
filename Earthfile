VERSION 0.8


INSTALL_PACKAGE: 
  FUNCTION
  ARG package
  COPY +${package}/${package}*.deb ./
  RUN dpkg -i *.deb

dpkgbuild:
  FROM debian:bookworm
  RUN apt-get update
  RUN apt-get install -y debhelper lintian

ros-archive-keyring:
  FROM +dpkgbuild
  RUN mkdir /tmp/pkg
  WORKDIR /tmp/pkg
  COPY README .
  COPY debian debian
  COPY keys keys
  RUN dpkg-buildpackage
  RUN lintian 
  SAVE ARTIFACT ../*.deb AS LOCAL output/


test-keyring-pkg-install:
  # Test that keyring package can be installed and configures the keys appropiately
  FROM ubuntu:noble
  LET install_key_path = /usr/share/keyrings/ros-archive-keyring.gpg
  DO +INSTALL_PACKAGE --package=ros-archive-keyring
  RUN if  [ -f ${install_key_path} ] && \ 
          [ -e ${install_key_path} ] && \ 
          [ -s ${install_key_path} \
  ]; then exit 0; else exit 1; fi;
