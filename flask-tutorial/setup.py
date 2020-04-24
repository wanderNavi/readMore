from setuptools import find_packages, setup

setup(
	name='flaskr',
	version='1.0.0',
	packages=find_packages(), # what dictionaries to include
	include_package_data=True, # include static and templates
	zip_safe=False,
	install_requires=[
		'flask',
	],
)

####### EXPLAINATION FOR MANIFEST.in #######
'''
Required file directing python to where other files are

Graft lines copying everything in static and templates 
But also excluding all bytecoe files
'''

##############################
# NOTE: NOT ACTUALLY PACKAGING PROJECT INTO PIP