# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.17

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/dansan/neuromorphic/source/snn

# Include any dependencies generated for this target.
include nest/CMakeFiles/nest_lib.dir/depend.make

# Include the progress variables for this target.
include nest/CMakeFiles/nest_lib.dir/progress.make

# Include the compile flags for this target's objects.
include nest/CMakeFiles/nest_lib.dir/flags.make

nest/CMakeFiles/nest_lib.dir/neststartup.cpp.o: nest/CMakeFiles/nest_lib.dir/flags.make
nest/CMakeFiles/nest_lib.dir/neststartup.cpp.o: nest-simulator-2.20.0/nest/neststartup.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/dansan/neuromorphic/source/snn/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object nest/CMakeFiles/nest_lib.dir/neststartup.cpp.o"
	cd /home/dansan/neuromorphic/source/snn/nest && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/nest_lib.dir/neststartup.cpp.o -c /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest/neststartup.cpp

nest/CMakeFiles/nest_lib.dir/neststartup.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/nest_lib.dir/neststartup.cpp.i"
	cd /home/dansan/neuromorphic/source/snn/nest && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest/neststartup.cpp > CMakeFiles/nest_lib.dir/neststartup.cpp.i

nest/CMakeFiles/nest_lib.dir/neststartup.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/nest_lib.dir/neststartup.cpp.s"
	cd /home/dansan/neuromorphic/source/snn/nest && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest/neststartup.cpp -o CMakeFiles/nest_lib.dir/neststartup.cpp.s

nest/CMakeFiles/nest_lib.dir/sli_neuron.cpp.o: nest/CMakeFiles/nest_lib.dir/flags.make
nest/CMakeFiles/nest_lib.dir/sli_neuron.cpp.o: nest-simulator-2.20.0/nest/sli_neuron.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/dansan/neuromorphic/source/snn/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object nest/CMakeFiles/nest_lib.dir/sli_neuron.cpp.o"
	cd /home/dansan/neuromorphic/source/snn/nest && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/nest_lib.dir/sli_neuron.cpp.o -c /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest/sli_neuron.cpp

nest/CMakeFiles/nest_lib.dir/sli_neuron.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/nest_lib.dir/sli_neuron.cpp.i"
	cd /home/dansan/neuromorphic/source/snn/nest && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest/sli_neuron.cpp > CMakeFiles/nest_lib.dir/sli_neuron.cpp.i

nest/CMakeFiles/nest_lib.dir/sli_neuron.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/nest_lib.dir/sli_neuron.cpp.s"
	cd /home/dansan/neuromorphic/source/snn/nest && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest/sli_neuron.cpp -o CMakeFiles/nest_lib.dir/sli_neuron.cpp.s

# Object files for target nest_lib
nest_lib_OBJECTS = \
"CMakeFiles/nest_lib.dir/neststartup.cpp.o" \
"CMakeFiles/nest_lib.dir/sli_neuron.cpp.o"

# External object files for target nest_lib
nest_lib_EXTERNAL_OBJECTS =

nest/libnest.so: nest/CMakeFiles/nest_lib.dir/neststartup.cpp.o
nest/libnest.so: nest/CMakeFiles/nest_lib.dir/sli_neuron.cpp.o
nest/libnest.so: nest/CMakeFiles/nest_lib.dir/build.make
nest/libnest.so: models/libmodels.so
nest/libnest.so: precise/libprecise.so
nest/libnest.so: topology/libtopology.so
nest/libnest.so: nestkernel/libnestkernel.so
nest/libnest.so: /lib/libltdl.so
nest/libnest.so: librandom/librandom.so
nest/libnest.so: sli/libsli.so
nest/libnest.so: libnestutil/libnestutil.so
nest/libnest.so: /usr/lib/libgsl.so
nest/libnest.so: /usr/lib/libgslcblas.so
nest/libnest.so: nest/CMakeFiles/nest_lib.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/dansan/neuromorphic/source/snn/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libnest.so"
	cd /home/dansan/neuromorphic/source/snn/nest && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/nest_lib.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
nest/CMakeFiles/nest_lib.dir/build: nest/libnest.so

.PHONY : nest/CMakeFiles/nest_lib.dir/build

nest/CMakeFiles/nest_lib.dir/clean:
	cd /home/dansan/neuromorphic/source/snn/nest && $(CMAKE_COMMAND) -P CMakeFiles/nest_lib.dir/cmake_clean.cmake
.PHONY : nest/CMakeFiles/nest_lib.dir/clean

nest/CMakeFiles/nest_lib.dir/depend:
	cd /home/dansan/neuromorphic/source/snn && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0 /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/nest /home/dansan/neuromorphic/source/snn /home/dansan/neuromorphic/source/snn/nest /home/dansan/neuromorphic/source/snn/nest/CMakeFiles/nest_lib.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : nest/CMakeFiles/nest_lib.dir/depend

