# frederikfrede.com
Portfolio site of Frederik Frede. Static HTML on GitHub Pages, branch `live`.

## Before committing
Run these in the site folder, in this order:

    node build-chrome.js       # nav and footer from footer.js into every page
    node build-grids.js        # homepage and Work grids into the HTML
    python3 build-llms-full.py # llms-full.txt from the page text
    node build-dates.js        # dateModified and sitemap lastmod, always last

## After a push has deployed

    node ping-indexnow.js      # tell Bing and others which pages changed
