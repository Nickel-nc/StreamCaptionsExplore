from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio
import torch

# importing libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

from glob import glob

class SpeechEngine():

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def remove_temp_chunks(self, folder_name):
        files = glob(f'{folder_name}/*')
        for f in files:
            os.remove(f)

    def wav2vec_model_init(self):
        # model_name = "facebook/wav2vec2-base-960h" # 360MB
        model_name = "facebook/wav2vec2-large-960h-lv60-self"  # 1.18GB
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)

    def get_transcription(self, audio_path):
        # load our wav file
        speech, sr = torchaudio.load(audio_path)
        speech = speech.squeeze()

        # resample from whatever the audio sampling rate to default rate
        resampler = torchaudio.transforms.Resample(sr, self.sample_rate)
        speech = resampler(speech)
        # tokenize our wav
        input_values = self.processor(
            speech,
            return_tensors="pt",
            sampling_rate=self.sample_rate)["input_values"]
        # perform inference
        logits = self.model(input_values)["logits"]
        # use argmax to get the predicted IDs
        predicted_ids = torch.argmax(logits, dim=-1)
        # decode the IDs to text
        transcription = self.processor.decode(predicted_ids[0])
        return transcription.lower()

    def wav2vec(self, audio_path):
        # self.get_chunks(audio_path)

        # open the audio file using pydub
        sound = AudioSegment.from_wav(audio_path)
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
                                  # experiment with this value for your target audio file
                                  min_silence_len=1000,
                                  # adjust this per requirement
                                  silence_thresh=sound.dBFS - 14,
                                  # keep the silence for 1 second, adjustable as well
                                  keep_silence=1000,
                                  )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk

            try:
                self.wav2vec_model_init()
                text = self.get_transcription(chunk_filename)

            except Exception as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

        self.remove_temp_chunks(folder_name)
        # return the text for all chunks detected
        return whole_text

        # self.wav2vec_model_init()
        # transcription = self.get_transcription(audio_path)
        # return transcription

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 1000,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=1000,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

    remove_temp_chunks(folder_name)
    # return the text for all chunks detected
    return whole_text

def remove_temp_chunks(folder_name):
    files = glob(f'{folder_name}/*')
    for f in files:
        os.remove(f)