// Not using tweet and load_page function since paginator become fault

function tweet() {
    event.preventDefault()

    const tweet = document.querySelector('#tweet_text').value;
    console.log(tweet)

    document.querySelector('#tweet-ground').innerHTML = ""

    fetch('/tweet', {
        method: 'POST',
        body: JSON.stringify({
          tweet: tweet
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        load_page('home');
    })
};

function load_page(user) {
    console.log(user)
    fetch(`/tweet/${user}`)
    .then(response => response.json())
    .then(tweets => {
        console.log(tweets);

        for (let i = 0; i < tweets.length; i++) {
            let obj = tweets[i];
            
            // Create new div element
            const data = document.createElement("div");
            data.className = "card text-white bg-dark mb-3";

            // Create tweet card from parent element tweet-ground
            const l = document.getElementById("tweet-ground")
            const card = l.appendChild(data)

            // Create new element for tweet head
            const head = document.createElement("div")
            head.className = "card-header";
            head.innerHTML = `@${obj.user} &#0149; ${obj.time}`;
            data.appendChild(head)

            // Create new element for tweet body
            const body = document.createElement("div")
            body.className = "card-body"
            const bd = data.appendChild(body)

            const t = document.createElement("p");
            t.className = "text-p";
            t.innerHTML = `${obj.tweet}`
            bd.appendChild(t)

            const foot = document.createElement("div")
            foot.className = "card-footer";
            foot.innerHTML = `<div class='row' id='btn' role='group' aria-label='tweet group'>
                                <div class='col-sm'>
                                    <p class='t-btn1'><i class='far fa-comment-dots'></i>total</p>
                                </div>
                                <div class='col-sm'>
                                    <p class='t-btn2'><i class='fas fa-retweet'></i>total</p>
                                </div>
                                <div class='col-sm'>
                                    <p class='t-btn3'><i class='far fa-heart'></i>total</p>
                                </div>
                                <div class='col-sm'>
                                    <p class='t-btn4'><i class='far fa-share-square'></i>total</p>
                                </div>
                            </div>`;
            data.appendChild(foot)
        }
    });
}

function edit(id) {
    console.log("edit_function")
    console.log(id)
    let tweetText = document.getElementById(`tweet_${id}`).textContent;
    console.log(tweetText)
}