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

# Utility rule file for install-nodoc.

# Include the progress variables for this target.
include CMakeFiles/install-nodoc.dir/progress.make

CMakeFiles/install-nodoc:
	make NEST_INSTALL_NODOC=true install

install-nodoc: CMakeFiles/install-nodoc
install-nodoc: CMakeFiles/install-nodoc.dir/build.make

.PHONY : install-nodoc

# Rule to build all files generated by this target.
CMakeFiles/install-nodoc.dir/build: install-nodoc

.PHONY : CMakeFiles/install-nodoc.dir/build

CMakeFiles/install-nodoc.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/install-nodoc.dir/cmake_clean.cmake
.PHONY : CMakeFiles/install-nodoc.dir/clean

CMakeFiles/install-nodoc.dir/depend:
	cd /home/dansan/neuromorphic/source/snn && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0 /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0 /home/dansan/neuromorphic/source/snn /home/dansan/neuromorphic/source/snn /home/dansan/neuromorphic/source/snn/CMakeFiles/install-nodoc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/install-nodoc.dir/depend

