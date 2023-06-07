FLASK_APP := nexui
FLASK     := flask

export FLASK_APP

FLASK_ARGS_run := --host 0.0.0.0 --port 5000

.PHONY: default
default: flask-run

.PHONY: flask-%
flask-%:
	$(FLASK) $* --no-reload --debug $(FLASK_ARGS_$*)
