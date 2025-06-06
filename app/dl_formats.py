import copy
import logging

AUDIO_FORMATS = ("m4a", "mp3", "opus", "wav", "flac")
logger = logging.getLogger(__name__)


def get_format(format: str, quality: str) -> str:
    """
    Returns format for download

    Args:
      format (str): format selected
      quality (str): quality selected

    Raises:
      Exception: unknown quality, unknown format

    Returns:
      dl_format: Formatted download string
    """
    format = format or "any"

    if format.startswith("custom:"):
        return format[7:]

    if format == "thumbnail":
        # Quality is irrelevant in this case since we skip the download
        return "bestaudio/best"

    if format in AUDIO_FORMATS:
        # Audio quality needs to be set post-download, set in opts
        return f"bestaudio[ext={format}]/bestaudio/best"

    if format in ("mp4", "any"):
        if quality == "audio":
            return "bestaudio/best"
        # video {res} {vfmt} + audio {afmt} {res} {vfmt}
        vfmt, afmt = ("[ext=mp4]", "[ext=m4a]") if format == "mp4" else ("", "")
        vres = f"[height<={quality}]" if quality not in ("best", "best_ios", "worst") else ""
        vcombo = vres + vfmt

        if quality == "best_ios":
            # iOS has strict requirements for video files, requiring h264 or h265
            # video codec and aac audio codec in MP4 container. This format string
            # attempts to get the fully compatible formats first, then the h264/h265
            # video codec with any M4A audio codec (because audio is faster to
            # convert if needed), and falls back to getting the best available MP4
            # file.
            return f"bestvideo[vcodec~='^((he|a)vc|h26[45])']{vres}+bestaudio[acodec=aac]/bestvideo[vcodec~='^((he|a)vc|h26[45])']{vres}+bestaudio{afmt}/bestvideo{vcombo}+bestaudio{afmt}/best{vcombo}"
        return f"bestvideo{vcombo}+bestaudio{afmt}/best{vcombo}"

    raise Exception(f"Unkown format {format}")


def get_opts(format: str, quality: str, ytdl_opts: dict) -> dict:
    """
    Returns extra download options
    Mostly postprocessing options

    Args:
      format (str): format selected
      quality (str): quality of format selected (needed for some formats)
      ytdl_opts (dict): current options selected

    Returns:
      ytdl_opts: Extra options
    """

    opts = copy.deepcopy(ytdl_opts)
    postprocessors = []

    if format in AUDIO_FORMATS:
        postprocessors.append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
                "preferredquality": 0 if quality == "best" else quality,
            }
        )
        logger.info(f"Audio transcoding options: format={format}, quality={quality}")
        
        # Add voice mono settings for MP3
        if format == "mp3" and quality == "32_mono":
            opts["postprocessor_args"] = {
                "ffmpeg": ["-ac", "1", "-ar", "22050", "-q:a", "8"]
            }
            logger.info(f"FFmpeg postprocessor args for MP3 32_mono: {opts['postprocessor_args']}")
            
        # Add voice mono settings for OPUS
        # https://www.opus-codec.org/docs/opus_api-1.2/group__opus__encoder.html
        # https://ffmpeg.org/ffmpeg-codecs.html#Option-Mapping
        # https://wiki.xiph.org/Opus_Recommended_Settings#:~:text=Opus%20uses%20a%2020%20ms,low%20latency%20and%20good%20quality.
        # Application VOIP option will make opus favor speech intelligibility.
        if format == "opus":
            if quality == "16_mono":
                opts["postprocessor_args"] = {
                    "ffmpeg": [
                        "-c:a", "libopus",            # Use OPUS codec
                        "-ac", "1",                   # Force mono
                        "-b:a", "16k"                 # Set bitrate to 16kbps
                        #"-application", "voip"        # Optimize for voice
                    ]
                }
            if quality == "24":
                opts["postprocessor_args"] = {
                    "ffmpeg": [
                        "-c:a", "libopus",            # Use OPUS codec
                        "-b:a", "24k"                 # Set bitrate to 24kbps
                    ]
                }
            if quality == "32":
                opts["postprocessor_args"] = {
                    "ffmpeg": [
                        "-c:a", "libopus",            
                        "-b:a", "32k"                 
                    ]
                }
            if quality == "64":
                opts["postprocessor_args"] = {
                    "ffmpeg": [
                        "-c:a", "libopus",
                        "-b:a", "64k",
                        "-application", "audio"
                    ]
                }
            if quality == "48":
                opts["postprocessor_args"] = {
                    "ffmpeg": [
                        "-c:a", "libopus",
                        "-b:a", "48k",
                        "-application", "audio"
                    ]
                }

            logger.info(f"FFmpeg postprocessor args for OPUS: {opts['postprocessor_args']}")

        # Audio formats without thumbnail
        if format not in ("wav") and "writethumbnail" not in opts:
            opts["writethumbnail"] = True
            postprocessors.append(
                {
                    "key": "FFmpegThumbnailsConvertor",
                    "format": "jpg",
                    "when": "before_dl",
                }
            )
            postprocessors.append({"key": "FFmpegMetadata"})
            postprocessors.append({"key": "EmbedThumbnail"})

    if format == "thumbnail":
        opts["skip_download"] = True
        opts["writethumbnail"] = True
        postprocessors.append(
            {"key": "FFmpegThumbnailsConvertor", "format": "jpg", "when": "before_dl"}
        )

    opts["postprocessors"] = postprocessors + (
        opts["postprocessors"] if "postprocessors" in opts else []
    )
    return opts
