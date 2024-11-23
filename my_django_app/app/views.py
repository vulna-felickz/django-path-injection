import datetime as dt
import logging
import os
import pathlib
from typing import Dict, List

from django import http
from django.core.files import storage as django_storage
from rest_framework import decorators
from rest_framework import exceptions as rf_exceptions  # basic exceptions
from rest_framework import parsers
from rest_framework import request
from rest_framework import response
from rest_framework import views

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest


class FileManagerDownloadView(views.APIView):
    """Endpoints to download file"""

    # path to shared volume
    volume_path = pathlib.Path(settings.FILE_MANAGER_ROOT)
    # list of supported subdirectories
    supported_subdirs = settings.FILE_MANAGER_SUBDIRS

    def post(self, request: request.Request):
        """Get a downloadable attachment given path to a file"""

        subdir = request.data.get('subdir')
        filename = request.data.get('filename')

        if filename is None or filename == '':
            raise exceptions.MissingRequiredFields(
                detail='filename is a required field.')

        if subdir is None or subdir == '':
            raise exceptions.MissingRequiredFields(
                detail='subdir is a required field.')

        # Remove fwd slash in the front
        subdir = subdir.lstrip('/')

        if not os.path.isdir(self.volume_path / subdir):
            raise HttpResponseBadRequest('This subdirectory does not exist.')

        if not (self.volume_path / subdir / filename).exists():
            raise rf_exceptions.NotFound(detail='File does not exist.')

        try:
            return http.FileResponse(
                open(self.volume_path / subdir / filename, 'rb'),
                filename=filename,
                as_attachment=True)

        except Exception as e:
            raise exceptions.ServerError(detail=str(e))