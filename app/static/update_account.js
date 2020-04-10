$.get('/account/live'
).done(function(response) {
    console.log(response)
    $(account_data).text(JSON.stringify(response, null, 4))
}).fail(function() {
    $(account_data).text("{{ ('Error: Could not get data from database.') }}");
});

// Enable pusher logging - don't include this in production
Pusher.logToConsole = true;

var pusher = new Pusher(pusher_key, {
  cluster: pusher_cluster,
  forceTLS: true
});

var channel = pusher.subscribe('account-channel');
channel.bind('account-update', function(data) {
  $(account_data).text(JSON.stringify(data, null, 4));
  $(live_data_flag).text("");
});
