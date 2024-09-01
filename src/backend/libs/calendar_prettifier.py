def prettify(data):
    newData = {
        "created_at": data.created_at,
        "organizer": data.organizer,
        "link": data.html_link,
        "title": data.title,
        "when": data.when
    }

    return newData