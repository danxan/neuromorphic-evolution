# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/dansan/neuromorphic/source/snn/librandom/librandom.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/sli:/home/dansan/neuromorphic/source/snn/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librandom.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/binomial_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/clipped_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/exp_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/gamma_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/gsl_binomial_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/gslrandomgen.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/knuthlfg.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/librandom_exceptions.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/librandom_names.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/lognormal_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/mt19937.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/normal_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/poisson_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/random.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/random_datums.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/random_numbers.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/randomgen.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/uniform_randomdev.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/librandom/uniformint_randomdev.h"
    )
endif()

