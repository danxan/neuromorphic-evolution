# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/doc

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
             COMMAND /home/dansan/neuromorphic/source/snn/necoenv/bin/python -B generate_help.py "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0" "/home/dansan/neuromorphic/source/snn"
             WORKING_DIRECTORY "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/extras/help_generator"
             )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dansan/nest2.20/share/doc/nest/help")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dansan/nest2.20/share/doc/nest" TYPE DIRECTORY OPTIONAL FILES "/home/dansan/neuromorphic/source/snn/doc/help")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(
             COMMAND /home/dansan/neuromorphic/source/snn/necoenv/bin/python -B generate_helpindex.py "/home/dansan/nest2.20/share/doc/nest"
             WORKING_DIRECTORY "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/extras/help_generator"
             )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest" TYPE DIRECTORY FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/doc/conngen"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/doc/model_details"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/doc/index.html"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/doc/quickref.html"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/doc/doc_header.txt"
    )
endif()

