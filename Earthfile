VERSION 0.8

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
  RUN dpkg-buildpackage -us -uc
  RUN lintian --suppress-tags empty-binary-package
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
  RUN apt-get install -y ros-jazzy-desktop

testpkg-main-repos:
  DO +CHECK --package=ros-archive-keyring
testpkg-testing-repos: 
  DO +CHECK --package=ros-testing-archive-keyring