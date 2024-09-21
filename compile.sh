#!/bin/bash

# will compile the runner.sh script and the Virus.sh script
# shc Usage: shc [-e date] [-m addr] [-i iopt] [-x cmnd] [-l lopt] [-o outfile] [-rvDSUHCABh] -f script
rm -rf build
mkdir -p build

echo "Compiling runner.sh and Virus.sh"
shc -f runner.sh -o build/runner
shc -f Virus.sh -o build/Virus

rm ./*.x.c
echo "Done"