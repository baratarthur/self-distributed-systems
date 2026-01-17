#!/bin/bash
echo "Generating proxy..."
python3 sds-proxy-generator
echo "Compiling Dana files..."
dnc .
echo "Compilation complete"