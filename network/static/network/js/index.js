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
    // Get content of tweet
    let tweetText = document.getElementById(`tweet_${id}`).textContent;
    console.log(tweetText)
    let tweet_area = document.getElementById(`tweet_${id}`)
    // Generate textarea in tweet cards
    tweet_area.innerHTML = 
    `<form id="edit-tweet">
        <div class="mb-3">
            <textarea class="form-control" id="edit_tweet_text" name="tweet_text" rows="2">${tweetText}</textarea>
        </div>
        <div id="tweet-btn">
            <input class="btn btn-info rounded-pill" type="submit" value="Save">
        </div>
    </form>`
    
    document.getElementById('edit-tweet').onsubmit = function(event) {
        // Prevent not to reload
        event.preventDefault()

        // Take value of edited textfield
        let edited_tweet = document.getElementById('edit_tweet_text').value;
        console.log(edited_tweet)

        fetch(`/tweet_id/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                tweet: edited_tweet
          })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data)
            tweet_area.innerHTML = edited_tweet
        })
        .catch((error) => {
            console.error('Error:', error)
        })
        return false;
    }
}

function like(id) {
    console.log(`${id}_like`)
    // Prevent not to reload
    event.preventDefault()
    // fetch(`/tweet_id/${id}`, {
    //     method: 'PUT',
    //     body: JSON.stringify({
    //         tweet: edited_tweet
    //   })
    // })
    let like_btn = document.getElementById(`${id}_like`)
    if (like_btn.className === "fa fa-heart") {
        like_btn.className = "fa fa-heart red-color"
    }
    else {
        like_btn.className = "fa fa-heart"
    }
}