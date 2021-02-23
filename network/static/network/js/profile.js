document.addEventListener('DOMContentLoaded', function() {
    // By default, load based on user
    let user = document.getElementById("username").textContent;
    load_page(user);
    // Button click for follow and unfollow
    // document.querySelector('#f-btn').addEventListener('click', follow);
});

function load_page(user) {
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

        };
    })
}

// function follow(user) {

//     const fo = document.querySelector('#f-btn').textContent;
//     console.log(fo)

//     fetch(`/follow/${user}`, {
//         method: 'PUT',
//         body: JSON.stringify({
//             follow: fo
//         })
//     })
//     .then(() => load_page(user))
// }