function secondsToTime(seconds) {
    seconds = parseInt(seconds);
    let minutes = 0;
    let hours = 0;
    let days = 0;
    if (seconds >= 60) {
        minutes = Math.floor(seconds / 60);
        seconds -= minutes * 60;
        if (minutes >= 60) {
            hours = Math.floor(minutes / 60);
            minutes -= hours * 60;
            if (hours >= 24) {
                days = Math.floor(hours / 24);
                hours -= days * 24;
            }
        }
    }
    let result = '';
    if (days > 0) {
        result += ' ' + days + ' day';
        if (days > 1) {
            result += 's';
        }
    }
    if (hours > 0) {
        result += ' ' + hours + ' hour';
        if (hours > 1) {
            result += 's';
        }
    }
    if (minutes > 0) {
        result += ' ' + minutes + ' minute';
        if (minutes > 1) {
            result += 's';
        }
    }
    if (seconds > 0) {
        result += ' ' + seconds + ' second';
        if (seconds > 1) {
            result += 's';
        }
    }
    return result;
}

function prepareTime() {
    $('.timezone').html(Intl.DateTimeFormat().resolvedOptions().timeZone);
    $('.localtime[data-aired]').each((id, elem) => {
        elem = $(elem);
        let aired = new Date(elem.data('aired'));
        let text = aired.toLocaleString('en');
        elem.html(text);
    });
    updateTime();
}

function updateTime() {
    $('.localtime[data-scheduled]').each((id, elem) => {
        elem = $(elem);
        let scheduled = new Date(elem.data('scheduled'));
        let now = new Date();
        let difference = scheduled - now;
        let text = scheduled.toLocaleString('en');
        if (difference > 0) {
            text += ', in ' + secondsToTime(difference / 1000);
            setTimeout(updateTime, 1000);
        } else {
            let runningFor = -difference / 1000 / 60 / 60;
            if (runningFor < 3) {
                text += ', stream should be running now, baring any '
                    + 'latepatness or other unexpected event';
                let remaining = 3 - runningFor;
                setTimeout(updateTime, remaining * 1000 * 60 * 60);
            } else {
                text += ', stream should have ended now; refresh this page '
                    + 'later to get the schedule of the next stream! (maybe)';
                setTimeout(() => { location.reload(true); }, 10 * 60 * 1000);
            }
        }
        elem.html(text);
    });
}
$(prepareTime);
