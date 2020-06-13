# Final Project

Web Programming with Python and JavaScript

All three of my html pages, in all scenarios are completely mobile-responsive using media queries
I have used python to set up the django app and javascript for the main functionality of the webpage
I have used RSS feeds to get the news and have used callback functions in order to make sure that no matter the Wifi speed, the website will load, and the loader will only stop showing once it has been confirmed that the data has arrived.

In short, my NewsForYou Application is a Django app, and allows a multitude of users to sign in and login with new accounts, here they can add preferences for what news they like to see, and this will be updated everytime the website is refreshed (these preferences can be changed). It is largely a single page application as once logged in, all the functionality is on dashboard.html. Here, you can view the news from all the different sectors, hovering on the news title will flip it to show a description and a read more button which takes you to the article. I have also created a search bar as when I recieve the article, I store every word with the article, and you can search for any word, and if this word appears in either the title or summary of the article, it will show up. The search results are ordered by sectors.

The preferences of users are stored in a database, as are the RSS feeds.




