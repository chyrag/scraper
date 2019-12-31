LABEL = jooble

.PHONY: all build run

all: run

build:
	docker build -t $(LABEL) .

run: build
	docker run --rm --network=host --volume /tmp:/tmp $(LABEL) --location="New York" --keywords="Python"
