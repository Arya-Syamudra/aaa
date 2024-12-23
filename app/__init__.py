"""
Modul inisialisasi untuk aplikasi Flask dalam Sistem Pakar Proker.
"""

from flask import Flask
from app.routes import bp

def create_app():
    """
    Membuat dan mengonfigurasi aplikasi Flask.
    """
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app
