### source: https://github.com/padmalcom/Real-Time-Voice-Cloning-German
### own changes and adjustments marked with "# modified by AVI" in comment
#
#Copyright (c) padmalcom
#
# MIT License

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import torch
import sounddevice as sd
import time

if __name__ == '__main__':
    enc_model_fpath = Path("encoder/saved_models/mini_encoder_de/encoder.pt")
    syn_model_fpath = Path("synthesizer/saved_models/mini_synthesizer_de"
                           "/mini_synthesizer_de.pt")
    voc_model_fpath = Path("vocoder/saved_models/mini_vocoder_de/mini_vocoder_de.pt")

    if torch.cuda.is_available():
        device_id = torch.cuda.current_device()
        gpu_properties = torch.cuda.get_device_properties(device_id)
        print(
            "Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d "
            "with %.1fGb total memory.\n" %
            (torch.cuda.device_count(),
             device_id,
             gpu_properties.name,
             gpu_properties.major,
             gpu_properties.minor,
             gpu_properties.total_memory / 1e9))
    else:
        print("Using CPU for inference.\n")
    # Load the models one by one.
    print("Preparing the encoder, the synthesizer and the vocoder...")
    encoder.load_model(enc_model_fpath)
    synthesizer = Synthesizer(syn_model_fpath)
    vocoder.load_model(voc_model_fpath)

    in_path = 'tests/avi_Audiospur_095.wav'
    in_text = 'Das ist ein Test mit meiner eigenen Stimme.'
    out_path = './gen.wav'

    original_wav, sampling_rate = librosa.load(str(in_path))
    preprocessed_wav = encoder.preprocess_wav(original_wav, int(sampling_rate))

    embed = encoder.embed_utterance(preprocessed_wav)
    print("Created the embedding")

    texts = [in_text]
    embeds = [embed]
    #embeds = [[0] * 256]

    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]
    print("Created the mel spectrogram")

    griffin_lim = False
    if not griffin_lim:
        generated_wav = vocoder.infer_waveform(spec)
        generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate),
                               mode="constant")
        generated_wav = encoder.preprocess_wav(generated_wav)
    else:
        generated_wav = Synthesizer.griffin_lim(spec)

    write = True
    if write:
        sf.write(out_path, generated_wav.astype(np.float32),
                 round(synthesizer.sample_rate / 1.0))
        print("Audio file has been written.")

    audio_length = librosa.get_duration(y=generated_wav, sr=14545)
    sd.play(generated_wav.astype(float), round(synthesizer.sample_rate / 1.0))
    time.sleep(audio_length)
    sd.play(generated_wav.astype(float), round(synthesizer.sample_rate / 1.0))
    time.sleep(audio_length)
    print("Done")
