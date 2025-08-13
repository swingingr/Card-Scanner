# Card-Scanner
A card scanning application used for the Pokemon TCG.

I have a large collection of Pokemon cards, and I was getting tired of not being able to remember which cards I owned. I decided to take matters into my own hands.
This program connects with a mobile phone using Iriun Webcam, then the user can scan a pokemon card. The boundaries of the card are discovered, and the card's picture is hashed before it is checked against a database of every hash for every pokemon card. The matching card is indicated, and it runs a check against my own personal database to see if I own that card.

The databse of hashes was created using a simple program to download images of every card, in chronological order, before doing the hashes and saving to a CSV. Originally, the program would run a series of hashes, then check against the databse 8 times per card to ensure the correct card was found and eliminate false positives. I decided to simplify this without sacrificing any of the certainty by turning each hash into a binary string, then concatenating them, so that all 8 hashes could be checked at once. This reduced the time between identifying the boundaries of the card and finding a match in the databse from 20 seconds to about .6 seconds.
