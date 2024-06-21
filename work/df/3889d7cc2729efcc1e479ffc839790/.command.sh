#!/bin/bash -ue
./bigWigToBedGraph ${bw_files[0]} ${fname}_FWD.temp.bg
./bigWigToBedGraph ${bw_files[1]} ${fname}_REV.temp.bg
