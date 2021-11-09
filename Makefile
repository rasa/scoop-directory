all: help

add:
	git remote add -f spdx/license-list-data https://github.com/spdx/license-list-data
	git subtree add --prefix vendor/spdx/license-list-data spdx/license-list-data master --squash

pull:
	git fetch spdx/license-list-data master
	git subtree pull --prefix vendor/spdx/license-list-data spdx/license-list-data master --squash

help:
	@echo 'add:  Add subtrees'
	@echo 'pull: Pull subtree changes'
