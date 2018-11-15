# clothes-matcher
HackDavis 2018 to improve on Google Shopping by matching one step further.

## Goal:
* Aggregate all shopping products from different companies onto one site.
* Allow user to look for more specific items based on selected images (which are closer to what they are looking for).

## Challenges:
* Creating a model that will successfully and accurately assess similarity between 2 images.
* Get enough quality product data (professionally taken images, product links, product title)

## Next Steps:
* Use NLP on product titles as another layer to assess similarity between products
* Train different models (convolutional autoencoder?), different loss functions, and different arcitectures for best results.
* Get more data.

## Files:
* App/app.py : Flask app with MySQL queries, receives similarity scores and displays top-k results
* img_to_category.ipynb : image file handling, training ResNet, return predictions, similarity ranking
* GoogleCrawler.py : web scraper to get different combinations of products from Google Shopping

## Tools Used:
* Tensorflow + Keras
* Google Cloud
* Python, Flask
* SQLite
* Javascript + JQuery


Coded by Varun Ved & me. *(+1 person last minute to help with front-end)*
