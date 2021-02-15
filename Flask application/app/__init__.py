from flask import Flask
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 1,
    "SECRET_KEY": 'you-will-never-guess',
    "UPLOAD_FOLDER": 'static\\uploads',
    "DROPZONE_ALLOWED_FILE_CUSTOM": True,
    "DROPZONE_MAX_FILES": 1,
    "DROPZONE_MAX_FILE_SIZE": 10,
    "DROPZONE_ALLOWED_FILE_TYPE": 'image/*, .png, .jpg, .jpeg',
    "DROPZONE_INVALID_FILE_TYPE": "Plik musi mieć rozszerzenie typu png, jpg lub jpeg",
    "DROPZONE_DEFAULT_MESSAGE": "Przeciągnij lub kliknij aby dodać wybrane zdjęcie",
    "DROPZONE_ENABLE_CSRF": True
}

app = Flask(__name__, static_folder='C:\\Users\\klaud\\OneDrive\\Documents\\studia\\'
                                    'Informaryczne narzędzia wizualizacji danych\\UM\\app\\static')

# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

bootstrap = Bootstrap()
bootstrap.init_app(app)

dropzone = Dropzone(app)
# enable CSRF protection
csrf = CSRFProtect(app)

from app import main

app.run(debug=True)



