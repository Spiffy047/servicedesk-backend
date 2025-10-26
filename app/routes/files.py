from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app import db
from app.models.attachment import FileAttachment
from app.models.ticket import Ticket
import os
import uuid
from datetime import datetime
