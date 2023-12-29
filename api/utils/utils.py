from pyrogram.types import Message

def get_file_id(message: Message):
    available_media = ("audio", "photo", "sticker", "animation", "video", "voice", "video_note")
    for kind in available_media:
            media = getattr(message, kind, None)
            if media is not None:
                return media.file_id