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
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Dict, List  # , Set, Tuple, Optional
from urllib.parse import urlencode, urlsplit  # python3

import chardet
import git
import jinja2
import jsoncomment
import jsonschema
import pandas
import requests
import requests.auth


def url_to_repo_name(url):
    """@todo"""
    path = urlsplit(url).path
    path = path[1:]
    (base, ext) = os.path.splitext(path)
    return base


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
        # https://github.com/rasa/scoop-directory/runs/4684777541?check_suite_focus=true#step:5:3106
        if isinstance(js["homepage"], list):
            return js["homepage"][0]
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
    global max_pages

    request_headers = {}
    if os.getenv("GITHUB_TOKEN"):
        request_headers["Authorization"] = "token " + os.getenv("GITHUB_TOKEN")
    elif len(sys.argv) > 1 and len(sys.argv[1]) == 40:
        request_headers["Authorization"] = "token " + sys.argv[1]

    sleep_seconds = SLEEP_SECONDS
    while sleep_seconds <= MAX_SLEEP_SECONDS:
        # print("url=%s" % urlstr)
        response = requests.get(url=urlstr, headers=request_headers)  # auth=basicAuth
        max_pages = 1
        if "Link" in response.headers:
            link = response.headers["Link"]
            m = re.search(r"""&page=(\d+)>?;\s*rel="last".?""", link)
            if m is not None:
                pages = m.group(1)
                if int(pages) > 0:
                    max_pages = int(pages)
                if MAX_SEARCHES < 99 and MAX_SEARCHES < max_pages:
                    max_pages = MAX_SEARCHES

        if response.status_code < 300:
            return response.json()

        if response.status_code == 422:  # reached 1,000 search limit
            return response.json()

        if response.status_code == 403:
            limit = int(response.headers["X-RateLimit-Limit"])
            remaining = int(response.headers["X-RateLimit-Remaining"])
            reset = int(response.headers["X-RateLimit-Reset"])
            waitSeconds = float(reset) - time.time()
            if remaining < 1:
                if waitSeconds > sleep_seconds:
                    sleep_seconds = waitSeconds
            print(
                "  limit=%d remaining=%d reset=%d (%d seconds from now) (sleeping %d seconds)"
                % (limit, remaining, reset, waitSeconds, sleep_seconds)
            )
            time.sleep(sleep_seconds)
            sleep_seconds = sleep_seconds * 2
            continue

        print("  Received status_code %d" % response.status_code)
        pprint.pprint(response.json())
        return response.json()

    return {}


def rmdir(path):
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

    if not os.path.isdir(path):
        return True

    # print('Deleting "%s"' % path)

    shutil.rmtree(path, onerror=on_rm_error)

    if not os.path.isdir(path):
        return True

    if os.name == "nt":
        # print('rmdir /s /q "%s"' % path)
        os.system('cmd.exe /c rmdir /s /q "%s"' % path)

    return not os.path.isdir(path)


def initialize_cache():
    """@todo"""
    global cache
    global last_run

    if os.getenv("DELETE_CACHE"):
        rmdir(cache_dir)

    if not os.path.isdir(cache_dir):
        print("Initializing cache at %s" % cache_dir)
        os.makedirs(cache_dir)

    try:
        with open(cache_pickle, "rb") as input_file:
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
            if re.search(r"additionalProperties", err):
                return (rv, j)
            rv = err

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


def do_clone(url, path):
    """@todo"""
    try:
        if not os.path.isdir(path):
            git.Repo.clone_from(url, path, depth=1)
        else:
            repo = git.Repo(path)
            o = repo.remotes.origin
            o.pull()
    except Exception as e:
        return str(e)
    return ""


def do_repo(repo, i, num_repos, do_score=True):
    """@todo"""
    failure = -1
    global last_run

    keys = [
        # 'checkver',
        "description",
        # 'homepage',
        "license",
        "version",
    ]

    if "name" not in repo:
        print("Unexpected response:")
        pprint.pprint(dict(repo), width=1)
        return failure

    full_name = repo["full_name"]
    full_name_lower = full_name.lower()

    nl = True

    if full_name_lower in done:
        print("Skipping (%s)" % done[full_name_lower])
        return failure

    if repo["fork"]:
        add_exclusion(repo, "fork")
        return failure

    repofoldername = full_name.replace("/", "+")
    git_clone_url = repo["clone_url"]
    html_url = repo["html_url"]
    score = float(repo["score"])
    if not do_score:
        score = 0
    last_updated = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

    id_ = full_name.replace("/", "_")
    id_ = re.sub(r"[^0-9a-zA-Z_:.-]+", "-", id_)
    if not re.match(r"^[a-zA-Z]", id_[0]):
        id_ = "a" + id_
    repo_dir = os.path.join(cache_dir, repofoldername)

    if repofoldername not in cache:
        errmsg = do_clone(git_clone_url, repo_dir)
        if errmsg:
            if nl:
                print("")
            print(errmsg)
            return failure

        try:
            description = repo["description"]
            if isinstance(description, list):
                description = " \n".join(description)
            description = description.strip()
            description = description.replace("|", "\\|")
        except Exception:
            description = ""

        builtin_text = ""
        if full_name_lower in builtins:
            builtin_text = "scoop's built-in bucket '%s'" % builtins[full_name_lower]
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
        errmsg = do_clone(git_clone_url, repo_dir)
        if errmsg:
            if nl:
                print("")
            print(errmsg)
            return failure

    if not os.path.isdir(repo_dir):
        return failure

    cache[repofoldername]["entries"] = []

    bucket = ""
    bucket_path = repo_dir
    if os.path.isdir(bucket_path + "/bucket"):
        bucket = "/bucket"
        bucket_path = bucket_path + "/bucket"

    rows = {}

    jsons = 0
    good_jsons = 0
    malformed = 0
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
                # if nl:
                #     print("")
                #    nl = False
                # print("        %s: %s" % (f, parse_error))
                if not j:
                    break

            if not get_link(j):
                # if nl:
                #     print("")
                #     nl = False
                # print("    %s: no url" % f)
                break

            if "version" not in j:
                # if nl:
                #     print("")
                #     nl = False
                # print("    %s: no version" % f)
                break

            try:
                row["url"] = get_url(j)
            except Exception:
                # if nl:
                #     print("")
                #     nl = False
                # print("    %s: %s" % (f, str(e)))
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
                    # if nl:
                    #     print("")
                    #     nl = False
                    # print(f)
                    # print(e)
                    parse_error = str(e)
                # @TODO add bits/exes,shortcuts
                # https://png.icons8.com/android/48/000000/ok.png
                # https://png.icons8.com/android/48/000000/32bit.png
                # https://png.icons8.com/android/48/000000/64bit.png
                # exes
                # shortcuts
            if len(parse_error) > 0:
                malformed += 1
                row["description"] += " [<em>%s</em>]" % parse_error
                break
            good_jsons += 1
            break

        rows[row["json"]] = row

    for k in sorted(rows.keys(), key=lambda s: s.lower()):
        cache[repofoldername]["entries"].append(rows[k])

    if good_jsons == 0:
        # disabling for now due to false positives, per 
        # https://github.com/ScoopSearch/ScoopSearch.AzureFunctions/issues/7#issuecomment-1019670879
        # add_exclusion(repo, "no manifests")
        cache[repofoldername]["entries"] = []
    else:
        done[full_name_lower] = "processed"

    cache[repofoldername]["packages"] = len(cache[repofoldername]["entries"])
    # if not nl:
    #     print("%-61s: " % "", end="")

    bad_jsons = jsons - good_jsons
    msg = ""
    if good_jsons:
        msg = f"{good_jsons:,}"
        if bad_jsons:
            msg += f"/{jsons:,} ({bad_jsons:,} bad)"
        if malformed:
            msg += f" ({malformed:,} malformed)"
    if msg:
        print(msg)
    return len(cache[repofoldername]["entries"])


def add_exclusion(repo, reason):
    """@todo"""
    full_name_lower = repo["full_name"].lower()
    if full_name_lower in done:
        print("Already excluded (%s)" % done[full_name_lower])
        return 0

    print("Excluding (%s)" % reason)
    with open(exclude_txt, "a", newline="\n") as fh:
        fh.write("%s,%s\n" % (repo["clone_url"], reason))

    done[full_name_lower] = reason

    repofoldername = repo["full_name"].replace("/", "+")
    repo_dir = os.path.join(cache_dir, repofoldername)
    try:
        rmdir(repo_dir)
    except Exception as e:
        print(e)

    return 0


def do_page(search, page, do_score=True):
    """@todo"""
    vars = {
        "q": search,
        "per_page": per_page,
    }
    if page > 1:
        vars["page"] = page
    query_string = urlencode(OrderedDict(vars))
    url = "https://api.github.com/search/repositories?" + query_string
    rv = fetchjson(url)
    if "message" in rv:
        if re.search(r"Only the first \d+ search results are available", rv["message"]) is None:
            print("message found in search results:")
            pprint.pprint(rv)
        return 0
    if "items" not in rv:
        print("items not found in search results:")
        pprint.pprint(rv)
        return 0
    repos = rv["items"]
    i = 0
    hits = 0
    for repo in repos:
        i += 1
        print(
            "%s: page %2d/%2d: repo %3d/%3d: %-40s: " % (search, page, max_pages, i, len(repos), repo["full_name"]),
            end="",
        )
        results = do_repo(repo, i, len(repos), do_score)
        if results <= 0:
            continue
        hits += results
        if i >= MAX_SEARCHES:
            break

    return hits


def do_search(search, do_score=True):
    """@todo"""
    global max_pages
    total_hits = 0
    for page in range(1, max_pages + 1):
        hits = do_page(search, page, do_score)
        total_hits += hits
        if hits == 0:
            break
        if page >= max_pages:
            break
        if MAX_SEARCHES < 99:
            break
    return total_hits


def do_searches():
    """@todo"""
    global max_pages
    searches[0]["searches"].extend(builtins)
    for h in searches:
        for search in h["searches"]:
            if search.lower() in done:
                continue
            max_pages = START_MAX_PAGES
            total_hits = do_search(search, h["score"])
            if total_hits > 0 and MAX_SEARCHES < 99:
                return 0

    return 0


def save_cache():
    """@todo"""
    global cache

    print("Saving cache")
    cache["last_run"] = datetime.strftime(datetime.now().replace(hour=0, minute=0, second=0), "%Y-%m-%dT%H:%M:%SZ")

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
    repos_by_score = [repo for repo in repos if repo != "last_run" and len(cache[repo]["entries"]) > 0]
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
    repos_by_name = sorted(repos_by_name, key=lambda repo: cache[repo]["full_name"].lower())
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
        "drop table if exists buckets",
        "drop table if exists apps",
        """create table buckets (
            id integer,
            bucket_url text,
            description text COLLATE NOCASE,
            packages integer,
            stars integer,
            updated text
        )""",
        """create table apps (
            name text COLLATE NOCASE,
            version text,
            description text COLLATE NOCASE,
            license text,
            homepage text,
            manifest_url text,
            bucket_url text,
            license_url text,
            bucket text COLLATE NOCASE,
            bucket_id integer
        )""",
        "CREATE INDEX idx_buckets_id ON buckets (id)",
        "CREATE INDEX idx_apps_name ON apps (name)",
        "CREATE INDEX idx_apps_description ON apps (description)",
        "CREATE INDEX idx_apps_bucket ON apps (bucket)",
        "CREATE INDEX idx_apps_bucket_id ON apps (bucket_id)",
    ]
    for sql in sqls:
        print("Executing ", sql)
        cur.execute(sql)

    scanned = 0
    bucket_id = 0
    total_manifests = 0

    for bucket in cache:
        scanned += 1
        if bucket == "last_run":
            continue
        if not cache[bucket]["entries"]:
            # print("Skipping %s: no manifests" % (cache[bucket]["url"]))
            continue
        bucket_id += 1
        # print("Inserting bucket %d: %s" % (bucket_id, cache[bucket]["url"]))
        cur.execute(
            "insert into buckets values (?, ?, ?, ?, ?, ?)",
            (
                bucket_id,
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
                version = manifest["version"].split("[", 1)[1].split("]")[0] if manifest["version"] != "" else ""
                description = manifest["description"]
                license_id = (
                    manifest["license_id"] if "license_id" in manifest else ""
                )  # fmt: skip
                url = manifest["url"] if "url" in manifest else ""
                manifest_url = manifest["manifest_url"] if "manifest_url" in manifest else ""
                bucket_url = cache[bucket]["url"]
                license_url = manifest["license_url"] if "license_url" in manifest else ""
                bucket_name = re.sub(r"^https?://[a-z0-9.-]+/", "", bucket_url, re.I)
                cur.execute(
                    "insert into apps values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                        bucket_id,
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

        # print("Added %d manifests" % manifests)
        total_manifests += manifests

    print("Inserted %d manifests and %d buckets (from %d repos)" % (total_manifests, bucket_id, scanned))
    conn.commit()
    print("Closing connection")
    conn.close()
    return 0


def main():
    """@todo"""
    start = time.time()
    initialize_cache()
    do_searches()
    save_cache()
    # GitHub truncates the readme
    # do_readme('score', 'README.md', 'Github score', True)
    do_readme("score", "by-score.md", "Github score", True)
    do_readme("full_name", "by-bucket.md", "bucket name", False)
    do_readme("packages", "by-apps.md", "number of apps", True)
    do_readme("stars", "by-stars.md", "number of stars", True)
    do_readme("forks", "by-forks.md", "number of forks", True)
    do_readme("epoch", "by-date-updated.md", "date last updated", True)
    do_db()
    elapsed = time.time() - start
    print("Elapsed: %s (%d seconds)" % ("{:0>8}".format(str(timedelta(seconds=elapsed))), elapsed))

    return 0


MAX_CLOCK_SKEW_SECONDS = 10
MAX_TRIES = 6
SLEEP_SECONDS = 60
MAX_SLEEP_SECONDS = SLEEP_SECONDS * 64  # 3840: 1 hour, 4 minutes
MAX_SEARCHES = 99
START_MAX_PAGES = 10

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

builtins = {}  # type: Dict[str, str]
cache = {}  # type: Dict[str, Any]
dir_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
last_run = None
max_pages = START_MAX_PAGES
# https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#pagination
per_page = 100  # Max is 100
repos_by_score = []  # type: List[str]
repos_by_name = []  # type: List[str]

base_dir = os.path.normpath(os.path.join(dir_path, ".."))
cache_dir = os.path.normpath(os.path.join(base_dir, "cache"))
vendor_dir = os.path.normpath(os.path.join(base_dir, "vendor"))
license_dir = os.path.normpath(os.path.join(vendor_dir, "spdx/license-list-data/json"))

if "CACHE_ROOT" in os.environ:
    cache_dir = os.environ["CACHE_ROOT"]
    if not re.search(r"cache$", cache_dir, re.I):
        cache_dir = os.path.normpath(os.path.join(cache_dir, "cache"))

cache_pickle = os.path.normpath(os.path.join(cache_dir, "cache.pickle"))
buckets_json = os.path.normpath(os.path.join(vendor_dir, "ScoopInstaller/Scoop/buckets.json"))
scoop_schema_name = "ScoopInstaller/Scoop/schema.json"
scoop_schema_json = os.path.normpath(os.path.join(vendor_dir, scoop_schema_name))

licenses_json = os.path.normpath(os.path.join(license_dir, "licenses.json"))
exceptions_json = os.path.normpath(os.path.join(license_dir, "exceptions.json"))

include_txt = os.path.normpath(os.path.join(base_dir, "include.txt"))
exclude_txt = os.path.normpath(os.path.join(base_dir, "exclude.txt"))

with open(buckets_json, "r") as fh:
    bucket_list = json.load(fh)
    for key in bucket_list:
        url = bucket_list[key]
        repo = url_to_repo_name(url)
        repo = repo.lower()
        builtins[repo] = key

with open(scoop_schema_json, "r") as fh:
    scoop_schema_data = json.load(fh)

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

df = pandas.read_csv(include_txt)
includes = df.to_dict("list")

df = pandas.read_csv(exclude_txt)
done = {}
excludes = df.to_dict("list")

for url in excludes["url"]:
    if url in includes["url"]:
        print("ERROR: url both included and excluded: %s" % url)
    repo = url_to_repo_name(url)
    repo = repo.lower()
    done[repo] = "excluded"

search_terms = [
    "topic:scoop-bucket",
    "scoop-bucket",
    "scoop bucket",
    "scoop",
]

for url in includes["url"]:
    repo = url_to_repo_name(url)
    repo = repo.lower()
    search_terms.append(repo)

searches = [
    {
        "score": True,
        "searches": search_terms,
    }
]

# @todo change to startup option
for arg in sys.argv[1:]:
    if re.match(r"^\d+$", arg):
        if int(arg) <= 99:
            MAX_SEARCHES = int(arg)

if MAX_SEARCHES < 99:
    max_pages = MAX_SEARCHES
    per_page = MAX_SEARCHES
    searches[0]["searches"] = ["topic:scoop-bucket"]

sys.exit(main())
