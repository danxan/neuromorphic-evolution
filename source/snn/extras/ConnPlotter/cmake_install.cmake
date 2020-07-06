# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/extras/ConnPlotter

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/dansan/nest2.20")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(
  COMMAND /home/dansan/neuromorphic/source/snn/necoenv/bin/python setup.py build --build-base=/home/dansan/neuromorphic/source/snn/extras/ConnPlotter/build
                             install --prefix=/home/dansan/nest2.20
                                     --install-lib=/home/dansan/nest2.20/lib/python3.7/site-packages
                                     --install-scripts=/home/dansan/nest2.20/bin
                                     --install-data=/home/dansan/nest2.20/share/nest
    WORKING_DIRECTORY "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/extras/ConnPlotter")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/examples/ConnPlotter" TYPE FILE FILES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/extras/ConnPlotter/examples/connplotter_tutorial.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/ConnPlotter" TYPE FILE FILES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/extras/ConnPlotter/doc/connplotter_tutorial.pdf")
endif()

