# Technical assignment for Cial dun&amp;bradStreet

# How to launch application
Check if *docker* is installed in your pc, otherwise follow the official tutorial:

For **windows**: https://docs.docker.com/desktop/install/windows-install/

For **linux**: https://docs.docker.com/desktop/install/linux-install/

- Now, assuming docker is installed, run:

`docker build -t my_image --rm .`

*Just wait for the installation of the dependencies and env setup*

- Finally, run:

`docker run -it --name my_app --rm my_image`


# How it works