document.addEventListener('DOMContentLoaded', function() {

    // By default, load homepage
    //load('index');
  
    // Send email after submit form 
    document.querySelector('form').onsubmit = tweet;
    
});

function tweet() {
    event.preventDefault()

    const tweet_text = document.querySelector('#tweet_text').value;

    fetch('/tweet', {
        method: 'POST',
        tweet: JSON.stringify({
          tweet_text: tweet_text
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
    console.log(data);
}