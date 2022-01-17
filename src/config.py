import os


class Config:
    # general settings
    PORT = int(os.environ.get("PORT", 8888))
