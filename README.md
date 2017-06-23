# Mirror Mirror

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)]()

Mirror Mirror is a library for scraping publicly available images from social websites. It's purpose is to help show user's how much of their own data is truly available for anyone to see. Mirror Mirror scrapes every image url off of the profile page for a specified user, and then returns the uncompressed links.

---
## Walkthrough

Here is a walkthrough on how to begin collecting high resolution images using Mirror Mirror! All you need to do is download the script for the particular site that you want to scrape, or download the master copy.

To use Mirror Mirror, simply fill in the `platform`, and pass the function the `username` argument.

The complete syntax should look similar to the following, where `instagram` is the platform, and `johndoe` is the username of the intended profile to be scraped.

```
scrape_instagram("johndoe")
```

That's all there is to it! Simply calling the function, and providing the `username` argument will return an array containing all scraped image links!

---

## Supported websites

* [Instagram](https://www.instagram.com)
* [Twitter](https://www.twitter.com)
* [VSCO](https://www.vsco.co)
* [Tinder](https://www.tinder.com)
