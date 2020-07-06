# CMake generated Testfile for 
# Source directory: /home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests
# Build directory: /home/dansan/neuromorphic/source/snn/testsuite/selftests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(selftests/test_pass.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_pass.sli")
set_tests_properties(selftests/test_pass.sli PROPERTIES  _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;25;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_goodhandler.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_goodhandler.sli")
set_tests_properties(selftests/test_goodhandler.sli PROPERTIES  _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;25;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_lazyhandler.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_lazyhandler.sli")
set_tests_properties(selftests/test_lazyhandler.sli PROPERTIES  _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;25;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_fail.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_fail.sli")
set_tests_properties(selftests/test_fail.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;32;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_stop.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_stop.sli")
set_tests_properties(selftests/test_stop.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;32;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_badhandler.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_badhandler.sli")
set_tests_properties(selftests/test_badhandler.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;32;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_pass_or_die.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_pass_or_die.sli")
set_tests_properties(selftests/test_pass_or_die.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_assert_or_die_b.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_assert_or_die_b.sli")
set_tests_properties(selftests/test_assert_or_die_b.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_assert_or_die_p.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_assert_or_die_p.sli")
set_tests_properties(selftests/test_assert_or_die_p.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_fail_or_die.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_fail_or_die.sli")
set_tests_properties(selftests/test_fail_or_die.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_crash_or_die.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_crash_or_die.sli")
set_tests_properties(selftests/test_crash_or_die.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_failbutnocrash_or_die_crash.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_failbutnocrash_or_die_crash.sli")
set_tests_properties(selftests/test_failbutnocrash_or_die_crash.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_failbutnocrash_or_die_pass.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_failbutnocrash_or_die_pass.sli")
set_tests_properties(selftests/test_failbutnocrash_or_die_pass.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
add_test(selftests/test_passorfailbutnocrash_or_die.sli "/home/dansan/nest2.20/bin/nest" "/home/dansan/nest2.20/share/doc/nest/selftests/test_passorfailbutnocrash_or_die.sli")
set_tests_properties(selftests/test_passorfailbutnocrash_or_die.sli PROPERTIES  WILL_FAIL "TRUE" _BACKTRACE_TRIPLES "/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;41;add_test;/home/dansan/neuromorphic/source/snn/nest-simulator-2.20.0/testsuite/selftests/CMakeLists.txt;0;")
