# Install script for directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models

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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so"
         RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/dansan/neuromorphic/source/snn/models/libmodels.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so"
         OLD_RPATH "/home/dansan/neuromorphic/source/snn/nestkernel:/home/dansan/neuromorphic/source/snn/librandom:/home/dansan/neuromorphic/source/snn/sli:/home/dansan/neuromorphic/source/snn/libnestutil:"
         NEW_RPATH "$ORIGIN/../lib:$ORIGIN/../lib/nest:$ORIGIN/../../..:$ORIGIN/../../../nest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmodels.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nest" TYPE FILE FILES
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/ac_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_cond_alpha.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_cond_alpha_RK5.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_cond_alpha_multisynapse.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_cond_beta_multisynapse.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_cond_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_psc_alpha.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_psc_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_psc_delta.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/aeif_psc_delta_clopath.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/amat2_psc_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/bernoulli_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/binary_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/clopath_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/cont_delay_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/cont_delay_connection_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/correlation_detector.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/correlomatrix_detector.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/correlospinmatrix_detector.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/dc_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/diffusion_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/erfc_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gamma_sup_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gap_junction.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gauss_rate.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gif_psc_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gif_psc_exp_multisynapse.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gif_cond_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gif_cond_exp_multisynapse.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/gif_pop_psc_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/ginzburg_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/glif_cond.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/glif_psc.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/hh_cond_exp_traub.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/hh_cond_beta_gap_traub.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/hh_psc_alpha.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/hh_psc_alpha_clopath.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/hh_psc_alpha_gap.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/ht_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/ht_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_chxk_2008.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_chs_2007.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_cond_alpha.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_cond_alpha_mc.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_cond_beta.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_cond_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_cond_exp_sfa_rr.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_psc_alpha.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_psc_alpha_multisynapse.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_psc_exp_multisynapse.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_psc_delta.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_psc_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/iaf_tum_2000.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/izhikevich.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/lin_rate.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/mat2_psc_exp.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/mcculloch_pitts_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/mip_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/modelsmodule.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/multimeter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/music_cont_in_proxy.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/music_cont_out_proxy.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/music_event_in_proxy.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/music_event_out_proxy.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/music_message_in_proxy.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/noise_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/parrot_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/inhomogeneous_poisson_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/poisson_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/pp_psc_delta.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/pp_pop_psc_delta.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/ppd_sup_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/pulsepacket_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/quantal_stp_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/quantal_stp_connection_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_connection_delayed.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_connection_instantaneous.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_neuron_opn.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_neuron_opn_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_neuron_ipn.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_neuron_ipn_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_transformer_node.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/rate_transformer_node_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/siegert_neuron.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/sigmoid_rate.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/sigmoid_rate_gg_1998.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/sinusoidal_poisson_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/sinusoidal_gamma_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/spike_detector.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/spike_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/spin_detector.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/static_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/static_connection_hom_w.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_nn_pre-centered_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_nn_restr_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_nn_symm_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_connection_facetshw_hom.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_connection_facetshw_hom_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_connection_hom.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_dopa_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_connection_facetshw_hom.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_connection_facetshw_hom_impl.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_pl_connection_hom.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/stdp_triplet_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/step_current_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/step_rate_generator.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/tanh_rate.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/threshold_lin_rate.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/tsodyks2_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/tsodyks_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/tsodyks_connection_hom.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/voltmeter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/volume_transmitter.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/vogels_sprekeler_connection.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/weight_recorder.h"
    "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/models/spike_dilutor.h"
    )
endif()

