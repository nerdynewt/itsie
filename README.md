The internet today has become such a commercial place. You have corporate landing pages, huge conglomerate news sites, monopolistic social media sites and misleading clickbait sites meant to generate revenue through affiliate marketing. Personal websites and blogs, which might be some of the most original and genuine content you can find, are often buried or not shown at all in search results. (Contrary to popular belief, Google doens't actually have 6 million results for every search query. They only have about 200 hits after which results start repeating, most of these being commercial pages.)

Itsie tries to crawl the web while categorically avioding such commercial pages. Along with an explicit blacklist, itsie also has the ability to recognize and block new commercial sites it comes across, whether it be another listicle site or a random bank's landing page. It also comes with a convenient PHP web front-end that can be easily served, and which acts like any other search engine.

![screenshot](screenshot.png)

## Installation and Usage

### Quick Start

Clone the repository and install using `pip`:

```bash
git clone "https://github.com/nerdynewt/itsie" && pip install -e itsie
```

Now make a folder to store all your crawl data, and initialize it. (Or just use the `example` directory)

```bash
mkdir mycrawl
itsie --init
```

Now you can put a list of starting urls into `todo.txt`, one per line:
```bash
echo "https://www.splitbrain.org" >> todo.txt
```

If you feel like you have very few urls to start with, use the `--collect` flag first, which will give you a lot more urls into `todo.txt` without touching the database. This may be needed if your starting urls are detected to be too mainstream and are skipped/blocked outright.

```bash
itsie --collect --depth 2
```

Now you can run `itsie`, specifying the depth to crawl to. The depth defaults to 3. This will add all the indexed results into `itsie.db`. You can safely terminate the process any time by supplying a `KeyboardInterrupt`. This writes back the remaining urls and the ones found to disk, before exiting.

```bash
itsie --depth 2
```

To use the web PHP frontend, make sure that PHP is installed, along with its sqlite plugin. You might also have to [enable](https://wiki.archlinux.org/index.php/PHP#Sqlite) sqlite for php. On the crawl directory you chose, you'll find an `index.php` file, which is the interface. Start a development PHP server using:

```bash
php -S 0.0.0.0:8000
```

No navigate to <http://localhost:8000> on your browser, and start searching!

### Production

Although the above method works for your usage, if you are planning to host Itsie for public use, follow these additional steps. Basic knowledge in `MySQL` and web hosting are assumed.

- [Install MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) for your distribution/OS
- Make sure it is installed: `mysql --version`
- Enable/start the MySQL Server. Usually `systemctl start mariadb` or `systemctl start mysql`
- Log in to MySQL as root: `sudo mysql -u root -p`. Press enter when prompted for password
- Make a new user, create a database, and give the new user rights to the database. Change `username`, `PaSSwoRd` and `search_index` as needed.
```mysql
CREATE USER 'username'@'localhost' IDENTIFIED BY 'PaSSwoRd';
CREATE DATABASE search_index;
GRANT ALL PRIVILEGES ON search_index.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
quit
```

Now make a configuration file for `itsie` at either `~/.itsie/config.yaml` or `~/.config/itsie/config.yaml`, and add the following configuration options according to the credentials you just entered into `mysql`:

```yaml
mysql: True

sql:
	user: username
	password: PaSSwoRd
	database: search_index
```

Copy the `site` folder to the web root of a server of your choice. Make sure that:
- The server is set to work with `php` (ex. for `nginx`)
- `php` is [set up](https://wiki.archlinux.org/index.php/PHP#MySQL/MariaDB) to work with `MySQL`
- SSL, reverse-proxy etc. are set up

## Features

Itsie makes broad sweeping generalizations and assumptions on the present state of the internet and the needs of the user. So these aren't bugs, these are features:

### Blocklists

- *Completely ignores links to popular sites*: Big-business sites like Google, Facebook, YouTube, Twitter, etc are explicity ignored through a blocklist. Such links won't even be traversed.
- *Ignores News Sites*: Similarly, the blocklist also contains mainstream news sites like theguardian, nytimes, huffpost, etc.
- *Ignores _some_ listicle sites*: Same as above, think techcrunch, buzzfeed, etc

Of course, these can be bypassed by editing the blocklist as will be described, but that's not the intent. Traversing these sites would increase the crawl-list significantly without adding much original content. Also, this would be a fool's errand, as these sites are already indexed and served first-page by Google. If, however you _really_ want results from these sites, please use [this](https://google.com) search engine instead.

### More Important Features

- *Detects WordPress sites*: Simple WYSIWYG website generators like WordPress, Drupal, ASP.NET and Squarespace reduce the barrier for entry and therefore tends to produce bottom-of-the-barrel low-effort content mainly geared towards gaining the search system (muh SEO) and exploiting it for making money through ads and affiliate marketing. The CMS will be detected from the HTML header and if the site runs on such technologies, the domain will be put on a blacklist and ignored from then on.
- *Detects Corporate Landing Pages*: A good chunk of your crawl results will be the landing page to some random HR firm or a bank. Thankfully, such sites are practically carbon copies of each other. The crawler looks for common corporate buzzwords like "Privacy Policy", "Code of Conduct" or "Diversity" in the footer and adds these sites to a blocklist to be ignored.
- *No Traverse Loops*: The crawler visits the same domain only 15 times in total. So no loops.
- *JSON and HTML output*: You can find the results of the crawl as a `results.html` file or as a `search.json` file. I should probably use a database for this, but whatever.
- *Simple Javascript frontent*: There's a simple javascript frontend that reads `search.json` and performs the search client-side. This is bad practice, and I will probably set up a MySQL-PHP stack later. The search script and css are stolen from ronv's [Sidey](https://github.com/ronv/sidey) theme for Jekyll.

## Configuration

As of now, the script uses three files:

- `excludes.txt`: This is a list of regular expressions. Any link matching these will be ignored. By default, this file contains some popular sites, non-html links and ad/tracking/cdn subdomains. You can add sites you don't like here.
- `sinners.txt`: You don't have to edit this. This file is populated whenever the crawler encounters a website running on CMS-driven sites
- `corporates.txt`: A list of detected corporate landing pages. Again, you don't have to edit this, this is read from and written to automatically.

## Similar Projects

Although this is a Sunday-evening hackjob, there are a couple other projects that work similarly and are more fleshed out:

- [wiby](https://wiby.me): This is a simple website for the 'old web'. Only select websites chosen by the author are indexed, and they should agree to strict design guidelines (no flashy css, no javascript).
- [YaCy](https://yacy.net): This is a promising project and seeks to set up a decentralized network of crawlers and index-servers, which can be queried on search-time. However, in spite of the size of the network, the results are a bit lacking. Also, the project seems badly bloated, and is written in java with apparently only a confusing web-interface.

## Todo

- [ ] An actual database for indexed results, and LAMP framework
- [ ] KeyboardInterrupt Doesn't work? Have to `killall python`, lol
- [ ] Command-line arguments, more configuration options
- [ ] API for remote querying of indexed results


The internet today has become such a commercial place. You have corporate landing pages, huge conglomerate news sites, monopolistic social media sites and misleading clickbait sites meant to generate revenue through affiliate marketing. Personal websites and blogs, which might be some of the most original and genuine content you can find, are often buried or not shown at all. (Contrary to popular belief, Google doens't actually have 6 million results for every search query. They only have about 200 hits after which results start repeating, most of these being commercial pages.)

Itsie tries to crawl the web while categorically avioding such commercial pages. Along with an explicit blacklist, itsie also has the ability to recognize and block new commercial sites it comes across, whether it be another listicle site or a random bank's landing page. It also comes with a convenient PHP web front-end that can be easily served, and which acts like any other search engine.
