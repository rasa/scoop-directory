# [Scoop](https://scoop.sh/) Directory

[![update-index](https://github.com/rasa/scoop-directory/actions/workflows/update-index.yml/badge.svg)](https://github.com/rasa/scoop-directory/actions/workflows/update-index.yml) <!--
--> [![Build Status](https://ci.appveyor.com/api/projects/status/github/rasa/scoop-directory?svg=true)](https://ci.appveyor.com/project/rasa/scoop-directory "Build Status") <!--
--> [![Chat on Gitter](https://badges.gitter.im/lukesampson/scoop.svg)](https://gitter.im/lukesampson/scoop) <!--
--> [![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE) <!--
--> [![Mentioned in Awesome Scoop](https://awesome.re/mentioned-badge.svg)](https://github.com/h404bi/awesome-scoop/blob/master/README.md "Awesome Scoop") <!--
--> [![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/rasa/scoop-directory)

To [search](https://rasa.github.io/scoop-directory/search) the Scoop Directory click [here](https://rasa.github.io/scoop-directory/search) (put together by [@rashil2000](https://github.com/rashil2000)).

The search index contains over 18,000 manifests in over 1,600 buckets and is updated daily at 15:00 UTC.

You can also view the full list of all discovered applications sorted by:

1. [Bucket name](https://rasa.github.io/scoop-directory/by-bucket)
2. [Apps](https://rasa.github.io/scoop-directory/by-apps)
3. [Stars](https://rasa.github.io/scoop-directory/by-stars)
4. [Forks](https://rasa.github.io/scoop-directory/by-forks)
5. [Last updated](https://rasa.github.io/scoop-directory/by-date-updated)

There are several other Scoop application manifest search tools too:

1. [ScoopSearch](https://scoopsearch.github.io/) searches over 19,000 apps in over 900 buckets. Maintained by the [ScoopSearch](https://github.com/ScoopSearch) organization. Created by [@gpailler](https://github.com/gpailler).

2. [shovel.sh](https://shovel.sh/search) searches just the [known](https://github.com/mertd/shovel-data/blob/ad6133a10cd9f9f2d6e4a674542c429c5ce70209/shovel.go#L45) buckets. Created by [@mertd](https://github.com/mertd).

3. [scoop-search](https://github.com/zhoujin7/scoop-search) is a command line utility that searches the buckets found by scoop-directory.
It works with another command-line tool, called [crawl-scoop-directory](https://github.com/zhoujin7/crawl-scoop-directory), which scans the bucket lists and compiles a [Sqlite3 database](https://github.com/zhoujin7/crawl-scoop-directory/blob/master/scoop_directory.db) which can be downloaded from [here](https://github.com/zhoujin7/crawl-scoop-directory/raw/master/scoop_directory.db).
Created by [@zhoujin7](https://github.com/zhoujin7).

4. [scoop-search](https://github.com/shilangyu/scoop-search) is another command line search utility utility. It can be installed via `scoop install scoop-search` It  searches the buckets installed locally via `scoop bucket add [bucketname]`. Created by [@shilangyu](https://github.com/shilangyu).

5. [Repology](https://repology.org/projects/?inrepo=scoop) searches the Main, Extras, Versions and Games buckets, per [here](https://repology.org/repository/scoop).

## Notes

A few buckets are excluded as they duplicate other buckets. The list of excluded buckets is [here](https://github.com/rasa/scoop-directory/blob/master/maintenance/github-crawler.py#L135).
