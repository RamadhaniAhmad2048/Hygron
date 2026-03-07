# GOON
# [1] START PROGRAM
print("[*] PROGRAM START")
print("PROGRAM GOON")
# [2] IMPORT LIBRARY
# [2.1] IMPORT BUILD-IN LIBRARY
import os
import pathlib
import re
import shutil
# [2.2] IMPORT EXTERNAL LIBRARY
try:
	import ffmpeg
	from PIL import Image
# [2.3] ERROR EXTERNAL MODULE NOT FOUND HANDLING
except ModuleNotFoundError:
	print("[!] External library not found, try \'pip install pillow ffmpeg\'")
# [3] DEFINE VARIABLE
# [3.1] CUSTOMIZABLE VARIABLE
DEFAULT_WORKING_PATH                = pathlib.Path('.')
DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION = 720
AUTO_RENAME_FILE                    = False
AUTO_DELETE_ORIGINAL                = False
AUTO_CREATE_PDF_PHOTO               = False
# [3.2] IMPORTANT VARIABLE
SCAN_PHOTO_FORMAT = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.afiv', '.bmp', '.tiff'}
SCAN_VIDEO_FORMAT = {'.mp4', '.mkv',  '.mov',  '.ts',  '.wmv',  '.m4v', '.avi',  '.flv'}
SCAN_ALL_FORMAT   = SCAN_PHOTO_FORMAT | SCAN_VIDEO_FORMAT
# [4] DEFINE FUNCTION
# [4.1] SCAN DIRECTORY WITH PATHLIB
def ScanDirectoryWithPathLib(ROOT_DIRECTORY):
	SCAN_RESULT = {}
	# [4.1.1] TRY SCAN ROOT DIRECTORY WITH PATHLIB
	try:
		for FILE in ROOT_DIRECTORY.rglob('*'):
			try:
				# [4.1.2] FILTER NO FILE IN PATH
				if not FILE.is_file():
					continue
				# [4.1.3] FILTER NOT IN CONTEXT FILE
				if not FILE.suffix.lower() in SCAN_ALL_FORMAT:
					continue
				# [4.1.4] INSERT FILE TO SCAN RESULT
				SCAN_RESULT.setdefault(FILE.parent, []).append(FILE)
			# [4.1.5] ERROR PERMISSION DENIED HANDLING
			except PermissionError:
				print("[!] File %s Permission Denied Error" % FILE[-64:])
	# [4.1.6] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] Root Directory Permission Denied Error")
	# [4.1.7] RETURN SCAN RESULT
	return SCAN_RESULT
# [4.2] GET PHOTO SHORT SIDE WITH PILLOW
def GetPhotoShortSideWithPillow(INPUT_FILE_PATH):
	# [4.2.1] TRY OPEN IMAGE FILE
	try:
		INPUT_FILE = Image.open(INPUT_FILE_PATH)
	# [4.2.2] ERROR FILE NOT FOUND HANDLING
	except FileNotFoundError:
		print("[!] File %s Not Found Error" % INPUT_FILE_PATH[-64:])
		return 'FileNotFoundError'
	# [4.2.3] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % INPUT_FILE_PATH[-64:])
		return 'PermissionError'
	# [4.2.4] TRY GET IMAGE RESOLUTION
	try:
		ORIGINAL_WIDTH, ORIGINAL_HEIGHT = INPUT_FILE.size
	except AttributeError:
		print("[!] File %s Size Attribute Error" % INPUT_FILE_PATH[-64:])
	# [4.2.5] TRY GET IMAGE SHORT SIDE
	INPUT_SHORT_RESOLUTION = min(ORIGINAL_WIDTH, ORIGINAL_HEIGHT)
	# [4.2.6] RETURN INPUT IMAGE SHORT RESOLUTION
	return INPUT_SHORT_RESOLUTION
# [4.3] GET VIDEO SHORT SIDE WITH FFMPEG
def GetVideoShortSideWithFFMPEG(INPUT_FILE_PATH):
	# [4.3.1] TRY OPEN VIDEO FILE
	try:
		PROBE_VIDEO = ffmpeg.probe(str(INPUT_FILE_PATH))
	# [4.3.2] ERROR FILE NOT FOUND HANDLING
	except FileNotFoundError:
		print("[!] File %s Not Found Error" % INPUT_FILE_PATH[-64:])
		return 'FileNotFoundError'
	# [4.3.3] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % INPUT_FILE_PATH[-64:])
		return 'PermissionError'
	# [4.3.4] ERROR INTERNAL FFMPEG HANDLING
	except ffmpeg.Error:
		print("[!] File %s FFMPEG Error" % INPUT_FILE_PATH[-64:])
		return 'FFMPEGError'
	# [4.3.5] TRY GET VIDEO RESOLUTION
	try:
		VIDEO_STREAM = None
		# [4.3.5] TRY GET VIDEO INFORMATION
		for STREAM in PROBE_VIDEO['streams']:
			if STREAM['codec_type'] == 'video':
				VIDEO_STREAM = STREAM
				break
		# [4.3.6] FILTER STREAM FILE
		if VIDEO_STREAM is None:
			return 'NoStreamError'
		# [4.3.7] GET VIDEO SHORT SIDE
		INPUT_SHORT_RESOLUTION = min(int(VIDEO_STREAM['width']), int(VIDEO_STREAM['height']))
		# [4.3.8] RETURN VIDEO SHORT SIDE
		return INPUT_SHORT_RESOLUTION
	# [4.3.9] ERROR INTERNAL FFMPEG HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % INPUT_FILE_PATH[-64:])
		return 'PermissionError'
	# [4.3.10] ERROR PERMISSION DENIED HANDLING
	except ffmpeg.Error:
		print("[!] File %s FFMPEG Error" % INPUT_FILE_PATH[-64:])
		return 'FFMPEGError'
# [4.4] CONVERT PHOTO WITH PILLOW
def ConvertPhotoWithPillow(INPUT_FILE_PATH, OUTPUT_FILE_PATH):
	pass
# [4.5] CONVERT VIDEO WITH FFMPEG
def ConvertVideoWithFFMPEG(INPUT_FILE_PATH, OUTPUT_FILE_PATH):
	pass
# [4.6] TEMPORARY LOGIC CONTROL
def TemporaryLogicControl():
	pass
# [4.7] CONVERT RESIZE RENAME LOGIC CONTROL
def ConvertAndResizeAndRenameLogicControl(SCAN_RESULT):
	pass
		
# [5] MAIN PROGRAM
# [5.1] MAIN PROGRAM FUNCTION
def Main():
	print("[*]")
# [5.2] MAIN PROGRAM TRIGGER
if __name__ == '__main__':
	Main()
# [6] FINISH PROGRAM
print("[*] PROGRAM EXIT")