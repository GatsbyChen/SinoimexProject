import imageio
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
imageio.plugins.ffmpeg.download()