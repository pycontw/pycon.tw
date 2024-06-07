.PHONY: init

init:
	. ${NVM_DIR}/nvm.sh && nvm use
	yarn install --dev
	poetry env use 3.10
	poetry install
