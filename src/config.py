import os


class Config:
    # general settings
    PORT = int(os.environ.get("PORT", 8888))

        # API
        API_BASE_URL = "/api/1"
        API_VERSION = "1.0.0"
        SWAGGERUI_URL = "/docs"
        SWAGGERUI_TITLE = "Stripe-Pay API"
        SWAGGERUI_DESCRIPTION = "Documentation of API implemented"
        SWAGGERUI_CONTACT = "nikimoro@gmail.com"

    # Stripe
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "SuperSecretKey")

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "SomeRandomSecretPhrase")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 900))
