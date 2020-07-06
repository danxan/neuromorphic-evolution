#!/bin/sh

# NEST is installed here. When you relocate NEST, change this variable.
export NEST_INSTALL_DIR=/home/dansan/nest2.20

# NEST finds standard *.sli files $NEST_DATA_DIR/sli
export NEST_DATA_DIR=$NEST_INSTALL_DIR/share/nest

# NEST finds help files $NEST_DOC_DIR/help
export NEST_DOC_DIR=$NEST_INSTALL_DIR/share/doc/nest

# The path where NEST looks for user modules.
export NEST_MODULE_PATH=$NEST_INSTALL_DIR/lib/nest

# The path where the PyNEST bindings are installed.
export NEST_PYTHON_PREFIX=$NEST_INSTALL_DIR/lib/python3.7/site-packages

# Prepend NEST to PYTHONPATH in a safe way even if PYTHONPATH is undefined
export PYTHONPATH=$NEST_PYTHON_PREFIX${PYTHONPATH:+:$PYTHONPATH}

# Make nest / sli /... executables visible.
export PATH=$NEST_INSTALL_DIR/bin:$PATH
