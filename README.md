# voice_cloning

### Speech training data: 
https://www.caito.de/2019/01/03/the-m-ailabs-speech-dataset/

### Used projects:
* https://github.com/CorentinJ/Real-Time-Voice-Cloning
* https://github.com/padmalcom/Real-Time-Voice-Cloning-German


### Installation:

Execute the `install_voice_cloning.sh` script. Adapt 

### Manual installation:
```bash
conda env create --file linux_64_environment.yml -n voice_cloning
conda activate voice_cloning
# adapt to cuda or rocm versio, see https://pytorch.org/ or for
# previous versions see https://pytorch.org/get-started/previous-versions/
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
```

### Update environment file (linux):
```bash
conda env export --no-builds -n voice_cloning > linux_64_environment.yml
```


