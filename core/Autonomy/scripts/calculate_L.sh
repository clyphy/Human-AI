#!/bin/bash
L=$(echo "0.5*0.9 + 0.3*0.8 + 0.2*0.7" | bc -l)
printf "L=%.2f\n" "$L"
