#!/usr/bin/env python
"""
Files handler module
"""
import os
from flask import abort
from werkzeug.utils import secure_filename

supported_extension = ['.csv']

def generate_filename(email: str, ext: str, file_id: int) -> str:
    """ Generate a defined filename with file id """
    sep = '_'
    # Set a defined name
    defined_name = email + sep + 'qb' + sep + file_id + ext
    # Secure the filename
    filename = secure_filename(defined_name)
    return filename


def upload(files, folder, current_user):
    """ Upload a file to the server """
    # Process the files
    if len(files) > 1:
        return {
            'status': 'error',
            'message': 'You can only upload a single file'
        }
    else:
        file = files[0]
        base, ext = os.path.splitext(file.filename)
        # Check if the file extension is supported
        if ext not in supported_extension:
            return {
                'status': 'error',
                'message': 'Unsupported file format. Upload a csv file'
            }
        # Create a defined filename
        file_id = 1
        filename = generate_filename(current_user.email.split('@')[0], ext, file_id)
        dst = os.path.join(folder, filename)
        # Generate a new file_id if file exist
        while os.path.exists(dst):
            file_id += 1
            dst = os.path.join(folder, generate_filename(current_user.email.split('@')[0], ext, file_id))
        # Save the file
        try:
            file.save(dst)
            return {
                'status': 'success',
                'message': 'File uploaded successfully'
            }
        except Exception as e:
            abort(403)