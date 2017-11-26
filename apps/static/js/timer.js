var selector = $('#timer');
var upgrade_started_at = parseFloat(selector.attr('data-upgrade-started-at') * 1000);
var upgrade_ends_at = parseFloat(selector.attr('data-upgrade-ends-at') * 1000);
var upgrade_ends_at_dt = new Date(upgrade_ends_at);



function calculate_upgrade_percent() {
    var progress_bar = $('#dynamic-progress-bar');

    var one_percent = (upgrade_ends_at - upgrade_started_at) / 100;
    var upgraded_percent = (100 - (upgrade_ends_at_dt - Date.now()) / one_percent).toFixed(1);

    progress_bar.css('width', upgraded_percent + '%');
    progress_bar.text(upgraded_percent + '%');

    // To delete
    $('#foo').text(upgraded_percent + '%');

}


if (upgrade_ends_at_dt > Date.now()) {
    setInterval(function showTimer() {
        calculate_upgrade_percent();

        var delta = Math.floor((upgrade_ends_at_dt - Date.now()));
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
        console.log('\n\n');

        timer.text(formatedRemainingTime);
    }, 1000);
}
