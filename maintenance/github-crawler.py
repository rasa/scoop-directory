#!/usr/bin/env python
# -*- coding: utf-8 -*-
# """ @todo add docstring """

from __future__ import print_function

import copy
import io
import json
import os
import pickle
import pprint
import re
import shutil
import sqlite3
import stat
import sys
import time
from datetime import datetime
from typing import Any, Dict, List  # , Set, Tuple, Optional

import chardet
import git
import jinja2
import jsoncomment
import jsonschema
import requests

lmap = {
    "commercial": "https://en.m.wikipedia.org/wiki/Software_license#Proprietary_software_licenses",
    "freeware": "https://en.wikipedia.org/wiki/Freeware",
    "proprietary": "https://en.m.wikipedia.org/wiki/Software_license#Proprietary_software_licenses",
    "public_domain": "https://wiki.creativecommons.org/wiki/Public_domain",
    "public domain": "https://wiki.creativecommons.org/wiki/Public_domain",
    "public-domain": "https://wiki.creativecommons.org/wiki/Public_domain",
    "publicdomain": "https://wiki.creativecommons.org/wiki/Public_domain",
    "shareware": "https://en.wikipedia.org/wiki/Shareware",
}

# skip these as they are dups of other buckets
done = [
    "01walid/it-scoop",
    "go2sun/scoop-bucket-1",  # dup of https://github.com/dodorz/scoop
    "Kiedtl/open-scoop",  # https://travis-ci.org/rasa/scoop-directory/jobs/467750220#L642
    "kkzzhizhou/scoop-apps", # Aggregates other buckets
    "lukesampson/scoop", # No manifests    
    "mertd/shovel-data", # All manifests in a single file
    "nueko/scoop-php-ext",
    "pavanbijja/scoop-bucket",
    "Psychopovt/open-scoop",
    "Ranjizamadhu/scoop-bear",
    "rivy/scoop.bucket.scoop-main",
    "se35710/scoop-java",
]

max_pages = 15

searches = []

searches.append(
    {
        "pages": max_pages,
        "score": True,
        "searches": [
            "topic:scoop-bucket",
            "scoop-bucket",
            "scoop+bucket",
        ],
    }
)

searches.append(
    {
        "pages": max_pages,
        "score": True,
        "searches": [
            "scoop",
            # @todo regen this list
            "82p/scoop-yubico-bucket",
            "Aaike/scoop",
            "Alxandr/scoop-bucket",
            "Ash258/Scoop-Ash258",
            "AStupidBear/scoop-bear",
            "BjoernPetersen/scoop-misc-bucket",
            "Callidin/ragnar-scoop",
            "Congee/barrel",
            "DimiG/dgBucket",
            "Doublemine/scoops",
            "ErnWong/scoop-bucket",
            "Guard13007/ScoopBucket",
            "Jeddunk/scoop-bucket",
            "Jokler/scoop-bucket",
            "Lomeli12/ScoopBucket",
            "MCOfficer/scoop-bucket",
            "MCOfficer/scoop-nirsoft",
            "Sandex/scoop-supernova",
            "Southclaws/scoops",
            "TheLastZombie/scoop-bucket",
            "TheRandomLabs/Scoop-Bucket",
            "TheRandomLabs/Scoop-Python",
            "TheRandomLabs/Scoop-Spotify",
            "TnmkFan/my-bucket",
            "TorrentKatten/torrentkatten-scoop-bucket",
            "Utdanningsdirektoratet/PAS-scoop-public",
            "Vngdv/another-useless-scoop-bucket",
            "anurse/scoop-bucket",
            "bitrvmpd/scoop-wuff",
            "broovy/scoop-bucket",
            "comp500/scoop-browser",
            "comp500/scoop-comp500",
            "cprecioso/scoop-lektor",
            "deevus/scoop-games",
            "demas/demas-scoop",
            "dennislloydjr/scoop-bucket-devbox",
            "divanvisagie/scoop-bucket",
            "dooteeen/scoop-for-jp",
            "edgardmessias/scoop-pentaho",
            "excitoon/scoop-user",
            "ezhikov/scoop-bucket",
            "follnoob/follnoob-bucket",
            "fredjoseph/scoop-bucket",
            "furyfire/my-bucket",
            "galbro/my-bucket",
            "gexclaude/scoop-bucket",
            "ghchinoy/scoop-ce",
            "ghchinoy/scoop-roguewave",
            "goreleaser/scoop-bucket",
            "gpailler/scoop-apps",
            "guitarrapc/scoop-bucket",
            "h404bi/dorado",
            "hermanjustnu/scoop-emulators",
            "huangnauh/carrot",
            "iainsgillis/isg-bucket",
            "idursun/my-bucket",
            "jamesgecko/scoop-packages",
            "jat001/scoop-ox",
            "javageek/scoop-bucket",
            "jfut/scoop-jfut",
            "jfut/scoop-pleiades",
            "jmcarbo/scoopbucket",
            "kentork/scoop-leaky-bucket",
            "klaidliadon/scoop-buckets",
            "klauern/trackello-bucket",
            "liaoya/scoop-bucket",
            "lillicoder/scoop-openjdk6",
            "littleli/scoop-clojure",
            "littleli/Scoop-littleli",
            "lptstr/open-scoop",
            "lzimd/lzimd-scoop-bucket",
            "maman/scoop-bucket",
            "masaeedu/scoop-growlnotify",
            "masonm12/scoop-personal",
            "mattkang/scoop-bucket",
            "michaelxmcbride/scoop-michaelxmcbride",
            "mko-x/bucket",
            "mmichaelis/scoop-bucket",
            "monotykamary/toms-scoop-bucket",
            "narnaud/scoop-bucket",
            "nikolasd/scoop-bucket",
            "noquierouser/nqu-scoop",
            "nrakochy/scoop-solidity",
            "nsstrunks/scoop-bucket",
            "nueko/scoop-php",
            "nueko/scoop-php-ext",
            "ondr3j/scoop-misc",
            "pastleo/scoop-bucket",
            "pcrama/scoop-buckets",
            "pgollangi/scoop-bucket",
            "pigsflew/scoop-arbitrariae",
            "prezesp/scoop-viewer-bucket",
            "rasa/scoops",
            "rcqls/scoop-extras",
            "rivy/scoop.bucket-scoop.main",
            "rkolka/scoop-manifold",
            "se35710/scoop-ibm",
            "siddarthasagar/scoopbucket",
            "simonwjackson/my-bucket",
            "starise/Scoop-Confetti",
            "stlhrt/steel-buckets",
            "svkoh/scoop-bucket",
            "systemexitzero/scoop-bucket",
            "tapanchandra/scoop-personal",
            "thushan/scoop-devtools",
            "tditlu/scoop-amiga",
            "themrhead/scoop-bucket-apps",
            "toburger/scoop-buckets",
            "twxs/scoop-buckets",
            "vidarkongsli/vidars-scoop-bucket",
            "wangzq/scoop-bucket",
            "webwesen/webwesen-scoop-bucket",
            "wrokred/phpdev-scoop-bucket",
            "yt3r/test-bucket",
            "yuanying1199/scoopbucket",
            "yutahaga/scoop-bucket",
            "zhoujin7/tomato",
            "GreatGodApollo/trough",
        ],
    }
)


def fix_license(s):
    """@todo"""
    s = re.sub(r"-only", "", s, re.I)
    s = re.sub(r"-or-later", "+", s, re.I)
    s = re.sub(r"-Clause", "", s, re.I)
    return s


def do_license(v):
    """@todo"""
    url = ""
    identifier = ""
    if type(v).__name__ in ["unicode", "str"]:
        url = v
    if isinstance(v, dict):
        if "identifier" in v:
            identifier = fix_license(v["identifier"])
            url = ""
        if "url" in v:
            url = v["url"]
    if re.search(r"^(http|ftp)", url):
        if not identifier:
            identifier = "Link"
        return do_license_identifier(identifier, url)

    if not identifier:
        identifier = url

    return do_license_identifier(identifier, "")


def do_license_identifier(identifier, url):
    """@todo"""
    parts = re.split(r"[,\|]+", identifier)
    v = ""
    for part in parts:
        if v > "":
            v += "/"
        part = part.strip()
        if not url:
            k = part.lower()
            if k in OSImap:
                url = OSImap[k]
            elif k in lmap:
                url = lmap[k]
        if url > "":
            v += "[%s](%s)" % (fix_license(part), url)
        else:
            v += part
        break

    if len(parts) > 1:
        v += "&hellip;"

    return v


def get_license_id(v):
    """@todo"""
    url = ""
    identifier = ""
    if type(v).__name__ in ["unicode", "str"]:
        url = v
    if isinstance(v, dict):
        if "identifier" in v:
            identifier = fix_license(v["identifier"])
            url = ""
        if "url" in v:
            url = v["url"]

    if re.search(r"^(http|ftp)", url):
        return identifier

    if identifier:
        return fix_license(identifier)

    return fix_license(url)


def get_license_url(v):
    """@todo"""
    url = ""
    if type(v).__name__ in ["unicode", "str"]:
        url = v
    if isinstance(v, dict):
        if "url" in v:
            url = v["url"]

    if re.search(r"^(http|ftp)", url):
        return url
    return ""


def get_url(js):
    """@todo"""
    if "homepage" in js:
        return js["homepage"]
    if "checkver" in js:
        if "url" in js["checkver"]:
            return js["checkver"]["url"]
        if "github" in js["checkver"]:
            return js["checkver"]["github"]
    return ""


def get_link(js):
    """@todo"""
    if "url" in js:
        return js["url"]
    if "architecture" not in js:
        return None
    for bits in ["64bit", "32bit"]:
        if bits not in js["architecture"]:
            continue
        if "url" not in js["architecture"][bits]:
            continue
        return js["architecture"][bits]["url"]
    return None


def do_version(js):
    """@todo"""
    version = js["version"]
    if "checkver" not in js:
        version = "*%s*" % str(version).strip()
    return version


def fetchjson(urlstr):
    """@todo"""
    try_ = 0
    while try_ < MAX_TRIES:
        try_ += 1
        secs = 0
        response = requests.get(url=urlstr)
        if "X-RateLimit-Remaining" in response.headers:
            if int(response.headers["X-RateLimit-Remaining"]) < 1:
                reset = int(response.headers["X-RateLimit-Reset"])
                secs = float(reset) - time.time()
                if secs > -MAX_CLOCK_SKEW_SECONDS:
                    time.sleep(secs + MAX_CLOCK_SKEW_SECONDS)

        if response.status_code < 300:
            return response.json()

        if secs == 0:
            print("Sleeping %d seconds to avoid 403 errors" % SLEEP_SECONDS)
            time.sleep(SLEEP_SECONDS)

        # print("Try %d of %d:" % (try_, MAX_TRIES))
        pprint.pprint(dict(response.headers), width=1)
        if try_ + 1 < MAX_TRIES:
            print("Attempting try %d of %d" % (try_ + 1, MAX_TRIES))

    return {}


def get_builtins():
    """@todo"""
    # @todo load from
    # https://raw.githubusercontent.com/ScoopInstaller/Scoop/master/buckets.json
    bucket_list = {
        "main": "https://github.com/ScoopInstaller/Main",
        "extras": "https://github.com/ScoopInstaller/Extras",
        "versions": "https://github.com/ScoopInstaller/Versions",
        "nightlies": "https://github.com/ScoopInstaller/Nightlies",
        "nirsoft": "https://github.com/kodybrown/scoop-nirsoft",
        "php": "https://github.com/ScoopInstaller/PHP",
        "nerd-fonts": "https://github.com/matthewjberger/scoop-nerd-fonts",
        "nonportable": "https://github.com/TheRandomLabs/scoop-nonportable",
        "java": "https://github.com/ScoopInstaller/Java",
        "games": "https://github.com/Calinou/scoop-games",
        "jetbrains": "https://github.com/Ash258/Scoop-JetBrains",
    }
    for key in bucket_list:
        url = bucket_list[key]
        m = re.search(r"github\.com/(.*)$", url, re.I)
        if m:
            name = m.group(1)
            m = re.search(r"^(.*)\.git$", name, re.I)
            if m:
                name = m.group(1)
            builtins[name] = key
    return 0


def rmdir(dir):
    """@todo"""

    # https://stackoverflow.com/a/4829285/1432614

    def on_rm_error(func, path, exc_info):
        # logging.error('path=%s', path)
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        try:
            os.chmod(path, stat.S_IWRITE)
        except Exception:
            pass

        try:
            if os.path.isdir(path):
                return os.rmdir(path)
            if os.path.isfile(path):
                return os.unlink(path)
            return 0
        except Exception:
            return 1

    if not os.path.isdir(cache_dir):
        return True

    print('Deleting "%s"' % cache_dir)

    shutil.rmtree(cache_dir, onerror=on_rm_error)

    if not os.path.isdir(cache_dir):
        return True

    if os.name == "nt":
        print('rmdir /s /q "%s"' % cache_dir)
        os.system('cmd.exe /c rmdir /s /q "%s"' % cache_dir)

    return not os.path.isdir(cache_dir)


def initialize_cache():
    """@todo"""
    global cache
    global last_run

    rmdir(cache_dir)
    os.makedirs(cache_dir)

    try:
        with open(os.path.join(cache_dir, "cache.pickle"), "rb") as input_file:
            cache = pickle.load(input_file)
    except (EnvironmentError, EOFError):
        cache["last_run"] = datetime(2000, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

    last_run = datetime.strptime(cache["last_run"], "%Y-%m-%dT%H:%M:%SZ")
    return 0


def do_parse(file_path):
    """@todo"""
    try:
        with io.open(file_path, "rb") as fp:  # read binary
            json_data = fp.read()
    except Exception as e:
        return (str(e), None)

    h = {}
    h["encoding"] = "unknown"
    try:
        h = chardet.detect(json_data)
        try:
            with io.open(file_path, "r", encoding=h["encoding"]) as fp:
                json_data = fp.read()
        except Exception as e:
            return (str(e), None)
    except Exception:
        try:
            with io.open(file_path, "r") as fp:  # read non-binary
                json_data = fp.read()
        except Exception as e:
            return (str(e), None)

    parser = jsoncomment.JsonComment(json)

    try:
        j = parser.loads(json_data)
        rv = ""
        try:
            jsonschema.validate(j, scoop_schema_data)
            return ("", j)
        except Exception as e:
            err = str(e)
            err = parse_validation_error(err)
            # print(
            #    "\nError: Invalid json: %s:\n%s\n%s\n%s"
            #    % (os.path.basename(file_path), "=" * 80, err, "=" * 80)
            # )
            m = re.search(r"(Failed validating.*)", err)
            if m is not None:
                err = m.group(1)
            else:
                err = "Failed schema validation against %s" % scoop_schema_name
            print(err)
            rv = "%s %s" % (err, scoop_schema_name)

        return (rv, j)
    except Exception as e:
        # Strip out single line comments
        lines = json_data.splitlines()
        s = ""
        for line in lines:
            line = re.sub(r"^\s*//.*$", "", line)
            s += line + "\n"
        try:
            j = parser.loads(s)
        except Exception:
            j = None

        rv = "%s (%s)" % (str(e), h["encoding"])
        return (rv, j)


def parse_validation_error(err):
    """@todo"""
    try:
        m = re.match(r"(.*^On instance[^:]*:$)(.*)", err, re.MULTILINE | re.DOTALL)
        if m is not None:
            return m.group(1)
    except Exception as e:
        print(e)
        sys.exit()
    return err


def do_repo(repo, i, num_repos, do_score=True):
    """@todo"""
    global last_run

    keys = [
        # 'checkver',
        "description",
        # 'homepage',
        "license",
        "version",
    ]

    if "name" not in repo:
        pprint.pprint(dict(repo), width=1)
        return 0

    full_name = repo["full_name"]

    print("  %3d/%3d: %-50s: " % (i, num_repos, full_name), end="")
    nl = True

    if full_name == "ScoopInstaller/Scoop":
        print("Skipping ScoopInstaller/Scoop (no apps)")
        return 0

    if full_name.lower() in done:
        print("Skipping (done)")
        return 0

    done.append(full_name.lower())

    if repo["fork"]:
        print("Skipping (fork)")
        return 0

    # pprint.pprint(dict(repo), width=1)
    # sys.exit()

    repofoldername = full_name.replace("/", "+")
    git_clone_url = repo["git_url"]
    html_url = repo["html_url"]
    score = float(repo["score"])
    if not do_score:
        score = 0
    last_updated = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

    id_ = full_name.replace("/", "_")
    id_ = re.sub(r"[^0-9a-zA-Z_:.-]+", "-", id_)
    if not re.match(r"^[a-zA-Z]", id_[0]):
        id_ = "a" + id_

    if repofoldername not in cache:
        try:
            git.Repo.clone_from(git_clone_url, os.path.join(cache_dir, repofoldername))
        except Exception as e:
            if nl:
                print("")
                nl = False
            print(e)
            return 0

        try:
            description = repo["description"]
            if isinstance(description, list):
                description = " \n".join(description)
            description = description.strip()
        except Exception:
            description = ""

        builtin_text = ""
        if full_name in builtins:
            builtin_text = "scoop's built-in bucket '%s'" % builtins[full_name]
        if builtin_text:
            description += " (%s)" % builtin_text

        if description:
            idescription = " *%s*" % description
            cdescription = ": " + idescription
        else:
            idescription = ""
            cdescription = ""

        pattern = "%Y-%m-%dT%H:%M:%S"
        try:
            epoch = int(time.mktime(time.strptime(repo["updated_at"][:-1], pattern)))
        except Exception:
            epoch = 0

        cache[repofoldername] = {
            "cdescription": cdescription,
            "description": description,
            "entries": [],
            "epoch": epoch,
            "forks": int(repo["forks"]),
            "forks_url": html_url + "/network",
            "full_name": full_name,
            "id": id_,
            "idescription": idescription,
            "packages": 0,
            "score": score,
            "score5": round(score, 2),
            "size": int(repo["size"]),
            "stars": int(repo["stargazers_count"]),
            "stars_url": html_url + "/stargazers",
            "updated": repo["updated_at"][2:10].replace("-", "&#x2011;"),
            "updated_at": repo["updated_at"].replace("-", "&#x2011;"),
            "updated_url": html_url + "/commits",
            "url": html_url,
            "default_branch": repo["default_branch"],
        }

    elif repofoldername in cache and (last_updated > last_run):
        repo = git.Repo(os.path.join(cache_dir, repofoldername))
        o = repo.remotes.origin
        try:
            o.pull()
        except Exception as e:
            if nl:
                print("")
                nl = False
            print(e)

    if not os.path.isdir(os.path.join(cache_dir, repofoldername)):
        return 0

    cache[repofoldername]["entries"] = []

    bucket = ""
    bucket_path = os.path.join(cache_dir, repofoldername)
    if os.path.isdir(bucket_path + "/bucket"):
        bucket = "/bucket"
        bucket_path = bucket_path + "/bucket"

    rows = {}

    jsons = 0
    good_jsons = 0
    for f in os.listdir(bucket_path):
        file_path = os.path.join(bucket_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.path.splitext(file_path)[1] != ".json":
            continue

        jsons += 1
        row = {}
        for key in keys:
            row[key] = ""
        row["json"] = os.path.splitext(f)[0]

        while True:
            (parse_error, j) = do_parse(file_path)

            if len(parse_error) > 0:
                if nl:
                    print("")
                    nl = False
                print("    %s: %s" % (f, parse_error))
                if not j:
                    break

            if not get_link(j):
                if nl:
                    print("")
                    nl = False
                print("    %s: no url" % f)
                break

            if "version" not in j:
                if nl:
                    print("")
                    nl = False
                print("    %s: no version" % f)
                break

            try:
                row["url"] = get_url(j)
            except Exception as e:
                if nl:
                    print("")
                    nl = False
                print(f)
                print(e)
                break

            default_branch = cache[repofoldername]["default_branch"]
            manifest_url = "%s/blob/%s%s/%s" % (html_url, default_branch, bucket, f)
            row["manifest_url"] = manifest_url
            if not row["url"]:
                row["url"] = row["manifest_url"]
            row["license_id"] = ""
            row["license_url"] = "#"
            for key in keys:
                if key not in j:
                    continue

                v = j[key]
                is_string = isinstance(v, str) or type(v).__name__ == "unicode"
                if is_string:
                    v = v.strip()
                    v = re.sub(r"[\r\n]+", " ", v)
                if key == "license":
                    row["license_id"] = get_license_id(v)
                    row["license_url"] = get_license_url(v)
                    if row["license_id"] == "":
                        row["license_id"] = "Undefined"
                    v = do_license(v)
                if key == "version":
                    v = do_version(j)
                    if row["manifest_url"]:
                        v = "[%s](%s)" % (v, row["manifest_url"])

                try:
                    if isinstance(v, list):
                        if key == "description":
                            v = " \n".join(v)
                    v = v.strip()
                    v = re.sub(r"[\r\n]+", " ", v)
                    row[key] = v
                except Exception as e:
                    if nl:
                        print("")
                        nl = False
                    print(f)
                    print(e)
                    parse_error = str(e)
                # @TODO add bits/exes,shortcuts
                # https://png.icons8.com/android/48/000000/ok.png
                # https://png.icons8.com/android/48/000000/32bit.png
                # https://png.icons8.com/android/48/000000/64bit.png
                # exes
                # shortcuts
            if len(parse_error) > 0:
                row["description"] += " (**%s**)" % parse_error
                break
            good_jsons += 1
            break

        rows[row["json"]] = row

    for k in sorted(rows.keys(), key=lambda s: s.lower()):
        cache[repofoldername]["entries"].append(rows[k])

    if good_jsons == 0:
        cache[repofoldername]["entries"] = []

    cache[repofoldername]["packages"] = len(cache[repofoldername]["entries"])
    if not nl:
        print("%-61s: " % "", end="")

    print("%3d (score:%10.6f)" % (len(cache[repofoldername]["entries"]), repo["score"]))
    return len(cache[repofoldername]["entries"])


def do_page(search, page, do_score=True):
    """@todo"""
    api = "https://api.github.com/search/repositories?q=%s&per_page=%d"

    url = api % (search, per_page)
    if page > 1:
        url += "&page=%d" % page
    rv = fetchjson(url)
    if "items" not in rv:
        print("items not found in search results")
        return 0
    repos = rv["items"]
    i = 0
    hits = 0
    for repo in repos:
        i += 1
        hits += do_repo(repo, i, len(repos), do_score)
        if SHORT_CIRCUIT:
            break

    return hits


def do_search(search, pages=1, do_score=True):
    """@todo"""
    for page in range(1, pages + 1):
        print("q: %s (page %s of %s)" % (search, page, pages))
        hits = do_page(search, page, do_score)
        if hits == 0:
            break
        if SHORT_CIRCUIT:
            return 0
    return 0


def do_searches():
    """@todo"""
    searches[1]["searches"].extend(builtins)
    for h in searches:
        for search in h["searches"]:
            if search.lower() in done:
                continue
            do_search(search, h["pages"], h["score"])
            if SHORT_CIRCUIT:
                return 0

    return 0


def save_cache():
    """@todo"""
    global cache

    print("Saving cache")
    cache["last_run"] = datetime.strftime(
        datetime.now().replace(hour=0, minute=0, second=0), "%Y-%m-%dT%H:%M:%SZ"
    )

    try:
        with open(os.path.join(cache_dir, "cache.pickle"), "wb") as input_file:
            pickle.dump(cache, input_file)
    except EnvironmentError:
        pass

    return 0


def sort_repos(first_sort_key, sort_in_reverse):
    """@todo"""
    global repos_by_score
    global repos_by_name

    print("Sorting output")
    repos = [repo for repo in cache.keys()]
    repos_by_score = [
        repo for repo in repos if repo != "last_run" and len(cache[repo]["entries"]) > 0
    ]
    repos_by_score = sorted(
        repos_by_score,
        key=lambda repo: (
            cache[repo][first_sort_key],
            cache[repo]["score"],
            cache[repo]["stars"],
            cache[repo]["forks"],
            cache[repo]["packages"],
            cache[repo]["full_name"].lower(),
        ),
        reverse=sort_in_reverse,
    )

    repos_by_name = copy.deepcopy(repos_by_score)
    repos_by_name = sorted(
        repos_by_name, key=lambda repo: cache[repo]["full_name"].lower()
    )
    return True


def do_render(filename, sort_order_description):
    """@todo"""
    print("Generating %s" % filename)
    TEMPLATE_ENVIRONMENT = jinja2.Environment(
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.join(dir_path, "template")),
        trim_blocks=False,
    )
    context = {
        "repos_by_score": repos_by_score,
        "repos_by_name": repos_by_name,
        "cache": cache,
        "sort_order_description": sort_order_description,
    }
    tpl = "ReadmeTemplate.md"
    markdown_content = TEMPLATE_ENVIRONMENT.get_template(tpl).render(context)
    with io.open(filename, "w+", encoding="utf-8", newline="\n") as f:
        written = f.write(markdown_content)
        lines = len(markdown_content.splitlines())
        print("Wrote %d bytes (%s lines) to %s" % (written, lines, filename))
    return True


def do_readme(sort_field, output_file, sort_order_description, sort_in_reverse):
    """@todo"""
    filename = os.path.realpath(os.path.join(dir_path, "..", output_file))
    # if not os.path.isfile(filename):
    #    print("File not found: %s" % filename)
    #    return False
    sort_repos(sort_field, sort_in_reverse)
    do_render(filename, sort_order_description)
    return True


def do_db():
    """@todo"""
    scoop_directory_db = os.path.join(dir_path, "..", "scoop_directory.db")
    print("Regenerating ", scoop_directory_db)
    conn = sqlite3.connect(scoop_directory_db)

    cur = conn.cursor()

    sqls = [
        "drop table if exists apps",
        "drop table if exists buckets",
        """create table apps (
                    name text COLLATE NOCASE,
                    version text,
                    description text COLLATE NOCASE,
                    license text,
                    homepage text,
                    manifest_url text,
                    bucket_url text COLLATE NOCASE,
                    license_url text,
                    bucket text COLLATE NOCASE)""",
        """create table buckets (
                    bucket_url text,
                    description text,
                    packages integer,
                    stars integer,
                    updated text)""",
    ]
    for sql in sqls:
        print("Executing ", sql)
        cur.execute(sql)

    buckets = 0
    total_manifests = 0

    for bucket in cache:
        if bucket == "last_run":
            continue
        buckets += 1
        print("Inserting bucket %d: %s" % (buckets, cache[bucket]["url"]))
        cur.execute(
            "insert into buckets values (?, ?, ?, ?, ?)",
            (
                cache[bucket]["url"],
                cache[bucket]["description"],
                cache[bucket]["packages"],
                cache[bucket]["stars"],
                cache[bucket]["updated"],
            ),
        )

        manifests = 0
        for manifest in cache[bucket]["entries"]:
            manifests += 1
            try:
                json = manifest["json"]
                version = (
                    manifest["version"].split("[", 1)[1].split("]")[0]
                    if manifest["version"] != ""
                    else ""
                )
                description = manifest["description"]
                license_id = manifest["license_id"] if "license_id" in manifest else ""
                url = manifest["url"] if "url" in manifest else ""
                manifest_url = (
                    manifest["manifest_url"] if "manifest_url" in manifest else ""
                )
                bucket_url = cache[bucket]["url"]
                license_url = (
                    manifest["license_url"] if "license_url" in manifest else ""
                )
                bucket_name = re.sub("^https?://[a-z0-9.-]+/", "", bucket_url, re.I)
                cur.execute(
                    "insert into apps values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        json,
                        version,
                        description,
                        license_id,
                        url,
                        manifest_url,
                        bucket_url,
                        license_url,
                        bucket_name,
                    ),
                )
            except Exception as e:
                print("Error inserting manifest %d: " % manifests)
                print(e)
                print("%-12s: %s" % ("json", json))
                print("%-12s: %s" % ("version", version))
                print("%-12s: %s" % ("description", description))
                print("%-12s: %s" % ("license_id", license_id))
                print("%-12s: %s" % ("url", url))
                print("%-12s: %s" % ("manifest_url", manifest_url))
                print("%-12s: %s" % ("bucket_url", bucket_url))
                print("%-12s: %s" % ("license_url", license_url))

        print("Added %d manifests" % manifests)
        total_manifests += manifests

    print("Inserted %d manifests in %d buckets" % (total_manifests, buckets))
    conn.commit()
    print("Closing connection")
    conn.close()
    return 0


def main():
    """@todo"""
    get_builtins()
    initialize_cache()
    do_searches()
    save_cache()
    # GitHub truncates the readme
    # do_readme('score', 'README.md', 'Github score', True)
    # do_readme('score', 'by-score.md', 'Github score', True)
    do_readme("full_name", "by-bucket.md", "bucket name", False)
    do_readme("packages", "by-apps.md", "number of apps", True)
    do_readme("stars", "by-stars.md", "number of stars", True)
    do_readme("forks", "by-forks.md", "number of forks", True)
    do_readme("epoch", "by-date-updated.md", "date last updated", True)
    do_readme("score", "by-score.md", "Github score", True)
    do_db()
    return 0


MAX_CLOCK_SKEW_SECONDS = 10
MAX_TRIES = 3
SLEEP_SECONDS = 75
SHORT_CIRCUIT = False

builtins = {}  # type: Dict[str, str]
cache = {}  # type: Dict[str, Any]
dir_path = os.path.dirname(os.path.realpath(__file__))
last_run = None
# https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#pagination
per_page = 100  # Max is 100
repos_by_score = []  # type: List[str]
repos_by_name = []  # type: List[str]

vendor_dir = os.path.join(dir_path, "..", "vendor")
license_dir = os.path.join(vendor_dir, "spdx/license-list-data/json")
licenses_json = os.path.join(license_dir, "licenses.json")
exceptions_json = os.path.join(license_dir, "exceptions.json")
scoop_schema_name = "ScoopInstaller/Scoop/schema.json"
scoop_schema_json = os.path.join(vendor_dir, scoop_schema_name)

OSImap = {}
with open(licenses_json) as fh:
    obj = json.load(fh)
    licenses = obj["licenses"]
    for license in licenses:
        OSImap[license["licenseId"].lower()] = license["reference"]
with open(exceptions_json) as fh:
    obj = json.load(fh)
    exceptions = obj["exceptions"]
    for license in exceptions:
        OSImap[license["licenseExceptionId"].lower()] = license["reference"]

with open(scoop_schema_json, "r") as fh:
    scoop_schema_data = json.load(fh)

cache_dir = os.path.join(dir_path, "cache")
if "CACHE_ROOT" in os.environ:
    cache_root = os.environ["CACHE_ROOT"]
else:
    cache_root = dir_path

if not re.search(r"cache$", cache_root):
    cache_dir = os.path.join(cache_root, "cache")

# @todo change to startup option
if len(sys.argv) > 1:
    SHORT_CIRCUIT = True

if SHORT_CIRCUIT:
    per_page = 1
    max_pages = 1
    searches[0]["pages"] = max_pages
    searches[1]["pages"] = max_pages
    searches[1]["searches"] = ["scoop"]

sys.exit(main())
