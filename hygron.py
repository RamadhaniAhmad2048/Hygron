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
				print("[!] File %s Permission Denied Error" % str(FILE)[-64:])
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
		print("[!] File %s Not Found Error" % str(INPUT_FILE_PATH)[-64:])
		return 'FileNotFoundError'
	# [4.2.3] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % str(INPUT_FILE_PATH)[-64:])
		return 'PermissionError'
	# [4.2.4] TRY GET IMAGE RESOLUTION
	try:
		ORIGINAL_WIDTH, ORIGINAL_HEIGHT = INPUT_FILE.size
	except AttributeError:
		print("[!] File %s Size Attribute Error" % str(INPUT_FILE_PATH)[-64:])
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
		print("[!] File %s Not Found Error" % str(INPUT_FILE_PATH)[-64:])
		return 'FileNotFoundError'
	# [4.3.3] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % str(INPUT_FILE_PATH)[-64:])
		return 'PermissionError'
	# [4.3.4] ERROR INTERNAL FFMPEG HANDLING
	except ffmpeg.Error:
		print("[!] File %s FFMPEG Error" % str(INPUT_FILE_PATH)[-64:])
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
		print("[!] File %s Permission Denied Error" % str(INPUT_FILE_PATH)[-64:])
		return 'PermissionError'
	# [4.3.10] ERROR PERMISSION DENIED HANDLING
	except ffmpeg.Error:
		print("[!] File %s FFMPEG Error" % str(INPUT_FILE_PATH)[-64:])
		return 'FFMPEGError'
# [4.4] CONVERT PHOTO WITH PILLOW
def ConvertPhotoWithPillow(INPUT_FILE_PATH, OUTPUT_FILE_PATH):
	# [4.4.1] TRY OPEN IMAGE FILE
	try:
		INPUT_FILE = Image.open(INPUT_FILE_PATH)
	# [4.4.2] ERROR FILE NOT FOUND HANDLING
	except FileNotFoundError:
		print("[!] File %s Not Found Error" % str(INPUT_FILE_PATH)[-64:])
		return 'FileNotFoundError'
	# [4.4.3] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % str(INPUT_FILE_PATH)[-64:])
		return 'PermissionError'
	# [4.4.4] TRY RESIZE AND CONVERT IMAGE
	try:
		ORIGINAL_WIDTH, ORIGINAL_HEIGHT = INPUT_FILE.size
		# [4.4.5] CALCULATE NEW RESOLUTION KEEP ASPECT RATIO
		if ORIGINAL_WIDTH < ORIGINAL_HEIGHT:
			NEW_WIDTH  = DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
			NEW_HEIGHT = int(ORIGINAL_HEIGHT * DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION / ORIGINAL_WIDTH)
		else:
			NEW_HEIGHT = DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
			NEW_WIDTH  = int(ORIGINAL_WIDTH * DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION / ORIGINAL_HEIGHT)
		# [4.4.6] RESIZE IMAGE
		OUTPUT_FILE = INPUT_FILE.resize((NEW_WIDTH, NEW_HEIGHT), Image.LANCZOS)
		# [4.4.7] CONVERT IMAGE MODE FOR JPG COMPATIBILITY
		if OUTPUT_FILE_PATH.suffix.lower() in {'.jpg', '.jpeg'} and OUTPUT_FILE.mode in ('RGBA', 'P'):
			OUTPUT_FILE = OUTPUT_FILE.convert('RGB')
		# [4.4.8] SAVE OUTPUT IMAGE
		OUTPUT_FILE.save(OUTPUT_FILE_PATH)
		return 'Success'
	# [4.4.9] ERROR ATTRIBUTE HANDLING
	except AttributeError:
		print("[!] File %s Attribute Error" % str(INPUT_FILE_PATH)[-64:])
		return 'AttributeError'
	# [4.4.10] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % str(OUTPUT_FILE_PATH)[-64:])
		return 'PermissionError'
# [4.5] CONVERT VIDEO WITH FFMPEG
def ConvertVideoWithFFMPEG(INPUT_FILE_PATH, OUTPUT_FILE_PATH):
	# [4.5.1] TRY CONVERT AND RESIZE VIDEO
	try:
		# [4.5.2] BUILD FFMPEG SCALE FILTER KEEP ASPECT RATIO
		# scale=-2:720 = short side 720, nilai -2 agar dimensi tetap genap (divisible by 2)
		SCALE_FILTER = "scale=-2:%d" % DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
		# [4.5.3] RUN FFMPEG CONVERSION
		(
			ffmpeg
			.input(str(INPUT_FILE_PATH))
			.output(
				str(OUTPUT_FILE_PATH),
				vf=SCALE_FILTER,
				vcodec='libx264',
				acodec='aac',
				crf=23,
			)
			.overwrite_output()
			.run(quiet=True)
		)
		return 'Success'
	# [4.5.4] ERROR FILE NOT FOUND HANDLING
	except FileNotFoundError:
		print("[!] File %s Not Found Error" % str(INPUT_FILE_PATH)[-64:])
		return 'FileNotFoundError'
	# [4.5.5] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % str(INPUT_FILE_PATH)[-64:])
		return 'PermissionError'
	# [4.5.6] ERROR INTERNAL FFMPEG HANDLING
	except ffmpeg.Error as ERROR:
		STDERR_MSG = ERROR.stderr.decode('utf-8', errors='replace') if ERROR.stderr else 'No detail'
		print("[!] File %s FFMPEG Error: %s" % (str(INPUT_FILE_PATH)[-64:], STDERR_MSG[-256:]))
		return 'FFMPEGError'
# [4.6] TEMPORARY LOGIC CONTROL
def TemporaryLogicControl():
	pass
# [4.7] CONVERT RESIZE RENAME LOGIC CONTROL
def ConvertAndResizeAndRenameLogicControl(SCAN_RESULT):
	# [4.7.1] LOOP EACH DIRECTORY IN SCAN RESULT
	for DIRECTORY, FILES in SCAN_RESULT.items():
		print("[*] Directory: %s" % DIRECTORY)
		# [4.7.2] LOOP EACH FILE IN DIRECTORY
		for FILE in FILES:
			FILE_SUFFIX = FILE.suffix.lower()
			# [4.7.3] GET SHORT SIDE FOR PHOTO FILE
			if FILE_SUFFIX in SCAN_PHOTO_FORMAT:
				SHORT_SIDE = GetPhotoShortSideWithPillow(FILE)
			# [4.7.4] GET SHORT SIDE FOR VIDEO FILE
			elif FILE_SUFFIX in SCAN_VIDEO_FORMAT:
				SHORT_SIDE = GetVideoShortSideWithFFMPEG(FILE)
			# [4.7.5] SKIP UNKNOWN FILE
			else:
				continue
			# [4.7.6] SKIP FILE IF SHORT SIDE IS ERROR STRING
			if isinstance(SHORT_SIDE, str):
				print("[!] File %-64s | Skipped (Error)" % FILE.name[-64:])
				continue
			# [4.7.7] SKIP FILE IF SHORT SIDE ALREADY <= TARGET RESOLUTION
			if SHORT_SIDE <= DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION:
				print("[-] File %-64s | Skipped (Short Side: %d <= %d)" % (FILE.name[-64:], SHORT_SIDE, DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION))
				continue
			# [4.7.8] PRINT FILE NEEDS CONVERSION
			print("[*] File %-64s | Converting (Short Side: %d > %d)" % (FILE.name[-64:], SHORT_SIDE, DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION))
			# [4.7.9] BUILD OUTPUT FILE PATH (SAME DIRECTORY, FORCE .jpg / .mp4)
			if FILE_SUFFIX in SCAN_PHOTO_FORMAT:
				OUTPUT_FILE_PATH = FILE.with_suffix('.jpg')
			else:
				OUTPUT_FILE_PATH = FILE.with_suffix('.mp4')
			# [4.7.9.1] AVOID INPUT OUTPUT SAME PATH CONFLICT
			if OUTPUT_FILE_PATH == FILE:
				OUTPUT_FILE_PATH = FILE.with_stem(FILE.stem + '_out').with_suffix(OUTPUT_FILE_PATH.suffix)
			# [4.7.10] CONVERT PHOTO FILE
			if FILE_SUFFIX in SCAN_PHOTO_FORMAT:
				CONVERT_RESULT = ConvertPhotoWithPillow(FILE, OUTPUT_FILE_PATH)
			# [4.7.11] CONVERT VIDEO FILE
			else:
				CONVERT_RESULT = ConvertVideoWithFFMPEG(FILE, OUTPUT_FILE_PATH)
			# [4.7.12] PRINT CONVERSION RESULT
			print("[*] File %-64s | Result: %s" % (FILE.name[-64:], CONVERT_RESULT))

# [5] MAIN PROGRAM
# [5.1] MAIN PROGRAM FUNCTION
def Main():
	print("[*]")
	# [5.1.1] SCAN WORKING DIRECTORY
	SCAN_RESULT = ScanDirectoryWithPathLib(DEFAULT_WORKING_PATH)
	# [5.1.2] RUN LOGIC CONTROL
	ConvertAndResizeAndRenameLogicControl(SCAN_RESULT)
# [5.2] MAIN PROGRAM TRIGGER
if __name__ == '__main__':
	Main()
# [6] FINISH PROGRAM
print("[*] PROGRAM EXIT")