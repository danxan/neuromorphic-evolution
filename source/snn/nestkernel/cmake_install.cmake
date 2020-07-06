# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/dansan/neuromorphic/source/snn/nestkernel/libnestkernel.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/librandom:/home/dansan/neuromorphic/source/snn/sli:/home/dansan/neuromorphic/source/snn/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libnestkernel.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/universal_data_logger_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/universal_data_logger.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/recordables_map.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/archiving_node.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/clopath_archiving_node.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/common_synapse_properties.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/completed_checker.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/sibling_container.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/subnet.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connection_label.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/common_properties_hom_w.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/syn_id_delay.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connector_base.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connector_base_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connector_model.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connector_model_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connection_id.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/device.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/device_node.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/dynamicloader.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/event.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/exceptions.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/genericmodel.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/genericmodel_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/gid_collection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/histentry.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/model.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/model_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/model_manager_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest_types.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest_datums.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest_names.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nestmodule.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest_time.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest_timeconverter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/modelrange.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/modelrange_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/multirange.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/node.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nodelist.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/proxynode.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/recording_device.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/pseudo_recording_device.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/ring_buffer.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/spikecounter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/stimulating_device.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/target_identifier.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/sparse_node_array.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/conn_parameter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/conn_builder.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/conn_builder_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/conn_builder_factory.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/music_event_handler.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/music_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/nest_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/synaptic_element.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/growth_curve.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/growth_curve_factory.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/kernel_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/vp_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/vp_manager_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/io_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/mpi_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/mpi_manager_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/simulation_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connection_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/connection_manager_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/sp_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/sp_manager_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/delay_checker.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/rng_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/event_delivery_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/event_delivery_manager_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/node_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/logging_manager.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/manager_interface.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/target_table.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/target_table_devices.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/target_table_devices_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/target.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/target_data.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/static_assert.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/send_buffer_position.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/source.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/source_table.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/source_table_position.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nestkernel/spike_data.h"
    )
endif()

