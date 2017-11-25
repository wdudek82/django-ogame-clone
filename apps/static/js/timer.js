// var this_js_script = $('script[src*=timer]');
var selector = $('#timer');
var total_milliseconds = parseFloat(selector.attr('data-datetime') * 1000);
var datetime = new Date(total_milliseconds);

if (datetime > Date.now()) {
    setInterval(function showTimer() {
        var delta = Math.floor((datetime - Date.now()));
        console.log(delta);
        console.log(datetime);
        console.log(datetime > Date.now());

        var timer = $('#timer');
        if (delta <= 600) {
            timer.css('color', 'red');
        } else {
            timer.css('color', 'black');
        }

        var timeRemaining = new Date(delta);
        var day = 24 * 60 * 60 * 1000;  // hours * minutes * seconds * milliseconds
        var hour = 60 * 60 * 1000;
        var rDays = Math.floor(delta / day) ? Math.floor(delta / day) + 'd ' : '';
        var rHours = Math.floor(delta % day / hour) ? Math.floor(delta % day / hour) + 'h ' : '';
        var rMinutes = (timeRemaining.getMinutes() < 10 ? '0' : '') + timeRemaining.getMinutes();
        var rSeconds = (timeRemaining.getSeconds() < 10 ? '0' : '') + timeRemaining.getSeconds();
        var formatedRemainingTime = rDays + rHours + rMinutes + 'm ' + rSeconds + 's';
        console.log(formatedRemainingTime);
        console.log('\n\n');

        timer.text(formatedRemainingTime);

    }, 1000);
}
