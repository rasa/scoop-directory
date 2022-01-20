# Makefile

SCOOP_SCHEMA_JSON=https://raw.githubusercontent.com/ScoopInstaller/Scoop/master/schema.json
BUCKETS_JSON=https://raw.githubusercontent.com/ScoopInstaller/Scoop/master/buckets.json
LICENSES_JSON=https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json
EXCEPTIONS_JSON=https://raw.githubusercontent.com/spdx/license-list-data/master/json/exceptions.json

all: help

add:
	# git remote add -f spdx/license-list-data https://github.com/spdx/license-list-data
	# git subtree add --prefix vendor/spdx/license-list-data spdx/license-list-data master --squash

pull:
	# git fetch spdx/license-list-data master
	# git subtree pull --prefix vendor/spdx/license-list-data spdx/license-list-data master --squash

update:
	-mkdir -p vendor/ScoopInstaller/Scoop
	wget -O vendor/ScoopInstaller/Scoop/schema.json $(SCOOP_SCHEMA_JSON)
	wget -O vendor/ScoopInstaller/Scoop/buckets.json $(BUCKETS_JSON)
	-mkdir -p vendor/spdx/license-list-data/master/json
	wget -O vendor/spdx/license-list-data/master/json/licenses.json $(LICENSES_JSON)
	wget -O vendor/spdx/license-list-data/master/json/exceptions.json $(EXCEPTIONS_JSON)

help:
	@echo 'add:    Add vendor subtrees'
	@echo 'pull:   Pull vendor subtree changes'
	@echo 'update: Download vendor updates'
