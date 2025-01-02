IMAGE=scraper

build:
	docker build -t $(IMAGE) .

run: build
	docker run -p 5000:5000 --name $(IMAGE) -it --rm $(IMAGE)

clean:
	-docker stop $(IMAGE)
	-docker rm $(IMAGE)

.PHONY: build run clean
default: build run
