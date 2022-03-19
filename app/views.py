from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    #print(Note.query.get(int(0)).first())
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(content=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            #new_id = Note.query.filter_by(content=note).first().id
            #print(Note.query.get(int(new_id))

            flash('Note added!', category='success')

    return render_template("index.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
               
    return jsonify({})

