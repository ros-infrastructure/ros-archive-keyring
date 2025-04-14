VERSION 0.8

dpkgbuild:
  FROM debian:bookworm
  RUN apt-get update
  RUN apt-get install -y debhelper lintian
  # This is needed to correctly populate the Suites entry in sources
  RUN apt-get install -y lsb-release

ros-archive-keyring:
  FROM +dpkgbuild
  RUN mkdir /tmp/pkg
  WORKDIR /tmp/pkg
  COPY README .
  COPY debian debian
  COPY keys keys
  RUN dpkg-buildpackage -us -uc
  # Supressing package-installs-apt-preferences,package-installs-apt-sources warnings since it's permited for keyring packages
  # See https://wiki.debian.org/DebianRepository/UseThirdParty#Certificate_rollover_and_updates
  RUN lintian 
  SAVE ARTIFACT ../*.deb AS LOCAL output/

CHECK:
  FUNCTION
  ARG package
  FROM ubuntu:noble
  ARG DEBIAN_FRONTEND=noninteractive
  RUN apt update
  COPY +ros-archive-keyring/${package}*.deb ./
  RUN dpkg -i *.deb
  RUN apt update
  RUN apt install -y ros-jazzy-desktop

testpkg-main-repos:
  DO +CHECK --package=ros-archive-keyring
testpkg-testing-repos: 
  DO +CHECK --package=ros-testing-archive-keyring