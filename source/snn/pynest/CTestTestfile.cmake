# CMake generated Testfile for 
# Source directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/pynest
# Build directory: /home/dansan/neuromorphic/source/snn/pynest
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(PyNEST "/home/dansan/anaconda3/bin/nosetests" "-v" "--with-xunit" "--xunit-file=/home/dansan/neuromorphic/source/snn/reports/pynest_tests.xml" "/home/dansan/nest2.20/lib/python3.7/site-packages/nest/tests")
set_tests_properties(PyNEST PROPERTIES  _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/pynest/CMakeLists.txt;95;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/pynest/CMakeLists.txt;0;")
