import youtube_dl
import os
import sys
import appex



def main():

	saveDir = './Download'

	url = appex.get_attachments()[-1]
	ydl_opts = {
		'outtmpl': '{}/%(title)s.%(ext)s'.format(saveDir),
	#	'format': 'mp4',
		'subtitlesformat': 'best',
		'writesubtitles': False,
		'writeautomaticsub': False,
		'continuedl': True,
		'quiet': False
	}

	os.makedirs(saveDir, exist_ok=True)

	print("Downloading video...")

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	print("Finished downloading video")


if __name__ == "__main__":
	main()

