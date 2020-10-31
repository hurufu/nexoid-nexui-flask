FLASK_APP := nexui
FLASK_ENV := development
FLASK     := flask

export FLASK_APP
export FLASK_ENV

FLASK_ARGS_run := --host 0.0.0.0 --port 5000

.PHONY: default
default: flask-run

.PHONY: flask-%
flask-%:
	$(FLASK) $* $(FLASK_ARGS_$*)
