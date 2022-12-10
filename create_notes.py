
# INPUT THE FILE NAME
"""
argument will be given before starting the code
the file name will be present in it
using that, we will decide the folder name of slides
# 'video.mp4'
"""
import argparse
import os
import cv2

from PIL import Image
from pprint import pprint
from natsort import natsorted


ap = argparse.ArgumentParser()
ap.add_argument('-i','--input',required=True)
args = vars(ap.parse_args())
print(args)

file = args['input']
folder = file[:-4]+'_Slides'

print(folder)

generate_frames = True
generate_pdf = True

# CREATE OUTPUT FOLDER WHERE WE CAN SAVE FILES
try:
	os.makedirs(folder)
	print("Folder Created Successfully!!")
except Exception as e:
	print(e)

# READ THE VIDEO FILE AND GENERATE FRAMES
if generate_frames:
	cap = cv2.VideoCapture(file)
	n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	print(f"# frames in the video {file} are {n_frames}")

	prev = None
	# 0 to n-1 - 0 to 8810
	for ctr in range(n_frames):
		ret, frame = cap.read()
		if not ret:
			break

		if prev is None:
			prev = frame
			continue

		if ctr%25:
			continue

		# SAVE FRAMES ONLY WHEN DIFFERENT FRAME IS THERE
		diff = sum(sum(sum(frame-prev)))
		print(diff)

		if diff>500:
			cv2.imshow('Output',frame)
			cv2.waitKey(1)

			slide_name = f'{ctr}_{folder}.jpg'.replace(' ','').replace('.\\','')
			slide_path = os.path.join(folder, slide_name)
			flag = cv2.imwrite(slide_path, frame)
			print(f"Frame: {ctr} Written: {flag}")
	print("Frames Generation is Done")	

# GENERATE THE PDF OF ALL THE IMAGES IN FOLDER
if generate_pdf:

	files = [os.path.join(folder,file) for file in os.listdir(folder)]
	files = natsorted(files)
	# Lexicographic way of sorting 

	images = [Image.open(f) for f in files]
	pdf_path = f'{folder}.pdf'
	
	images[0].save(
		pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
		)

	print("PDF Generation is Done")	

print("Program Finished Execution")