# [Scoop](https://scoop.sh/) buckets
[![Build Status](https://travis-ci.com/rasa/scoop-directory.svg)](https://travis-ci.com/rasa/scoop-directory "Build status")  [![Build Status](https://ci.appveyor.com/api/projects/status/github/rasa/scoop-directory?svg=true)](https://ci.appveyor.com/project/rasa/scoop-directory "Build Status")  [![Chat on Gitter](https://badges.gitter.im/lukesampson/scoop.svg)](https://gitter.im/lukesampson/scoop)  [![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE)  [![Mentioned in Awesome Scoop](https://awesome.re/mentioned-badge.svg)](https://github.com/h404bi/awesome-scoop/blob/master/README.md "Awesome Scoop")

View the Scoop Directory sorted by:

[bucket name](https://rasa.github.io/scoop-directory/by-bucket) | [number of apps](https://rasa.github.io/scoop-directory/by-apps) | [number of stars](https://rasa.github.io/scoop-directory/by-stars) | [number of forks](https://rasa.github.io/scoop-directory/by-forks) | [last updated](https://rasa.github.io/scoop-directory/by-date-updated) | [GitHub score](https://rasa.github.io/scoop-directory/by-score) ([deprecated](#Deprecated-pages)) | 

The above pages are updated daily.

To search the [known](https://github.com/lukesampson/scoop#known-application-buckets) scoop buckets for apps (as well as other well known buckets), please visit scoop-docs.now.sh's [search page](https://scoop-docs.now.sh/apps/).

[@mertd](https://github.com/mertd) created another search page at [shovel.sh](https://shovel.sh/search).

[@zhoujin7](https://github.com/zhoujin7) created the command-line search tool [scoop-search](https://github.com/zhoujin7/scoop-search) which searches the above pages. The search tool works with another command-line tool, called [crawl-scoop-directory](https://github.com/zhoujin7/crawl-scoop-directory), which scans the bucket lists and compiles a [Sqlite3 database](https://github.com/zhoujin7/crawl-scoop-directory/blob/master/scoop_directory.db) which can be downloaded from [here](https://github.com/zhoujin7/crawl-scoop-directory/raw/master/scoop_directory.db).

[@shilangyu](https://github.com/shilangyu) created another command-line search tool called [scoop-search](https://github.com/shilangyu/scoop-search) which can be installed via `scoop install scoop-search` which searches the buckets installed locally via `scoop bucket add [bucketname]`.

## Notes

A few buckets are excluded as they duplicate other buckets. The list of excluded buckets is [here](https://github.com/rasa/scoop-directory/blob/master/maintenance/github-crawler.py#L135).

## Deprecated pages

The [GitHub score](https://rasa.github.io/scoop-directory/by-score) page is deprecated as the GitHub API returns a score of `1` for every search result.

