Move the initialize.sh, startup.sh, shutdown.sh, and reset.sh files to the mysql file in your project directory. Then, run the following commands:

# Initialize (Do it once)
sh -x initialize.sh

# Start server
sh -x startup.sh

# Stop server
#sh -x shutdown.sh

# Destroy (!!!) all your databases, cleanup directory
#sh -x reset.sh

Once this is done, run the setup.py from the database directory. 
If at any point the setup.py fails, use schema.py's main to reset/cleanup the database and import the things you want to.
