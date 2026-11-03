.PHONY: all setup test build run-stdio run-http docker-build clean

all: setup test build

setup:
	npm install

test: setup
	npm test

build: setup
	npm run build

run-stdio: setup
	npm run dev:stdio

run-http: setup
	npm run dev

docker-build:
	docker build -t mcp-starter-node:latest .

clean:
	rm -rf node_modules dist coverage
