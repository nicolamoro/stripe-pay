import os


class Config:
    # general settings
    PORT = int(os.environ.get("PORT", 8888))

    # API
    API_BASE_URL = "/api/1"
    API_VERSION = "1.0.0"
    SWAGGERUI_URL = "/docs"
    SWAGGERUI_TITLE = "Twinkly Assignment API"
    SWAGGERUI_DESCRIPTION = "Documentation of API implemented"
    SWAGGERUI_CONTACT = "nikimoro@gmail.com"
