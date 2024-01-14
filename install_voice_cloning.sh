#!/bin/bash

conda -V 2&> /dev/null
ret=$?
if [ $ret -eq 0 ]; then
  echo "Installing voice_cloning ..."
  eval "$(conda shell.bash hook)"
  conda update -n base -c conda-forge conda -y
  conda env create --file linux_64_environment.yml -n voice_cloning
  conda activate voice_cloning
  # adapt to own CUDA or ROCM version, see https://pytorch.org/ or for
  # previous versions see https://pytorch.org/get-started/previous-versions/
#  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
  pip3 install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/rocm5.4.2
#  pip3 install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/rocm5.4.2
else
  echo "voice_cloning installation failed."
fi
