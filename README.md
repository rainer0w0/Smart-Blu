## Inspiration
The inspiration for Smart Blu came from a lack of quick access to utility usage tips in Counter-Strike. To new players, it can seem daunting to memorize dozens of lineups for grenades. We solve this by giving easy access to a database of grenade lineup references, accessible enough to be from right on the fly, whether it be for practice or mid-game.

## What it does
Smart Blu is a python project that acts as a virtual desk assistant. Its main function is to give users a way to pull up references to grenade lineups in the most convenient way possible. This makes it possible to pull grenade lineups in mid-round situations, where pulling your hands away from the keyboard and mouse could leave you vulnerable, and swing the tide of the round in the other team's favor. Not only are there dozens of grenade lineups already preloaded into Smart Blu, but it's as easy as adding reference material into a text document, and you can upload your own lineups to access at any time.

Smar Blu offers many secondary functions as well. It has a notification system to alert you of any player transfers that may have happened in the Counter-Strike scene, as well as easy access to a team's daily game from a simple voice command. It also has built-in twitch functionality, enabling you to look up and watch your favorite streamer on a completely separate device, leaving your computer free for playing games.

## How we built it
Smart Blu was built running python scripts on a raspberry pi 4. We take advantage of Google Cloud's Speech to Text API, which acts as our end-users input to get the info we are looking for. Our raspberry pi is connected to a MySQL database hosted on AWS, where we keep all of the grenade lineups, notifications, and stream alerts saved.

## Challenges we ran into
One of the biggest challenges of our project was trying to move everything from Windows (where it was originally scripted) over to our raspberry pi, which ran Linux. None of us had experience working with Python or Linux before this project, so there was a lot of trial and error we had to go through. We also had challenges relating to hardware in the form of our microphone dying partway into our project, forcing us to resort to using a stand-alone microphone in the final product.

## Accomplishments that we're proud of
Trying to be adventurous and use environments and resources we didn't have experience with in the past.

## What we learned
(Malcolm) I got more insight into software development, as well as how to use online APIs.

## What's next for Smart Blu
I'd love to add more features related to the CS Esports scene, as well as add functionality for other games past CS:GO. I think the idea of a desk assistant specifically for gaming is a really interesting idea that I would love to expand further on.
