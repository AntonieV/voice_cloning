### source: https://github.com/padmalcom/Real-Time-Voice-Cloning-German
### own changes and adjustments marked with "# modified by AVI" in comment
#
#Copyright (c) padmalcom
#
# MIT License
# 
# Modified & original work Copyright (c) 2019 Corentin Jemine (https://github.com/CorentinJ)
# Original work Copyright (c) 2018 Rayhane Mama (https://github.com/Rayhane-mamah)
# Original work Copyright (c) 2019 fatchord (https://github.com/fatchord)
# Original work Copyright (c) 2015 braindead (https://github.com/braindead)
# 
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


import argparse
import os
import csv
from glob import glob
import codecs

if __name__ == "__main__":    
	parser = argparse.ArgumentParser(
		description="Create normlized text files for each audio file in mailabs datasets.",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument("--datasets_root", type=str, help="Path to the mailabs root directory (e.g. '/training_data/de_DE').")
	# overwrite
	# male, female, mix
	# audio format
	args = parser.parse_args()
	print(args.datasets_root)
	
	wav_folders = []
	
	print("Searching speakers...")

	# list female speakers
	speaker_search_dir_female = os.path.join(args.datasets_root, "by_book/female/*")  # modified by AVI
	female_speaker_dirs = glob(speaker_search_dir_female)
	print(female_speaker_dirs)
	
	# list male speakers
	speaker_search_dir_male = os.path.join(args.datasets_root, "by_book/male/*")  # modified by AVI
	male_speaker_dirs = glob(speaker_search_dir_male)
	
	# list mixed speakers
	speaker_search_dir_mix = os.path.join(args.datasets_root, "by_book/mix/*")  # modified by AVI
	mix_speaker_dirs = glob(speaker_search_dir_mix)
	
	all_speakers = female_speaker_dirs + male_speaker_dirs + mix_speaker_dirs
	print(all_speakers)
	
	# Check if speaker dirs have subfoders
	print("Checking subfolders...")
	for speaker in all_speakers:
		# get subfolders
		speaker_subfolders_search_dir = os.path.join(speaker, "*/")  # modified by AVI
		print(speaker_subfolders_search_dir)
		speaker_subfolders = glob(speaker_subfolders_search_dir)
		print(speaker_subfolders)
		
		# is subfolder a wavs dir?
		for speaker_subfolder in speaker_subfolders:
			last_folder = os.path.basename(os.path.normpath(speaker_subfolder))
			if last_folder == 'wavs':
				#print(speaker_subfolder + " is a wav folder")
				wav_folders.append(speaker_subfolder)
			else:
				# traverse further dirs
				speaker_subfolders_books_search_dir = os.path.join(speaker_subfolder, "*/")  # modified by AVI
				speaker_subfolders_books_dirs = glob(speaker_subfolders_books_search_dir)
				#print(speaker_subfolders_books_dirs)
				for speaker_subfolders_book in speaker_subfolders_books_dirs:
					last_folder = os.path.basename(os.path.normpath(speaker_subfolders_book))
					if last_folder == 'wavs':
						#print(speaker_subfolders_book + " is a wav folder")
						wav_folders.append(speaker_subfolders_book)					
						
	print("Found " + str(len(wav_folders)) + " wav folders")
	print(wav_folders)
	
	# read metadata.csv
	file_count = 0
	for wav_folder in wav_folders:
		wav_folder_parent = os.path.dirname(os.path.dirname(wav_folder))
		metadata_path = os.path.join(wav_folder_parent, "metadata.csv")
		if os.path.exists(metadata_path):
			with open(metadata_path, newline='', encoding='utf-8') as csvfile:
				csv_reader = csv.reader(csvfile, delimiter='|')
				for row in csv_reader:
					txt_file_to_create = os.path.join(wav_folder, row[0] + ".txt")
					if os.path.exists(txt_file_to_create):
						print(txt_file_to_create + " already exists.")
					else:
						expected_wav_file = os.path.join(wav_folder, row[0] + ".wav")
						if os.path.exists(expected_wav_file):
							if len(row) > 1:
								print("All good. Creating " + txt_file_to_create)
								f = codecs.open(txt_file_to_create, "w", "utf-8")
								f.write(row[1])
								f.close()
								file_count +=1
							else:
								print("Metadat is corrupt" + str(row))
						else:
							print("Corresponding wav file " + expected_wav_file + " was not found.")
		else:
			print("Expected file to exist: " + metadata_path)
	
	print("Wrote " + str(file_count) + " files.")
