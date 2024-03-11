update_env:
	@echo "Updating the 'stock_markets' Conda environment from environment.yml..."
	conda env update --name stock_markets --file environment.yml
	@echo "Please activate the Conda environment with the following command: conda activate stock_markets"
