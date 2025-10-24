from flask import Blueprint, request, jsonify
from app import db
from app.models.ticket import Ticket, TicketActivity
from app.schemas.ticket_schema import ticket_schema, tickets_schema
from app.services.assignment_service import AssignmentService
from datetime import datetime
import uuid