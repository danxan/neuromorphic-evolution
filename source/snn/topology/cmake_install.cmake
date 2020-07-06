# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/dansan/neuromorphic/source/snn/topology/libtopology.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/nestkernel:/home/dansan/neuromorphic/source/snn/librandom:/home/dansan/neuromorphic/source/snn/sli:/home/dansan/neuromorphic/source/snn/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtopology.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nest/sli" TYPE FILE FILES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/sli/topology-interface.sli")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/topology/unittests" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_distance.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_circ_anchor_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_circ_anchor_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_circ_anchor_10.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_circ_anchor_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_donut_anchor_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_donut_anchor_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_donut_anchor_10.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_donut_anchor_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_rect_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_rect_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_rect_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_free_mask_rect_13.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_oversize_mask.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_circ_anchor_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_circ_anchor_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_circ_anchor_10.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_circ_anchor_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_donut_anchor_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_donut_anchor_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_donut_anchor_10.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_donut_anchor_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_02.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_03.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_04.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_05.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_06.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_10.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_13.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_grid_anchor_15.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_rect_00.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_rect_01.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_rect_02.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_rect_10.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_reg_mask_rect_11.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_rows_cols_pos.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_weight_delay.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/unittests/test_weight_delay_free.sli"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/topology/mpitests" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/mpitests/ticket-516.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/mpitests/topo_mpi_test_convergent.sli"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/testsuite/mpitests/topo_mpi_test_divergent.sli"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/topologymodule.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/topology_names.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/connection_creator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/connection_creator_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/generic_factory.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/position.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/layer.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/layer_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/free_layer.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/grid_layer.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/mask.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/mask_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/grid_mask.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/ntree.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/ntree_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/vose.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/topology_parameter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/selector.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/topology.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(
    COMMAND /home/dansan/neuromorphic/source/snn/necoenv/bin/python setup.py build --build-base=/home/dansan/neuromorphic/source/snn/topology/build
                               install --prefix=/home/dansan/nest2.20
                                       --install-lib=/home/dansan/nest2.20/lib/python3.7/site-packages
                                       --install-scripts=/home/dansan/nest2.20/bin
                                       --install-data=/home/dansan/nest2.20/share/nest
    WORKING_DIRECTORY "/home/dansan/neuromorphic/source/snn/topology")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/doc/nest/examples/topology" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/README"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/conncomp.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/conncon_sources.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/conncon_targets.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/connex.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/connex_ew.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/ctx_2n.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/gaussex.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/grid_iaf.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/grid_iaf_irr.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/grid_iaf_oc.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/hill_tononi_Vp.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/test_3d.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/test_3d_exp.py"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/topology/examples/test_3d_gauss.py"
    )
endif()

