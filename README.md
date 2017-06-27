# Mirror Mirror

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)]()

Mirror Mirror is a library for scraping publicly available images from social websites. It's purpose is to help show user's how much of their own data is truly available for anyone to see. Mirror Mirror scrapes every image url off of the profile page for a specified user, and then returns the uncompressed links.

---
## Walkthrough

Here is a walkthrough on how to begin collecting high resolution images using Mirror Mirror! All you need to do is download the script for the particular site that you want to scrape, or download `mirror-mirror.py`, which contains all methods in one convenient file.

To use Mirror Mirror, simply call the file through the command line. Then, fill in the `service`, and `username` arguments.

The complete syntax should look similar to the following, where `service` is the platform, and `username` is the username of the intended profile(s) to be scraped. More than one user may be scraped from the same service at a time.

```
python3 mirror-mirror.py <service> <username...>
```

That's all there is to it! This command line tool will return a list containing all scraped image links. If the profile does not exist, or the user account has no photos associated with it, the list will return empty.

---

## Supported services

* [Instagram](https://www.instagram.com)
* [Twitter](https://www.twitter.com)
* [VSCO](https://www.vsco.co)
* [Tinder](https://www.tinder.com)
* [OkCupid](https://www.okcupid.com)
