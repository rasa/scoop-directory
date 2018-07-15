#!/bin/sh

setup_git() {
  git checkout master
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

upload_files() {  
  git add -u .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER [ci skip]"
  ls
  git remote add github-origin https://rasa:${GITHUB_TOKEN}@github.com/rasa/scoop-directory.git
  git push github-origin master 
}

echo starting push
setup_git
upload_files

