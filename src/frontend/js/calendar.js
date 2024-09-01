function createCalendar(events) {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            center: 'addEventButton'
        },
        customButtons: {
            addEventButton: {
                text: 'Add Event',
                click: addEvent
            }
        },
        events: events
    });

    calendar.render();
}

async function getCalendar() {
    const calendar = await _fetch('/api/getevents');
    if (!calendar) {
        return;
    }

    const events = calendar.events.map(event => {
        return {
            title: event.title,
            start: new Date(event.when.start_time * 1000).toISOString(),
            end: new Date(event.when.end_time * 1000).toISOString(),
            url: event.link,
            allDay: false
        }
    })

    createCalendar(events);
}

function addEvent() {
    async function addEvent() {
        const title = prompt('Enter event title:');
        if (!title) {
            return;
        }

        const _start_time = prompt('Enter start time (YYYY-MM-DD HH:MM):');
        if (!_start_time) {
            return;
        }

        const _end_time = prompt('Enter end time (YYYY-MM-DD HH:MM):');
        if (!_end_time) {
            return;
        }

        const start_time = new Date(_start_time).getTime() / 1000;
        const end_time = new Date(_end_time).getTime() / 1000;

        if (start_time >= end_time) {
            alert('Start time must be before end time');
            return;
        }

        const res = await _fetch('/api/createevent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                start_time: start_time,
                end_time: end_time
            })
        });

        if (res && res.success) {
            getCalendar();
        } else {
            alert('Failed to create event');
        }
    }

    addEvent();
}

getCalendar();