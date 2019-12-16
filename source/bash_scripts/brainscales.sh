#!/bin/bash

ssh s2ext_daniesis@brainscales-r.kip.uni-heidelberg.de -p 11022 -X

export LC_ALL=C
module load nmpm_software/current

run_nmpm_software python -c "import pyhmf" && echo ok
