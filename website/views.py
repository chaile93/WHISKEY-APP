from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/update-note', methods=['PUT'])
@login_required
def update_note():
    data = request.get_json()
    note_id = data['noteId']
    new_content = data['content']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        note.data = new_content
        db.session.commit()
        return jsonify({'message': 'Note updated successfully'})
    return jsonify({'message': 'Note not found or permission denied'}), 404

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


