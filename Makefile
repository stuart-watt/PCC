###########################
## Environment variables ##
###########################

export ALIAS = PCC 

#############
## Install ##
#############

mamba:
	mamba env update -n $(ALIAS) --file environment.yml --prune \
		|| \
	mamba env create --file environment.yml

#############
## Testing ##
#############


################
## Formatting ##
################

format:
	black .

