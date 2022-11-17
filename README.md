# scrappy_asp.net
Sorting some difficulties when scrapping sites develped on asp.net

## This is an example of using Scrappy on asp.net site.

I'm sharing this becouse althou it looks trivial, I had some troubles trying to pull this off.

* The site scrapped doesn't give you links for changing page, so you must to configure the payload for making a form request.
* You will find those paramaters in payload.py. There is one payload to submit de first form and load the table, the next ones are for changing pages when selected page is out of bounds.
* In spiders folder there is spider_1.py that was an aptempt to do the work using selenium, but I think is not a good idea. Look for spider_2.py for the solution I found using only scrapy.
