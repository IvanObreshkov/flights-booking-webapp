.PHONY: install-hooks
install-hooks:
	chmod +x ./.githooks/install_hooks.sh
	sudo ./.githooks/install_hooks.sh
