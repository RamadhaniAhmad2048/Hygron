# GOON
# [1] START PROGRAM
print("[*] PROGRAM START")
print("PROGRAM GOON")
# [2] IMPORT LIBRARY
# [2.1] IMPORT BUILD-IN LIBRARY
import os
import json
import pathlib
import re
import shutil
# [2.2] IMPORT EXTERNAL LIBRARY
try:
	import ffmpeg
	from PIL import Image
# [2.3] ERROR EXTERNAL MODULE NOT FOUND HANDLING
except ModuleNotFoundError:
	print("[!] External library not found, try \'pip install pillow ffmpeg-python\'")
# [3] DEFINE VARIABLE
# [3.1] CUSTOMIZABLE VARIABLE
DEFAULT_WORKING_PATH                = pathlib.Path('.')
DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION = 720
AUTO_RENAME_FILE                    = False
AUTO_DELETE_ORIGINAL                = False
AUTO_CREATE_PDF_PHOTO               = False
# [3.2] IMPORTANT VARIABLE
SCAN_PHOTO_FORMAT = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.bmp', '.tiff'}
SCAN_VIDEO_FORMAT = {'.mp4', '.mkv',  '.mov',  '.ts',  '.wmv',  '.m4v', '.avi',  '.flv'}
SCAN_ALL_FORMAT   = SCAN_PHOTO_FORMAT | SCAN_VIDEO_FORMAT
PROGRESS_LOG_PATH = pathlib.Path('hygron_progress.json')
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
		return 'AttributeError'
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
	# [4.4.4] TRY RESIZE AND CONVERT PHOTO FILE
	try:
		ORIGINAL_WIDTH, ORIGINAL_HEIGHT = INPUT_FILE.size
		# [4.4.5] CALCULATE NEW RESOLUTION KEEP ASPECT RATIO
		if ORIGINAL_WIDTH < ORIGINAL_HEIGHT:
			NEW_WIDTH  = DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
			NEW_HEIGHT = int(ORIGINAL_HEIGHT * DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION / ORIGINAL_WIDTH)
		else:
			NEW_HEIGHT = DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
			NEW_WIDTH  = int(ORIGINAL_WIDTH * DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION / ORIGINAL_HEIGHT)
		# [4.4.6] GIF CONVERTION
		if INPUT_FILE_PATH.suffix.lower() == '.gif':
			# [4.4.6.1] GET ALL GIF FRAMES INFORMATION
			GIF_FRAMES    = []  # FIX: was GIF_FRAME (typo)
			GIF_DURATIONS = []  # FIX: was GIF_DURATION (typo)
			GIF_DISPOSALS = []  # FIX: was GIF_DISPOSAL (typo)
			try:
				while True:
					FRAME_INFO     = INPUT_FILE.info
					FRAME_DURATION = FRAME_INFO.get('duration', 100)
					FRAME_DISPOSAL = FRAME_INFO.get('disposal', 2)
					# [4.4.6.2] CONVERT FRAME
					RESIZED_FRAME = INPUT_FILE.copy().resize((NEW_WIDTH, NEW_HEIGHT), Image.LANCZOS)
					# [4.4.6.3] CONVERT TO RGBA
					if RESIZED_FRAME.mode not in ('P', 'RGBA', 'RGB'):
						RESIZED_FRAME = RESIZED_FRAME.convert('RGBA')
					GIF_FRAMES.append(RESIZED_FRAME)
					GIF_DURATIONS.append(FRAME_DURATION)
					GIF_DISPOSALS.append(FRAME_DISPOSAL)
					INPUT_FILE.seek(INPUT_FILE.tell() + 1)
			except EOFError:
				pass  # FIX: was `raise e` (e not defined), EOF = normal end of frames
			# [4.4.6.4] FILTER EMPTY FRAME LIST
			if not GIF_FRAMES:
				return 'AttributeError'
			# [4.4.6.5] SAVE ALL FRAMES AS OUTPUT GIF
			GIF_FRAMES[0].save(
				OUTPUT_FILE_PATH,
				format='GIF',
				save_all=True,
				append_images=GIF_FRAMES[1:],
				loop=INPUT_FILE.info.get('loop', 0),
				duration=GIF_DURATIONS,
				disposal=GIF_DISPOSALS,
			)
			return 'Success'
		# [4.4.7] BRANCH: NON-GIF FILE HANDLING (ORIGINAL LOGIC)
		else:
			# [4.4.7.1] RESIZE IMAGE
			OUTPUT_FILE = INPUT_FILE.resize((NEW_WIDTH, NEW_HEIGHT), Image.LANCZOS)
			# [4.4.7.2] SAVE OUTPUT IMAGE
			OUTPUT_FILE.save(OUTPUT_FILE_PATH)
			return 'Success'
	# [4.4.8] ERROR ATTRIBUTE HANDLING
	except AttributeError:
		print("[!] File %s Attribute Error" % str(INPUT_FILE_PATH)[-64:])
		return 'AttributeError'
	# [4.4.9] ERROR PERMISSION DENIED HANDLING
	except PermissionError:
		print("[!] File %s Permission Denied Error" % str(OUTPUT_FILE_PATH)[-64:])
		return 'PermissionError'
# [4.5] CONVERT VIDEO WITH FFMPEG
def ConvertVideoWithFFMPEG(INPUT_FILE_PATH, OUTPUT_FILE_PATH):
	# [4.5.1] GET VIDEO SHORT SIDE
	INPUT_SHORT_RESOLUTION = GetVideoShortSideWithFFMPEG(INPUT_FILE_PATH)
	# [4.5.2] FILTER ERROR RETURN
	if isinstance(INPUT_SHORT_RESOLUTION, str):
		return INPUT_SHORT_RESOLUTION
	# [4.5.3] CALCULATE SCALE FILTER (keep aspect ratio, short side = 720)
	# ffmpeg scale: -2 means auto-calculate the other side divisible by 2
	if INPUT_SHORT_RESOLUTION <= DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION:
		print("[~] File %s already <= %dp, skipping" % (str(INPUT_FILE_PATH)[-64:], DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION))
		return 'AlreadySmall'
	# [4.5.4] BUILD FFMPEG SCALE FILTER
	# scale=w=-2:h=720 if landscape, scale=w=720:h=-2 if portrait
	try:
		PROBE_VIDEO  = ffmpeg.probe(str(INPUT_FILE_PATH))
		VIDEO_STREAM = next(s for s in PROBE_VIDEO['streams'] if s['codec_type'] == 'video')
		WIDTH        = int(VIDEO_STREAM['width'])
		HEIGHT       = int(VIDEO_STREAM['height'])
		if WIDTH < HEIGHT:
			# portrait
			SCALE_FILTER = 'scale=%d:-2' % DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
		else:
			# landscape or square
			SCALE_FILTER = 'scale=-2:%d' % DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
	except (ffmpeg.Error, StopIteration, KeyError):
		SCALE_FILTER = 'scale=-2:%d' % DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION
	# [4.5.5] BUILD TEMP OUTPUT PATH (avoid overwrite mid-process)
	TEMP_OUTPUT_PATH = OUTPUT_FILE_PATH.with_suffix('.tmp.mp4')
	# [4.5.6] TRY RUN FFMPEG CONVERSION
	try:
		(
			ffmpeg
			.input(str(INPUT_FILE_PATH))
			.output(
				str(TEMP_OUTPUT_PATH),
				vcodec  = 'libx264',
				acodec  = 'aac',
				vf      = SCALE_FILTER,
				crf     = 23,         # quality: 18=high, 28=low, 23=default
				preset  = 'medium',   # encoding speed vs size
				movflags= '+faststart' # web-friendly MP4
			)
			.overwrite_output()
			.run(quiet=True)
		)
	# [4.5.7] ERROR INTERNAL FFMPEG HANDLING
	except ffmpeg.Error as e:
		print("[!] File %s FFMPEG Conversion Error" % str(INPUT_FILE_PATH)[-64:])
		if TEMP_OUTPUT_PATH.exists():
			TEMP_OUTPUT_PATH.unlink()
		return 'FFMPEGError'
	# [4.5.8] RENAME TEMP TO FINAL OUTPUT (use replace() for Windows compatibility)
	TEMP_OUTPUT_PATH.replace(OUTPUT_FILE_PATH)
	return 'Success'
# [4.6] LOAD PROGRESS LOG
def LoadProgressLog():
	# [4.6.1] CHECK IF PROGRESS LOG EXISTS
	if not PROGRESS_LOG_PATH.exists():
		return {}
	# [4.6.2] TRY LOAD PROGRESS LOG
	try:
		with open(PROGRESS_LOG_PATH, 'r') as F:
			return json.load(F)
	except (json.JSONDecodeError, PermissionError):
		print("[!] Progress log corrupted or unreadable, starting fresh")
		return {}
# [4.7] SAVE PROGRESS LOG
def SaveProgressLog(PROGRESS_LOG):
	# [4.7.1] TRY SAVE PROGRESS LOG
	try:
		with open(PROGRESS_LOG_PATH, 'w') as F:
			json.dump(PROGRESS_LOG, F, indent=2)
	except PermissionError:
		print("[!] Cannot write progress log, crash recovery disabled")
# [4.8] CONVERT RESIZE RENAME LOGIC CONTROL
def ConvertAndResizeAndRenameLogicControl(SCAN_RESULT):
	# [4.8.1] LOAD PROGRESS LOG FOR CRASH RECOVERY
	PROGRESS_LOG    = LoadProgressLog()
	GLOBAL_COUNTER  = PROGRESS_LOG.get('_last_counter', 0)
	PROCESSED_FILES = set(PROGRESS_LOG.get('_processed', []))
	TOTAL_FILES     = sum(len(FILES) for FILES in SCAN_RESULT.values())
	CURRENT_INDEX   = 0
	print("[*] Found %d files to process" % TOTAL_FILES)
	# [4.8.2] LOOP EACH DIRECTORY IN SCAN RESULT
	for DIRECTORY, FILE_LIST in SCAN_RESULT.items():
		# [4.8.3] SORT FILES FOR CONSISTENT ORDERING
		FILE_LIST_SORTED = sorted(FILE_LIST)
		# [4.8.4] LOOP EACH FILE IN DIRECTORY
		for INPUT_FILE_PATH in FILE_LIST_SORTED:
			CURRENT_INDEX += 1
			FILE_KEY = str(INPUT_FILE_PATH)
			# [4.8.5] SKIP IF ALREADY PROCESSED (CRASH RECOVERY)
			if FILE_KEY in PROCESSED_FILES:
				print("[~] [%d/%d] SKIP (already done): %s" % (CURRENT_INDEX, TOTAL_FILES, str(INPUT_FILE_PATH)[-64:]))
				continue
			print("[-] [%d/%d] Processing: %s" % (CURRENT_INDEX, TOTAL_FILES, str(INPUT_FILE_PATH)[-64:]))
			IS_PHOTO = INPUT_FILE_PATH.suffix.lower() in SCAN_PHOTO_FORMAT
			IS_VIDEO = INPUT_FILE_PATH.suffix.lower() in SCAN_VIDEO_FORMAT
			# [4.8.6] GET SHORT SIDE OF FILE
			if IS_PHOTO:
				SHORT_SIDE = GetPhotoShortSideWithPillow(INPUT_FILE_PATH)
			elif IS_VIDEO:
				SHORT_SIDE = GetVideoShortSideWithFFMPEG(INPUT_FILE_PATH)
			else:
				continue
			# [4.8.7] SKIP IF ERROR GETTING SHORT SIDE
			if isinstance(SHORT_SIDE, str):
				print("[!] [%d/%d] SKIP (error getting size): %s" % (CURRENT_INDEX, TOTAL_FILES, str(INPUT_FILE_PATH)[-64:]))
				continue
			# [4.8.8] SKIP IF ALREADY SMALL ENOUGH
			if SHORT_SIDE <= DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION:
				print("[~] [%d/%d] SKIP (already <= %dp): %s" % (CURRENT_INDEX, TOTAL_FILES, DEFAULT_SHORTSIDE_OUTPUT_RESOLUTION, str(INPUT_FILE_PATH)[-64:]))
				PROCESSED_FILES.add(FILE_KEY)
				PROGRESS_LOG['_processed'] = list(PROCESSED_FILES)
				SaveProgressLog(PROGRESS_LOG)
				continue
			# [4.8.9] BUILD OUTPUT FILE PATH
			GLOBAL_COUNTER += 1
			if AUTO_RENAME_FILE:
				# [4.8.9.1] RENAME WITH SEQUENTIAL NUMBER
				if IS_VIDEO:
					OUTPUT_SUFFIX = '.mp4'
				else:
					OUTPUT_SUFFIX = INPUT_FILE_PATH.suffix.lower()
				OUTPUT_FILE_NAME = '%03d%s' % (GLOBAL_COUNTER, OUTPUT_SUFFIX)
				OUTPUT_FILE_PATH = DIRECTORY / OUTPUT_FILE_NAME
			else:
				# [4.8.9.2] KEEP ORIGINAL NAME, VIDEO OUTPUT ALWAYS .mp4
				if IS_VIDEO:
					OUTPUT_FILE_PATH = DIRECTORY / (INPUT_FILE_PATH.stem + '.mp4')
				else:
					OUTPUT_FILE_PATH = INPUT_FILE_PATH  # overwrite in-place
			# [4.8.10] AVOID OVERWRITING INPUT IF OUTPUT == INPUT (for non-rename mode)
			OVERWRITE_ORIGINAL = (OUTPUT_FILE_PATH == INPUT_FILE_PATH)
			if OVERWRITE_ORIGINAL:
				TEMP_INPUT = INPUT_FILE_PATH.with_suffix(INPUT_FILE_PATH.suffix + '.orig')
				shutil.copy2(INPUT_FILE_PATH, TEMP_INPUT)
				ACTUAL_INPUT = TEMP_INPUT
			else:
				ACTUAL_INPUT = INPUT_FILE_PATH
			# [4.8.11] RUN CONVERSION
			if IS_PHOTO:
				RESULT = ConvertPhotoWithPillow(ACTUAL_INPUT, OUTPUT_FILE_PATH)
			elif IS_VIDEO:
				RESULT = ConvertVideoWithFFMPEG(ACTUAL_INPUT, OUTPUT_FILE_PATH)
			else:
				RESULT = 'UnknownFormat'
			# [4.8.12] HANDLE RESULT
			if RESULT == 'Success':
				print("[+] [%d/%d] Done: %s" % (CURRENT_INDEX, TOTAL_FILES, str(OUTPUT_FILE_PATH)[-64:]))
				# [4.8.13] DELETE ORIGINAL IF FLAG SET
				if AUTO_DELETE_ORIGINAL and not OVERWRITE_ORIGINAL:
					try:
						INPUT_FILE_PATH.unlink()
						print("[x] Deleted original: %s" % str(INPUT_FILE_PATH)[-64:])
					except PermissionError:
						print("[!] Cannot delete original: %s" % str(INPUT_FILE_PATH)[-64:])
				# [4.8.14] CLEANUP TEMP INPUT IF OVERWRITE MODE
				if OVERWRITE_ORIGINAL:
					try:
						TEMP_INPUT.unlink()
					except PermissionError:
						pass
				# [4.8.15] SAVE PROGRESS
				PROCESSED_FILES.add(FILE_KEY)
				PROGRESS_LOG['_processed']    = list(PROCESSED_FILES)
				PROGRESS_LOG['_last_counter'] = GLOBAL_COUNTER
				SaveProgressLog(PROGRESS_LOG)
			else:
				print("[!] [%d/%d] FAILED (%s): %s" % (CURRENT_INDEX, TOTAL_FILES, RESULT, str(INPUT_FILE_PATH)[-64:]))
				# [4.8.16] CLEANUP TEMP INPUT ON FAIL
				if OVERWRITE_ORIGINAL and TEMP_INPUT.exists():
					shutil.copy2(TEMP_INPUT, INPUT_FILE_PATH)  # restore original
					TEMP_INPUT.unlink()
	# [4.8.17] CLEANUP PROGRESS LOG AFTER ALL DONE
	if PROGRESS_LOG_PATH.exists():
		PROGRESS_LOG_PATH.unlink()
		print("[*] Progress log cleared")
	print("[*] Processing complete. %d files processed." % len(PROCESSED_FILES))
# [5] MAIN PROGRAM
# [5.1] MAIN PROGRAM FUNCTION
def Main():
	SCAN_RESULT = ScanDirectoryWithPathLib(DEFAULT_WORKING_PATH)
	ConvertAndResizeAndRenameLogicControl(SCAN_RESULT)
if __name__ == '__main__':
	Main()
# [6] FINISH PROGRAM
print("[*] PROGRAM EXIT")