.PHONY: all setup test clean

all: setup test

setup:
	@echo "Setting up Python starter..."
	@$(MAKE) -C python setup
	@echo "Setting up Node starter..."
	@$(MAKE) -C node setup

test:
	@echo "Testing Python starter..."
	@$(MAKE) -C python test
	@echo "Testing Node starter..."
	@$(MAKE) -C node test

clean:
	@$(MAKE) -C python clean
	@$(MAKE) -C node clean
