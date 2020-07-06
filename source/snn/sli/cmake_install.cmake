# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/dansan/neuromorphic/source/snn/sli/libsli_readline.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/sli:/home/dansan/neuromorphic/source/snn/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli_readline.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/dansan/neuromorphic/source/snn/sli/libsli.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/libnestutil:::::::::::::::::::::::::"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsli.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/dansan/neuromorphic/source/snn/sli/sli")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/sli:/home/dansan/neuromorphic/source/snn/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/sli")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/allocator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/aggregatedatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/arraydatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/booldatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/callbackdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/charcode.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/datum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/dict.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/dictdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/dictstack.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/dictutils.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/doubledatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/fdstream.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/filesystem.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/functional.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/functiondatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/genericdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/integerdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/interpret.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/iostreamdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/iteratordatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/lockptrdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/lockptrdatum_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/name.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slinames.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/namedatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/numericdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/numericdatum_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/oosupport.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/parser.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/parserdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/processes.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/psignal.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/scanner.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/sli_io.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/sliactions.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/sliarray.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slibuiltins.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slicontrol.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slidata.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slidict.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/sliexceptions.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slifunction.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/sligraphics.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slimath.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slimodule.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/sliregexp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slistack.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slistartup.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slitype.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/slitypecheck.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/specialfunctionsmodule.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/stringdatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/symboldatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/tarrayobj.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/token.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/tokenarray.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/tokenstack.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/tokenutils.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/triedatum.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/typearray.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/typechk.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/utils.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/gnureadline.h"
    )
endif()

