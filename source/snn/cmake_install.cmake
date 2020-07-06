# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/LICENSE"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/README.md"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/dansan/neuromorphic/source/snn/doc/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/examples/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/extras/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/lib/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/libnestutil/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/librandom/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/models/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/sli/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/nest/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/nestkernel/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/precise/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/testsuite/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/topology/cmake_install.cmake")
  include("/home/dansan/neuromorphic/source/snn/pynest/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/dansan/neuromorphic/source/snn/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
