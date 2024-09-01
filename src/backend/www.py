from libs.calendar_client import getAllEvents, createEvent
from libs.email_functions import getAllEmails
from libs.email_client import sendEmail
from libs.calendar_notes import makeNote
from libs.event_checker import shouldAddEvent
from libs.translate import translate
from libs.ai_client import askAI
from libs.chatbot import ask, initConvo
from libs.nylas_client import nylas
import libs.auth_database as auth_database

import flask
import os

app = flask.Flask(__name__, static_url_path="", static_folder="../frontend", template_folder="../frontend")

def getGrantFromRequest(request: flask.Request):
    token = request.cookies.get('token')
    if token is None:
        token = request.headers.get('Authorization')
        if token is None:
            return None

    return auth_database.getGrant(token)


@app.route("/")
def index():
    return flask.render_template("index.html", app_name="APP NAME")

@app.route("/login")
def login():
    return flask.render_template("login.html", app_name="APP NAME")

@app.route("/mail")
def mail():
    return flask.render_template("mail.html", app_name="APP NAME")

@app.route("/calendar")
def calendar():
    return flask.render_template("calendar.html", app_name="APP NAME")

@app.route("/chat")
def _chat():
    return flask.render_template("chat.html", app_name="APP NAME")

@app.route('/enhance')
def _enhance():
    return flask.render_template("enhance.html", app_name="APP NAME")

@app.route('/dashboard')
def _dashboard():
    return flask.render_template("dashboard.html", app_name="APP NAME")

@app.route("/api/chat", methods=["POST"])
def chat():
    grant_id = getGrantFromRequest(flask.request)
    if grant_id is None:
        return flask.jsonify({ "success": False, "error": "No token" })

    body = flask.request.json
    prompt = body["prompt"]

    if prompt is None:
        return flask.jsonify({ "success": False, "error": "No prompt" })

    res = ask(grant_id, prompt)

    return flask.jsonify({ "success": True, "response": res })

@app.route("/api/chat/init", methods=["POST"])
def _chat_init():
    grant_id = getGrantFromRequest(flask.request)
    if grant_id is None:
        return flask.jsonify({ "success": False, "error": "No token" })

    initConvo(grant_id)

    return flask.jsonify({ "success": True })

@app.route("/api/translate", methods=["POST"])
def _translate():
    body = flask.request.json
    text = body["text"]
    target_language = body["language"]

    translation = translate(text, target_language)

    return flask.jsonify({ "success": True, "translation": translation })

@app.route("/api/getmails", methods=["GET"])
def getmails():
    grant_id = getGrantFromRequest(flask.request)
    if grant_id is None:
        return flask.jsonify({ "success": False, "error": "No token" })

    data = getAllEmails(grant_id)
    return flask.jsonify({ "success": True, "mails": data })

@app.route("/api/summarize", methods=["POST"])
def summarize():
    body = flask.request.json
    text = body["text"]

    if text is None:
        return flask.jsonify({ "success": False, "error": "No text" })
    
    max_length = 3000
    if len(text) > max_length:
        text = text[-max_length:]
        text = " ... (truncated)\n\n" + text

    prompt = f"Summarize the following text: {text}"
    res = askAI(prompt)

    return flask.jsonify({ "success": True, "summary": res })

@app.route("/api/sendmail", methods=["POST"])
def sendmail():
    grant_id = getGrantFromRequest(flask.request)
    if grant_id is None:
        return flask.jsonify({ "success": False, "error": "No token" })

    body = flask.request.json
    name = "name"
    email = body["email"]
    subject = body["subject"]
    body = body["body"]
    sendEmail(grant_id, name, email, subject, body)
    return flask.jsonify({ "success": True })

@app.route("/api/enhance", methods=["POST"])
def enhance():
    body = flask.request.json
    text = body["text"]

    if text is None:
        return flask.jsonify({ "success": False, "error": "No text" })
    
    prompt = f"Enhance the following email by correcting spelling mistakes, using better words, just return the enhanced email, nothing more, nothing less, do NOT use introducing sentence like 'Here is the enhanced email:', JUST return the enhanced email: {text}"
    res = askAI(prompt)

    return flask.jsonify({ "success": True, "enhanced": res })

@app.route("/api/suggestmailreply", methods=["POST"])
def suggestmailreply():
    body = flask.request.json
    from_name = body["from_name"]
    email_body = body["body"]
    subject = body["subject"]
    
    prompt = f'Reply to this email. The sender is "{from_name}", the subject is "{email_body}" and the email is "{subject}".'
    res = askAI(prompt)
    return flask.jsonify({ "success": True, "reply": res })

@app.route("/api/getevents", methods=["GET"])
def getevents():
    grant_id = getGrantFromRequest(flask.request)
    if grant_id is None:
        return flask.jsonify({ "success": False, "error": "No token" })
    
    data = getAllEvents(grant_id)
    return flask.jsonify({ "success": True, "events": data })

@app.route("/api/eventnote", methods=["POST"])
def eventnote():
    body = flask.request.json
    note = body["note"]
    start = body["start_time"]
    end = body["end_time"]

    data = {
        "title": note,
        "start_time": start,
        "end_time": end
    }

    res = makeNote(data)
    return flask.jsonify({ "success": True, "note": res })

@app.route("/api/createevent", methods=["POST"])
def createevent():
    grant_id = getGrantFromRequest(flask.request)
    if grant_id is None:
        return flask.jsonify({ "success": False, "error": "No token" })
    
    body = flask.request.json
    title = body["title"]
    start_time = int(body["start_time"])
    end_time = int(body["end_time"])

    createEvent(grant_id, title, start_time, end_time)
    return flask.jsonify({ "success": True })

@app.route("/api/suggestevent", methods=["POST"])
def suggestevent():
    body = flask.request.json
    subject = body["subject"]
    body = body["body"]
    suggested_event = shouldAddEvent(subject, body)
    return flask.jsonify({ "success": True, "suggested_event": suggested_event })


REDIRECT_CLIENT_URI = 'http://localhost:5000/oauth/exchange'

@app.route("/oauth/google", methods=["GET"])
def build_auth_url():
  auth_url = nylas.auth.url_for_oauth2(
      config={
        "client_id": os.environ.get("NYLAS_CLIENT_ID"),
        "provider": 'google',
        "redirect_uri": REDIRECT_CLIENT_URI,
        "login_hint": "me@example.com"
      }
  )
  return flask.redirect(auth_url)

@app.route("/oauth/microsoft", methods=["GET"])
def build_microsoft_auth_url():
  auth_url = nylas.auth.url_for_oauth2(
      config={
        "client_id": os.environ.get("NYLAS_CLIENT_ID"),
        "provider": 'microsoft',
        "redirect_uri": REDIRECT_CLIENT_URI,
        "login_hint": "me@example.com"
      }
  )
  return flask.redirect(auth_url)

@app.route("/oauth/exchange", methods=["GET"])
def exchange_code_for_token():
  code_exchange_response = nylas.auth.exchange_code_for_token(
      request={
        "code": flask.request.args.get('code'),
        "client_id": os.environ.get("NYLAS_CLIENT_ID"),
        "redirect_uri": REDIRECT_CLIENT_URI
      }
  )

  data = {
    'email_address': code_exchange_response.email,
    'grant_id': code_exchange_response.grant_id
  }

  token = auth_database.storeGrant(data["grant_id"])
  
  resp = flask.make_response(flask.redirect("/"))
  resp.set_cookie('token', token, max_age=60*60)

  return resp

def start():
    app.run(port=5000, host='0.0.0.0', debug=True)