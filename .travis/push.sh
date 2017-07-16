#!/bin/sh

setup_git() {
  git checkout master
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

upload_files() {  
  git add . -A
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER [ci skip]"
  ls
  git remote add github-origin https://algomaniac:${GITHuB_TOKEN}@github.com/algomaniac/awesome-scoop.git
  git push --force --quiet github-origin master > /dev/null 2>&1
}

echo starting push
setup_git
upload_files