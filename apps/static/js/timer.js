// var this_js_script = $('script[src*=timer]');
var selector = $('#timer');
var total_milliseconds = parseFloat(selector.attr('data-upgrade-ends-at') * 1000);
var upgrade_ends_at = new Date(total_milliseconds);
var upgraded_percent = parseFloat(selector.attr('data-upgraded-duration'));
var upgraded_percent_dt = new Date(upgraded_percent);


if (upgrade_ends_at > Date.now()) {
    setInterval(function showTimer() {
        var delta = Math.floor((upgrade_ends_at - Date.now()));
        console.log(delta);
        console.log(upgrade_ends_at);
        console.log(upgrade_ends_at > Date.now());

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
        console.log(upgraded_percent_dt);
        console.log('\n\n');

        timer.text(formatedRemainingTime);

    }, 1000);
}
