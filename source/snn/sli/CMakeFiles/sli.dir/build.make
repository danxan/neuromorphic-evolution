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
include sli/CMakeFiles/sli.dir/depend.make

# Include the progress variables for this target.
include sli/CMakeFiles/sli.dir/progress.make

# Include the compile flags for this target's objects.
include sli/CMakeFiles/sli.dir/flags.make

sli/CMakeFiles/sli.dir/puresli.cc.o: sli/CMakeFiles/sli.dir/flags.make
sli/CMakeFiles/sli.dir/puresli.cc.o: nest-simulator-2.20.0/sli/puresli.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/dansan/neuromorphic/source/snn/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object sli/CMakeFiles/sli.dir/puresli.cc.o"
	cd /home/dansan/neuromorphic/source/snn/sli && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/sli.dir/puresli.cc.o -c /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/puresli.cc

sli/CMakeFiles/sli.dir/puresli.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/sli.dir/puresli.cc.i"
	cd /home/dansan/neuromorphic/source/snn/sli && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/puresli.cc > CMakeFiles/sli.dir/puresli.cc.i

sli/CMakeFiles/sli.dir/puresli.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/sli.dir/puresli.cc.s"
	cd /home/dansan/neuromorphic/source/snn/sli && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli/puresli.cc -o CMakeFiles/sli.dir/puresli.cc.s

# Object files for target sli
sli_OBJECTS = \
"CMakeFiles/sli.dir/puresli.cc.o"

# External object files for target sli
sli_EXTERNAL_OBJECTS =

sli/sli: sli/CMakeFiles/sli.dir/puresli.cc.o
sli/sli: sli/CMakeFiles/sli.dir/build.make
sli/sli: sli/libsli_readline.so
sli/sli: /usr/lib/libgsl.so
sli/sli: /usr/lib/libgslcblas.so
sli/sli: sli/libsli.so
sli/sli: libnestutil/libnestutil.so
sli/sli: /usr/lib/libgsl.so
sli/sli: /usr/lib/libgslcblas.so
sli/sli: /lib/libreadline.so
sli/sli: /lib/libncurses.so
sli/sli: sli/CMakeFiles/sli.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/dansan/neuromorphic/source/snn/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable sli"
	cd /home/dansan/neuromorphic/source/snn/sli && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sli.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
sli/CMakeFiles/sli.dir/build: sli/sli

.PHONY : sli/CMakeFiles/sli.dir/build

sli/CMakeFiles/sli.dir/clean:
	cd /home/dansan/neuromorphic/source/snn/sli && $(CMAKE_COMMAND) -P CMakeFiles/sli.dir/cmake_clean.cmake
.PHONY : sli/CMakeFiles/sli.dir/clean

sli/CMakeFiles/sli.dir/depend:
	cd /home/dansan/neuromorphic/source/snn && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0 /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/sli /home/dansan/neuromorphic/source/snn /home/dansan/neuromorphic/source/snn/sli /home/dansan/neuromorphic/source/snn/sli/CMakeFiles/sli.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : sli/CMakeFiles/sli.dir/depend

