#!/bin/bash

conda -V 2&> /dev/null
ret=$?
if [ $ret -eq 0 ]; then
  echo "Installing voice_cloning ..."
  eval "$(conda shell.bash hook)"
  conda update -n base -c conda-forge conda
  conda env create --file linux_64_environment.yml -n voice_cloning
  conda activate voice_cloning
  # adapt to own CUDA or ROCM version, see https://pytorch.org/ or for
  # previous versions see https://pytorch.org/get-started/previous-versions/
  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
else
  echo "voice_cloning installation failed."
fi
