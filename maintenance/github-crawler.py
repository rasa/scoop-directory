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
# import shutil
# import stat
import sys
import time

# from builtins import dict
from datetime import datetime

import chardet
import jsoncomment
import requests

from git import Repo
from jinja2 import Environment, FileSystemLoader

OSI = [
    '0BSD', 'AAL', 'Abstyles', 'Adobe-2006', 'Adobe-Glyph', 'ADSL', 'AFL-1.1',
    'AFL-1.2', 'AFL-2.0', 'AFL-2.1', 'AFL-3.0', 'Afmparse', 'AGPL-1.0',
    'AGPL-1.0-only', 'AGPL-1.0-or-later', 'AGPL-3.0', 'AGPL-3.0-only',
    'AGPL-3.0-or-later', 'Aladdin', 'AMDPLPA', 'AML', 'AMPAS', 'ANTLR-PD',
    'Apache-1.0', 'Apache-1.1', 'Apache-2.0', 'APAFML', 'APL-1.0', 'APSL-1.0',
    'APSL-1.1', 'APSL-1.2', 'APSL-2.0', 'Artistic-1.0', 'Artistic-1.0-cl8',
    'Artistic-1.0-Perl', 'Artistic-2.0', 'Bahyph', 'Barr', 'Beerware',
    'BitTorrent-1.0', 'BitTorrent-1.1', 'Borceux', 'BSD-1-Clause',
    'BSD-2-Clause', 'BSD-2-Clause-FreeBSD', 'BSD-2-Clause-NetBSD',
    'BSD-2-Clause-Patent', 'BSD-3-Clause', 'BSD-3-Clause-Attribution',
    'BSD-3-Clause-Clear', 'BSD-3-Clause-LBNL',
    'BSD-3-Clause-No-Nuclear-License', 'BSD-3-Clause-No-Nuclear-License-2014',
    'BSD-3-Clause-No-Nuclear-Warranty', 'BSD-4-Clause', 'BSD-4-Clause-UC',
    'BSD-Protection', 'BSD-Source-Code', 'BSL-1.0', 'bzip2-1.0.5',
    'bzip2-1.0.6', 'Caldera', 'CATOSL-1.1', 'CC-BY-1.0', 'CC-BY-2.0',
    'CC-BY-2.5', 'CC-BY-3.0', 'CC-BY-4.0', 'CC-BY-NC-1.0', 'CC-BY-NC-2.0',
    'CC-BY-NC-2.5', 'CC-BY-NC-3.0', 'CC-BY-NC-4.0', 'CC-BY-NC-ND-1.0',
    'CC-BY-NC-ND-2.0', 'CC-BY-NC-ND-2.5', 'CC-BY-NC-ND-3.0', 'CC-BY-NC-ND-4.0',
    'CC-BY-NC-SA-1.0', 'CC-BY-NC-SA-2.0', 'CC-BY-NC-SA-2.5', 'CC-BY-NC-SA-3.0',
    'CC-BY-NC-SA-4.0', 'CC-BY-ND-1.0', 'CC-BY-ND-2.0', 'CC-BY-ND-2.5',
    'CC-BY-ND-3.0', 'CC-BY-ND-4.0', 'CC-BY-SA-1.0', 'CC-BY-SA-2.0',
    'CC-BY-SA-2.5', 'CC-BY-SA-3.0', 'CC-BY-SA-4.0', 'CC0-1.0', 'CDDL-1.0',
    'CDDL-1.1', 'CDLA-Permissive-1.0', 'CDLA-Sharing-1.0', 'CECILL-1.0',
    'CECILL-1.1', 'CECILL-2.0', 'CECILL-2.1', 'CECILL-B', 'CECILL-C',
    'ClArtistic', 'CNRI-Jython', 'CNRI-Python', 'CNRI-Python-GPL-Compatible',
    'Condor-1.1', 'CPAL-1.0', 'CPL-1.0', 'CPOL-1.02', 'Crossword',
    'CrystalStacker', 'CUA-OPL-1.0', 'Cube', 'curl', 'D-FSL-1.0', 'diffmark',
    'DOC', 'Dotseqn', 'DSDP', 'dvipdfm', 'ECL-1.0', 'ECL-2.0', 'eCos-2.0',
    'EFL-1.0', 'EFL-2.0', 'eGenix', 'Entessa', 'EPL-1.0', 'EPL-2.0',
    'ErlPL-1.1', 'EUDatagrid', 'EUPL-1.0', 'EUPL-1.1', 'EUPL-1.2', 'Eurosym',
    'Fair', 'Frameworx-1.0', 'FreeImage', 'FSFAP', 'FSFUL', 'FSFULLR', 'FTL',
    'GFDL-1.1', 'GFDL-1.1-only', 'GFDL-1.1-or-later', 'GFDL-1.2',
    'GFDL-1.2-only', 'GFDL-1.2-or-later', 'GFDL-1.3', 'GFDL-1.3-only',
    'GFDL-1.3-or-later', 'Giftware', 'GL2PS', 'Glide', 'Glulxe', 'gnuplot',
    'GPL-1.0', 'GPL-1.0+', 'GPL-1.0-only', 'GPL-1.0-or-later', 'GPL-2.0',
    'GPL-2.0+', 'GPL-2.0-only', 'GPL-2.0-or-later',
    'GPL-2.0-with-autoconf-exception', 'GPL-2.0-with-bison-exception',
    'GPL-2.0-with-classpath-exception', 'GPL-2.0-with-font-exception',
    'GPL-2.0-with-GCC-exception', 'GPL-3.0', 'GPL-3.0+', 'GPL-3.0-only',
    'GPL-3.0-or-later', 'GPL-3.0-with-autoconf-exception',
    'GPL-3.0-with-GCC-exception', 'gSOAP-1.3b', 'HaskellReport', 'HPND',
    'IBM-pibs', 'ICU', 'IJG', 'ImageMagick', 'iMatix', 'Imlib2', 'Info-ZIP',
    'Intel', 'Intel-ACPI', 'Interbase-1.0', 'IPA', 'IPL-1.0', 'ISC',
    'JasPer-2.0', 'JSON', 'LAL-1.2', 'LAL-1.3', 'Latex2e', 'Leptonica',
    'LGPL-2.0', 'LGPL-2.0+', 'LGPL-2.0-only', 'LGPL-2.0-or-later', 'LGPL-2.1',
    'LGPL-2.1+', 'LGPL-2.1-only', 'LGPL-2.1-or-later', 'LGPL-3.0', 'LGPL-3.0+',
    'LGPL-3.0-only', 'LGPL-3.0-or-later', 'LGPLLR', 'Libpng', 'libtiff',
    'LiLiQ-P-1.1', 'LiLiQ-R-1.1', 'LiLiQ-Rplus-1.1', 'Linux-OpenIB', 'LPL-1.0',
    'LPL-1.02', 'LPPL-1.0', 'LPPL-1.1', 'LPPL-1.2', 'LPPL-1.3a', 'LPPL-1.3c',
    'MakeIndex', 'MirOS', 'MIT', 'MIT-0', 'MIT-advertising', 'MIT-CMU',
    'MIT-enna', 'MIT-feh', 'MITNFA', 'Motosoto', 'mpich2', 'MPL-1.0', 'MPL-1.1',
    'MPL-2.0', 'MPL-2.0-no-copyleft-exception', 'MS-PL', 'MS-RL', 'MTLL',
    'Multics', 'Mup', 'NASA-1.3', 'Naumen', 'NBPL-1.0', 'NCSA', 'Net-SNMP',
    'NetCDF', 'Newsletr', 'NGPL', 'NLOD-1.0', 'NLPL', 'Nokia', 'NOSL', 'Noweb',
    'NPL-1.0', 'NPL-1.1', 'NPOSL-3.0', 'NRL', 'NTP', 'Nunit', 'OCCT-PL',
    'OCLC-2.0', 'ODbL-1.0', 'OFL-1.0', 'OFL-1.1', 'OGTSL', 'OLDAP-1.1',
    'OLDAP-1.2', 'OLDAP-1.3', 'OLDAP-1.4', 'OLDAP-2.0', 'OLDAP-2.0.1',
    'OLDAP-2.1', 'OLDAP-2.2', 'OLDAP-2.2.1', 'OLDAP-2.2.2', 'OLDAP-2.3',
    'OLDAP-2.4', 'OLDAP-2.5', 'OLDAP-2.6', 'OLDAP-2.7', 'OLDAP-2.8', 'OML',
    'OpenSSL', 'OPL-1.0', 'OSET-PL-2.1', 'OSL-1.0', 'OSL-1.1', 'OSL-2.0',
    'OSL-2.1', 'OSL-3.0', 'PDDL-1.0', 'PHP-3.0', 'PHP-3.01', 'Plexus',
    'PostgreSQL', 'psfrag', 'psutils', 'Python-2.0', 'Qhull', 'QPL-1.0',
    'Rdisc', 'RHeCos-1.1', 'RPL-1.1', 'RPL-1.5', 'RPSL-1.0', 'RSA-MD', 'RSCPL',
    'Ruby', 'SAX-PD', 'Saxpath', 'SCEA', 'Sendmail', 'SGI-B-1.0', 'SGI-B-1.1',
    'SGI-B-2.0', 'SimPL-2.0', 'SISSL', 'SISSL-1.2', 'Sleepycat', 'SMLNJ',
    'SMPPL', 'SNIA', 'Spencer-86', 'Spencer-94', 'Spencer-99', 'SPL-1.0',
    'StandardML-NJ', 'SugarCRM-1.1.3', 'SWL', 'TCL', 'TCP-wrappers', 'TMate',
    'TORQUE-1.1', 'TOSL', 'Unicode-DFS-2015', 'Unicode-DFS-2016', 'Unicode-TOU',
    'Unlicense', 'UPL-1.0', 'Vim', 'VOSTROM', 'VSL-1.0', 'W3C', 'W3C-19980720',
    'W3C-20150513', 'Watcom-1.0', 'Wsuipa', 'WTFPL', 'wxWindows', 'X11',
    'Xerox', 'XFree86-1.1', 'xinetd', 'Xnet', 'xpp', 'XSkat', 'YPL-1.0',
    'YPL-1.1', 'Zed', 'Zend-2.0', 'Zimbra-1.3', 'Zimbra-1.4', 'Zlib',
    'zlib-acknowledgement', 'ZPL-1.1', 'ZPL-2.0', 'ZPL-2.1', '389-exception',
    'Autoconf-exception-2.0', 'Autoconf-exception-3.0', 'Bison-exception-2.2',
    'Bootloader-exception', 'Classpath-exception-2.0', 'CLISP-exception-2.0',
    'DigiRule-FOSS-exception', 'eCos-exception-2.0', 'Fawkes-Runtime-exception',
    'FLTK-exception', 'Font-exception-2.0', 'freertos-exception-2.0',
    'GCC-exception-2.0', 'GCC-exception-3.1', 'gnu-javamail-exception',
    'i2p-gpl-java-exception', 'Libtool-exception', 'Linux-syscall-note',
    'LLVM-exception', 'LZMA-exception', 'mif-exception',
    'Nokia-Qt-exception-1.1', 'OCCT-exception-1.0',
    'OpenJDK-assembly-exception-1.0', 'openvpn-openssl-exception',
    'Qt-GPL-exception-1.0', 'Qt-LGPL-exception-1.1', 'Qwt-exception-1.0',
    'u-boot-exception-2.0', 'sWxWindows-exception-3.1']

lmap = {
    'commercial':
        'https://en.m.wikipedia.org/wiki/Software_license#Proprietary_software_licenses',
    'freeware':
        'https://en.wikipedia.org/wiki/Freeware',
    'proprietary':
        'https://en.m.wikipedia.org/wiki/Software_license#Proprietary_software_licenses',
    'public_domain':
        'https://wiki.creativecommons.org/wiki/Public_domain',
    'public domain':
        'https://wiki.creativecommons.org/wiki/Public_domain',
    'public-domain':
        'https://wiki.creativecommons.org/wiki/Public_domain',
    'publicdomain':
        'https://wiki.creativecommons.org/wiki/Public_domain',
    'shareware':
        'https://en.wikipedia.org/wiki/Shareware', }

done = [
    'nueko/scoop-php-ext',
    'pavanbijja/scoop-bucket',
    'rivy/scoop.bucket.scoop-main', ]

max_pages = 10

searches = []

searches.append({
    'pages': max_pages,
    'score': True,
    'searches': [
        'scoop-bucket',
        'scoop+bucket', ]})

searches.append({
    'pages':
        1,
    'score':
        True,
    'searches': [
        'scoop',
        'comp500/scoop-browser',
        'ghchinoy/scoop-ce',
        'jfut/scoop-jfut',
        'jfut/scoop-pleiades',
        'ghchinoy/scoop-roguewave',
        'mko-x/bucket',
        '82p/scoop-yubico-bucket',
        'Aaike/scoop',
        'Alxandr/scoop-bucket',
        'BjoernPetersen/scoop-bucket',
        'Callidin/ragnar-scoop',
        'Congee/barrel',
        'DimiG/dgBucket',
        'Doublemine/scoops',
        'ErnWong/scoop-bucket',
        'Guard13007/ScoopBucket',
        'Jokler/scoop-bucket',
        'Lomeli12/ScoopBucket',
        'Sandex/scoop-supernova',
        'Southclaws/scoops',
        'TnmkFan/my-bucket',
        'TorrentKatten/torrentkatten-scoop-bucket',
        'Utdanningsdirektoratet/PAS-scoop-public',
        'Vngdv/another-useless-scoop-bucket',
        'anurse/scoop-bucket',
        'bitrvmpd/scoop-wuff',
        'broovy/scoop-bucket',
        'comp500/scoop-comp500',
        'cprecioso/scoop-lektor',
        'deevus/scoop-games',
        'demas/demas-scoop',
        'dennislloydjr/scoop-bucket-devbox',
        'divanvisagie/scoop-bucket',
        'excitoon/scoop-user',
        'ezhikov/scoop-bucket',
        'follnoob/follnoob-bucket',
        'fredjoseph/scoop-bucket',
        'furyfire/my-bucket',
        'galbro/my-bucket',
        'gexclaude/scoop-bucket',
        'goreleaser/scoop-bucket',
        'h404bi/dorado',
        'hermanjustnu/scoop-emulators',
        'iainsgillis/isg-bucket',
        'idursun/my-bucket',
        'jamesgecko/scoop-packages',
        'javageek/scoop-bucket',
        'jmcarbo/scoopbucket',
        'kentork/scoop-leaky-bucket',
        'klaidliadon/scoop-buckets',
        'klauern/trackello-bucket',
        'kodybrown/scoop-nirsoft',
        'liaoya/scoop-bucket',
        'lillicoder/scoop-openjdk6',
        'lukesampson/scoop',
        'lukesampson/scoop-extras',
        'lzimd/lzimd-scoop-bucket',
        'maman/scoop-bucket',
        'masaeedu/scoop-growlnotify',
        'masonm12/scoop-personal',
        'matthewjberger/scoop-nerd-fonts',
        'mattkang/scoop-bucket',
        'michaelxmcbride/scoop-michaelxmcbride',
        'mmichaelis/scoop-bucket',
        'monotykamary/toms-scoop-bucket',
        'narnaud/scoop-bucket',
        'nikolasd/scoop-bucket',
        'noquierouser/nqu-scoop',
        'nrakochy/scoop-solidity',
        'nsstrunks/scoop-bucket',
        'nueko/scoop-php',
        'nueko/scoop-php-ext',
        'oltolm/scoop-nonportable',
        'ondr3j/scoop-misc',
        'pastleo/scoop-bucket',
        'pcrama/scoop-buckets',
        'rasa/scoops',
        'rcqls/scoop-extras',
        'rivy/scoop.bucket-scoop.main',
        'scoopinstaller/nightlies',
        'scoopinstaller/versions',
        'se35710/scoop-ibm',
        'se35710/scoop-java',
        'siddarthasagar/scoopbucket',
        'simonwjackson/my-bucket',
        'stlhrt/steel-buckets',
        'svkoh/scoop-bucket',
        'systemexitzero/scoop-bucket',
        'tapanchandra/scoop-personal',
        'tditlu/scoop-amiga',
        'themrhead/scoop-bucket-apps',
        'toburger/scoop-buckets',
        'twxs/scoop-buckets',
        'vidarkongsli/vidars-scoop-bucket',
        'wangzq/scoop-bucket',
        'webwesen/webwesen-scoop-bucket',
        'wrokred/phpdev-scoop-bucket',
        'yt3r/test-bucket',
        'yuanying1199/scoopbucket',
        'yutahaga/scoop-bucket', ]})

bucket_list = {
    "extras": "https://github.com/lukesampson/scoop-extras.git",
    "versions": "https://github.com/scoopinstaller/versions",
    "nightlies": "https://github.com/scoopinstaller/nightlies",
    "nirsoft": "https://github.com/kodybrown/scoop-nirsoft",
    "php": "https://github.com/nueko/scoop-php.git",
    "nerd-fonts": "https://github.com/matthewjberger/scoop-nerd-fonts.git",
    "nonportable": "https://github.com/oltolm/scoop-nonportable",
    "java": "https://github.com/se35710/scoop-java"}


def fix_license(s):
    """ @todo """
    s = re.sub(r'-only', '', s, re.I)
    s = re.sub(r'-or-later', '+', s, re.I)
    s = re.sub(r'-Clause', '', s, re.I)
    return s


def do_license(v):
    """ @todo """
    url = v
    if 'identifier' in v:
        identifier = fix_license(v['identifier'])
    else:
        identifier = ''
    if 'url' in v:
        url = v['url']
    if re.search(r'^(http|ftp)', url):
        if not identifier:
            identifier = 'Link'
        v = '[%s](%s)' % (identifier, url)
        return v

    if not identifier:
        identifier = url

    parts = re.split(r'[,|]+', identifier)
    v = ''
    for part in parts:
        if v > '':
            v += '/'
        url = ''
        part = part.strip()
        k = part.lower()
        if k in OSImap:
            url = OSImap[k]
        elif k in lmap:
            url = lmap[k]
        if url > '':
            v += '[%s](%s)' % (fix_license(part), url)
        else:
            v += part
        break

    if len(parts) > 1:
        v += '&hellip;'

    return v


def get_url(js):
    """ @todo """
    if 'homepage' in js:
        return js['homepage']
    if 'checkver' in js:
        if 'url' in js['checkver']:
            return js['checkver']['url']
        if 'github' in js['checkver']:
            return js['checkver']['github']
    return ''


def get_link(js):
    """ @todo """
    if 'url' in js:
        return js['url']
    if 'architecture' not in js:
        return None
    for bits in ['64bit', '32bit']:
        if bits not in js['architecture']:
            continue
        if 'url' not in js['architecture'][bits]:
            continue
        return js['architecture'][bits]['url']
    return None


def do_version(js):
    """ @todo """
    version = js['version']
    url = get_url(js)
    if 'checkver' not in js:
        version = '*%s*' % version.strip()
    if url == '':
        return version
    return '[%s](%s)' % (version, url)


def fetchjson(urlstr):
    """ @todo """
    response = requests.get(url=urlstr)
    if 'X-RateLimit-Remaining' not in response.headers:
        pprint.pprint(dict(response.headers), width=1)
    elif int(response.headers['X-RateLimit-Remaining']) < 1:
        reset = float(response.headers['X-RateLimit-Reset'])
        secs = reset - time.time()
        if secs > 0:
            print('Sleeping %d seconds due to rate limiting' % secs)
            time.sleep(secs)
    if response.status_code > 299:
        pprint.pprint(dict(response.headers), width=1)
        return {}
    return response.json()


def get_builtins():
    """ @todo """
    for key in bucket_list:
        url = bucket_list[key]
        m = re.search(r'github\.com/(.*)$', url, re.I)
        if m:
            name = m.group(1)
            m = re.search(r'^(.*)\.git$', name, re.I)
            if m:
                name = m.group(1)
            builtins[name] = key
    return 0


def initialize_cache():
    """ @todo """
    global cache
    global last_run

    # https://stackoverflow.com/a/4829285/1432614
    """
    def on_rm_error(func, path, exc_info):
        # logging.error('path=%s', path)
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        try:
            os.chmod(path, stat.S_IWRITE)
        except Exception as e:
            print(e)
        try:
            return os.unlink(path)
        except Exception as e:
            print(e)
            return 1
    """

    if os.path.isdir(cache_dir):
        print('deleting %s' % cache_dir)
        # shutil.rmtree(cache_dir, onerror=on_rm_error)

        os.system('cmd /c rmdir /s /q "%s"' % cache_dir)

    os.makedirs(cache_dir)

    try:
        with open(os.path.join(cache_dir, 'cache.pickle'), "rb") as input_file:
            cache = pickle.load(input_file)
    except (EnvironmentError, EOFError):
        cache['last_run'] = datetime(2000, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ')

    last_run = datetime.strptime(cache['last_run'], '%Y-%m-%dT%H:%M:%SZ')
    return 0


def do_repo(repo, i, num_repos, do_score=True):
    """ @todo """
    global last_run

    if 'name' not in repo:
        pprint.pprint(dict(repo), width=1)
        return 0

    full_name = repo['full_name']

    print('  %3d/%3d: %-50s: ' % (i, num_repos, full_name), end='')
    nl = True

    if full_name.lower() in done:
        print('Skipping (done)')
        return 0

    done.append(full_name.lower())

    if repo['fork']:
        print('Skipping (fork)')
        return 0

    # pprint.pprint(dict(repo), width=1)
    # sys.exit()

    repofoldername = full_name.replace('/', '+')
    git_clone_url = repo['git_url']
    html_url = repo['html_url']
    score = float(repo['score'])
    if not do_score:
        score = 0
    last_updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')

    id_ = full_name.replace('/', '_')
    id_ = re.sub(r'[^0-9a-zA-Z_:.-]+', '-', id_)
    if not re.match(r'^[a-zA-Z]', id_[0]):
        id_ = 'a' + id_

    if repofoldername not in cache:
        try:
            Repo.clone_from(
                git_clone_url, os.path.join(cache_dir, repofoldername))
        except Exception as e:
            if nl:
                print('')
                nl = False
            print(e)
            return 0

        try:
            description = repo['description'].strip()
        except Exception:
            description = ''

        builtin_text = ''
        if full_name in builtins:
            builtin_text = "scoop's built-in bucket '%s'" % builtins[full_name]
        if full_name in 'lukesampson/scoop':
            builtin_text = "scoop's main/default bucket"
        if builtin_text:
            description += " (%s)" % builtin_text

        if description:
            idescription = '*%s*' % description
            cdescription = ': ' + idescription
        else:
            idescription = ''
            cdescription = ''

        pattern = '%Y-%m-%dT%H:%M:%S'
        try:
            epoch = int(
                time.mktime(time.strptime(repo['updated_at'][:-1], pattern)))
        except:
            epoch = 0

        cache[repofoldername] = {
            'cdescription': cdescription,
            'description': description,
            'entries': [],
            'epoch': epoch,
            'forks': int(repo['forks']),
            'forks_url': html_url + '/network',
            'full_name': full_name,
            'id': id_,
            'idescription': idescription,
            'packages': 0,
            'score': score,
            'score5': round(score, 2),
            'size': int(repo['size']),
            'stars': int(repo['stargazers_count']),
            'stars_url': html_url + '/stargazers',
            'updated': repo['updated_at'][2:10].replace('-', '&#x2011;'),
            'updated_url': html_url + '/commits',
            'url': html_url, }

    elif repofoldername in cache and (last_updated > last_run):
        repo = Repo(os.path.join(cache_dir, repofoldername))
        o = repo.remotes.origin
        try:
            o.pull()
        except Exception as e:
            if nl:
                print('')
                nl = False
            print(e)

    if not os.path.isdir(os.path.join(cache_dir, repofoldername)):
        return 0

    cache[repofoldername]['entries'] = []

    if full_name == 'lukesampson/scoop':
        bucket = '/bucket'
    else:
        bucket = ''

    bucket_path = os.path.join(cache_dir, repofoldername) + bucket

    jsons = 0
    good_jsons = 0
    for f in os.listdir(bucket_path):
        file_path = os.path.join(bucket_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.path.splitext(file_path)[1] != '.json':
            continue

        jsons += 1
        row = {}
        for key in keys:
            row[key] = ''
        row['json'] = os.path.splitext(f)[0]
        try:
            parser = jsoncomment.JsonComment(json)
            with io.open(file_path, 'rb') as fp:
                s = fp.read()
                h = chardet.detect(s)
            with io.open(file_path, 'r', encoding=h['encoding']) as fp:
                s = fp.read()
                # Strip out single line comments
                s = re.sub(r'^\s*//.*$', '', s)
                j = parser.loads(s)

            if not get_link(j):
                if nl:
                    print('')
                    nl = False
                print('    %s: no url' % f)
                continue
            if 'version' not in j:
                if nl:
                    print('')
                    nl = False
                print('    %s: no version' % f)
                continue

            row['url'] = get_url(j)
            if not row['url']:
                row['url'] = html_url + '/blob/master' + bucket + '/' + f
            for key in keys:
                if key in j:
                    v = j[key]
                    is_string = type(v).__name__ == 'unicode' or type(
                        v).__name__ == 'str'
                    if is_string:
                        v = v.strip()
                        v = re.sub(r'[\r\n]+', ' ', v)
                    if key == 'license':
                        v = do_license(v)
                    if key == 'version':
                        v = do_version(j)

                    row[key] = v
                # @TODO add bits/exes,shortcuts
                # https://png.icons8.com/android/48/000000/ok.png
                # https://png.icons8.com/android/48/000000/32bit.png
                # https://png.icons8.com/android/48/000000/64bit.png
                # exes
                # shortcuts
            good_jsons += 1

        except Exception as e:
            if nl:
                print('')
                nl = False
            print('    %s: %s (%s)' % (f, e, h['encoding']))
            row['description'] = str(e)

        cache[repofoldername]['entries'].append(row)

    if good_jsons == 0:
        cache[repofoldername]['entries'] = []

    cache[repofoldername]['packages'] = len(cache[repofoldername]['entries'])
    if not nl:
        print('%-61s: ' % '', end='')

    print(
        '%3d (score:%10.6f)' %
        (len(cache[repofoldername]['entries']), repo['score']))
    return len(cache[repofoldername]['entries'])


def do_page(search, page, do_score=True):
    """ @todo """
    api = 'https://api.github.com/search/repositories?q=%s&per_page=%d'

    url = api % (search, per_page)
    if page > 1:
        url += '&page=%d' % page
    rv = fetchjson(url)
    if 'items' not in rv:
        print('items not found in search results')
        return 0
    repos = rv['items']
    i = 0
    hits = 0
    for repo in repos:
        i += 1
        hits += do_repo(repo, i, len(repos), do_score)

    return hits


def do_search(search, pages=1, do_score=True):
    """ @todo """
    for page in range(1, pages + 1):
        print('q: %s (page %s of %s)' % (search, page, pages))
        hits = do_page(search, page, do_score)
        if hits == 0:
            break
    return 0


def do_searches():
    """ @todo """
    for h in searches:
        for search in h['searches']:
            if search.lower() in done:
                continue
            do_search(search, h['pages'], h['score'])

    return 0


def save_cache():
    """ @todo """
    global cache

    print("Saving cache")
    cache['last_run'] = datetime.strftime(
        datetime.now().replace(hour=0, minute=0, second=0),
        '%Y-%m-%dT%H:%M:%SZ')

    try:
        with open(os.path.join(cache_dir, 'cache.pickle'), "wb") as input_file:
            pickle.dump(cache, input_file)
    except EnvironmentError:
        pass

    return 0


def sort_repos(first_sort_key):
    """ @todo """
    global repos_by_score
    global repos_by_name

    print("Sorting output")
    repos = [repo for repo in cache.keys()]
    repos_by_score = [
        repo for repo in repos
        if repo != 'last_run' and len(cache[repo]['entries']) > 0]
    repos_by_score = sorted(
        repos_by_score,
        key=lambda repo: (
            -cache[repo][first_sort_key], -cache[repo]['score'], -cache[repo]['stars'],
            -cache[repo]['forks'], -cache[repo]['packages'], 
            cache[repo]['full_name'].lower()))
    
    repos_by_name = copy.deepcopy(repos_by_score)
    repos_by_name = sorted(
        repos_by_name, key=lambda repo: cache[repo]['full_name'].lower())
    return True


def do_render(filename, sort_order_description):
    """ @todo """
    print("Generating %s" % filename)
    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(dir_path, 'template')),
        trim_blocks=False)
    context = {
        'repos_by_score': repos_by_score,
        'repos_by_name': repos_by_name,
        'cache': cache,
        'sort_order_description': sort_order_description}
    tpl = 'ReadmeTemplate.tpl'
    markdown_content = TEMPLATE_ENVIRONMENT.get_template(tpl).render(context)
    with io.open(filename, 'w', encoding='utf-8', newline="\n") as f:
        written = f.write(markdown_content)
        print("Wrote %d bytes to %s" % (written, filename))
    return True


def do_readme(sort_field, output_file, sort_order_description):
    """ @todo """
    filename = os.path.realpath(os.path.join(dir_path, '..', output_file))
    if not os.path.isfile(filename):
        print("File not found: %s" % filename)
        return False    
    sort_repos(sort_field)
    do_render(filename, sort_order_description)
    return True


def main():
    """ @todo """
    get_builtins()
    initialize_cache()
    do_searches()
    save_cache()
    do_readme('score', 'README.md', 'Github score')
    do_readme('epoch', 'by-date-updated.md', 'update date')
    return 0


OSImap = {}
for k_ in OSI:
    OSImap[k_.lower()] = 'https://opensource.org/licenses/%s' % k_

keys = [
    'checkver',
    'description',
    'homepage',
    'license',
    'version', ]

dir_path = os.path.dirname(os.path.realpath(__file__))
cache_dir = os.path.join(dir_path, 'cache')

if 'COMPUTERNAME' in os.environ:
    if os.environ['COMPUTERNAME'] == 'KITSUNE':
        cache_dir = 'd:/c'

last_run = None

cache = {}
builtins = {}
repos_by_score = []
repos_by_name = []

per_page = 100

if False:
    per_page = 1
    max_pages = 1
    searches[0]['pages'] = max_pages
    searches[1]['pages'] = max_pages
    searches[1]['searches'] = ['scoop']

sys.exit(main())
"""
{u'archive_url': u'https://api.github.com/repos/lukesampson/scoop-extras/{archive_format}{/ref}',
 u'archived': False,
 u'assignees_url': u'https://api.github.com/repos/lukesampson/scoop-extras/assignees{/user}',
 u'blobs_url': u'https://api.github.com/repos/lukesampson/scoop-extras/git/blobs{/sha}',
 u'branches_url': u'https://api.github.com/repos/lukesampson/scoop-extras/branches{/branch}',
 u'clone_url': u'https://github.com/lukesampson/scoop-extras.git',
 u'collaborators_url': u'https://api.github.com/repos/lukesampson/scoop-extras/collaborators{/collaborator}',
 u'comments_url': u'https://api.github.com/repos/lukesampson/scoop-extras/comments{/number}',
 u'commits_url': u'https://api.github.com/repos/lukesampson/scoop-extras/commits{/sha}',
 u'compare_url': u'https://api.github.com/repos/lukesampson/scoop-extras/compare/{base}...{head}',
 u'contents_url': u'https://api.github.com/repos/lukesampson/scoop-extras/contents/{+path}',
 u'contributors_url': u'https://api.github.com/repos/lukesampson/scoop-extras/contributors',
 u'created_at': u'2013-08-06T03:27:50Z',
 u'default_branch': u'master',
 u'deployments_url': u'https://api.github.com/repos/lukesampson/scoop-extras/deployments',
 u'description': u'"Extras" bucket for Scoop',
 u'downloads_url': u'https://api.github.com/repos/lukesampson/scoop-extras/downloads',
 u'events_url': u'https://api.github.com/repos/lukesampson/scoop-extras/events',
 u'fork': False,
 u'forks': 214,
 u'forks_count': 214,
 u'forks_url': u'https://api.github.com/repos/lukesampson/scoop-extras/forks',
 u'full_name': u'lukesampson/scoop-extras',
 u'git_commits_url': u'https://api.github.com/repos/lukesampson/scoop-extras/git/commits{/sha}',
 u'git_refs_url': u'https://api.github.com/repos/lukesampson/scoop-extras/git/refs{/sha}',
 u'git_tags_url': u'https://api.github.com/repos/lukesampson/scoop-extras/git/tags{/sha}',
 u'git_url': u'git://github.com/lukesampson/scoop-extras.git',
 u'has_downloads': True,
 u'has_issues': True,
 u'has_pages': False,
 u'has_projects': True,
 u'has_wiki': True,
 u'homepage': None,
 u'hooks_url': u'https://api.github.com/repos/lukesampson/scoop-extras/hooks',
 u'html_url': u'https://github.com/lukesampson/scoop-extras',
 u'id': 11914939,
 u'issue_comment_url': u'https://api.github.com/repos/lukesampson/scoop-extras/issues/comments{/number}',
 u'issue_events_url': u'https://api.github.com/repos/lukesampson/scoop-extras/issues/events{/number}',
 u'issues_url': u'https://api.github.com/repos/lukesampson/scoop-extras/issues{/number}',
 u'keys_url': u'https://api.github.com/repos/lukesampson/scoop-extras/keys{/key_id}',
 u'labels_url': u'https://api.github.com/repos/lukesampson/scoop-extras/labels{/name}',
 u'language': u'PowerShell',
 u'languages_url': u'https://api.github.com/repos/lukesampson/scoop-extras/languages',
 u'license': None,
 u'merges_url': u'https://api.github.com/repos/lukesampson/scoop-extras/merges',
 u'milestones_url': u'https://api.github.com/repos/lukesampson/scoop-extras/milestones{/number}',
 u'mirror_url': None,
 u'name': u'scoop-extras',
 u'node_id': u'MDEwOlJlcG9zaXRvcnkxMTkxNDkzOQ==',
 u'notifications_url': u'https://api.github.com/repos/lukesampson/scoop-extras/notifications{?since,all,participating}',
 u'open_issues': 23,
 u'open_issues_count': 23,
 u'owner': {u'avatar_url': u'https://avatars3.githubusercontent.com/u/103446?v=4',
            u'events_url': u'https://api.github.com/users/lukesampson/events{/privacy}',
            u'followers_url': u'https://api.github.com/users/lukesampson/followers',
            u'following_url': u'https://api.github.com/users/lukesampson/following{/other_user}',
            u'gists_url': u'https://api.github.com/users/lukesampson/gists{/gist_id}',
            u'gravatar_id': u'',
            u'html_url': u'https://github.com/lukesampson',
            u'id': 103446,
            u'login': u'lukesampson',
            u'node_id': u'MDQ6VXNlcjEwMzQ0Ng==',
            u'organizations_url': u'https://api.github.com/users/lukesampson/orgs',
            u'received_events_url': u'https://api.github.com/users/lukesampson/received_events',
            u'repos_url': u'https://api.github.com/users/lukesampson/repos',
            u'site_admin': False,
            u'starred_url': u'https://api.github.com/users/lukesampson/starred{/owner}{/repo}',
            u'subscriptions_url': u'https://api.github.com/users/lukesampson/subscriptions',
            u'type': u'User',
            u'url': u'https://api.github.com/users/lukesampson'},
 u'private': False,
 u'pulls_url': u'https://api.github.com/repos/lukesampson/scoop-extras/pulls{/number}',
 u'pushed_at': u'2018-07-13T23:01:50Z',
 u'releases_url': u'https://api.github.com/repos/lukesampson/scoop-extras/releases{/id}',
 u'score': 221.29436,
 u'size': 2615,
 u'ssh_url': u'git@github.com:lukesampson/scoop-extras.git',
 u'stargazers_count': 248,
 u'stargazers_url': u'https://api.github.com/repos/lukesampson/scoop-extras/stargazers',
 u'statuses_url': u'https://api.github.com/repos/lukesampson/scoop-extras/statuses/{sha}',
 u'subscribers_url': u'https://api.github.com/repos/lukesampson/scoop-extras/subscribers',
 u'subscription_url': u'https://api.github.com/repos/lukesampson/scoop-extras/subscription',
 u'svn_url': u'https://github.com/lukesampson/scoop-extras',
 u'tags_url': u'https://api.github.com/repos/lukesampson/scoop-extras/tags',
 u'teams_url': u'https://api.github.com/repos/lukesampson/scoop-extras/teams',
 u'trees_url': u'https://api.github.com/repos/lukesampson/scoop-extras/git/trees{/sha}',
 u'updated_at': u'2018-07-14T00:33:08Z',
 u'url': u'https://api.github.com/repos/lukesampson/scoop-extras',
 u'watchers': 248,
 u'watchers_count': 248}

"""
