#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Файл для продакшн-запуска приложения через Gunicorn WSGI-сервер.
"""

from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
