# [Scoop](https://scoop.sh/) Directory

[![update-index](https://github.com/rasa/scoop-directory/actions/workflows/update-index.yml/badge.svg)](https://github.com/rasa/scoop-directory/actions/workflows/update-index.yml) <!--
--> [![Build Status](https://ci.appveyor.com/api/projects/status/github/rasa/scoop-directory?svg=true)](https://ci.appveyor.com/project/rasa/scoop-directory "Build Status") <!--
--> [![Chat on Gitter](https://badges.gitter.im/lukesampson/scoop.svg)](https://gitter.im/lukesampson/scoop) <!--
--> [![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE) <!--
--> [![Mentioned in Awesome Scoop](https://awesome.re/mentioned-badge.svg)](https://github.com/h404bi/awesome-scoop/blob/master/README.md "Awesome Scoop")

View the Scoop Directory sorted by:

[bucket name](https://rasa.github.io/scoop-directory/by-bucket) | [number of apps](https://rasa.github.io/scoop-directory/by-apps) | [number of stars](https://rasa.github.io/scoop-directory/by-stars) | [number of forks](https://rasa.github.io/scoop-directory/by-forks) | [last updated](https://rasa.github.io/scoop-directory/by-date-updated) | [GitHub score](https://rasa.github.io/scoop-directory/by-score) ([deprecated](#Deprecated-pages)) | 

You can also [Search](https://rasa.github.io/scoop-directory/search) the Scoop Directory (put together by [@rashil2000](https://github.com/rashil2000)).

The above pages are updated daily.

There are several other Scoop application manifest search tools too:

1. [shovel.sh](https://shovel.sh/search) searches just the [known](https://github.com/mertd/shovel-data/blob/ad6133a10cd9f9f2d6e4a674542c429c5ce70209/shovel.go#L45) buckets. Created by [@mertd](https://github.com/mertd).

2. [scoop-search](https://github.com/zhoujin7/scoop-search) is a command line utility that searches the buckets found by scoop-directory. It works with another command-line tool, called [crawl-scoop-directory](https://github.com/zhoujin7/crawl-scoop-directory), which scans the bucket lists and compiles a [Sqlite3 database](https://github.com/zhoujin7/crawl-scoop-directory/blob/master/scoop_directory.db) which can be downloaded from [here](https://github.com/zhoujin7/crawl-scoop-directory/raw/master/scoop_directory.db). Created by [@zhoujin7](https://github.com/zhoujin7).

3. [scoop-search](https://github.com/shilangyu/scoop-search) is another command line search utility utility. It can be installed via `scoop install scoop-search` It  searches the buckets installed locally via `scoop bucket add [bucketname]`. Created by [@shilangyu](https://github.com/shilangyu).

## Notes

A few buckets are excluded as they duplicate other buckets. The list of excluded buckets is [here](https://github.com/rasa/scoop-directory/blob/master/maintenance/github-crawler.py#L135).

## Deprecated pages

The [GitHub score](https://rasa.github.io/scoop-directory/by-score) page is deprecated as the GitHub API returns a score of `1` for every search result.

