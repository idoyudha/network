document.addEventListener('DOMContentLoaded', function() {

    // By default, load homepage
    //load('index');
  
    // Send email after submit form 
    document.querySelector('form').onsubmit = tweet;
    
});

function tweet() {
    event.preventDefault()

    const tweet = document.querySelector('#tweet_text').value;
    console.log(tweet)
    
    fetch('/tweet', {
        method: 'POST',
        body: JSON.stringify({
          tweet: tweet
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print emails
        console.log(result);
        // ... do something else with emails ...
    });
    return false;
}

function load(page) {
    console.log(page)
    fetch('/tweet_all')
    .then(response => response.json())
    .then(tweet => {
        console.log(tweet)
    })
}