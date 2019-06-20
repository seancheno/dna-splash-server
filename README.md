# Dna Splash 

A RESTful API built with Python, Flask, and Docker to help visualize the genome by adding a splash of color to each base pair (A C G T). 

* This is the server-side repo built with Docker and Flask. 

* Uses Amazon RDS and S3 for database and image storage.

* The front end repo built with React can be found [here](https://github.com/seancheno/dna-splash-client).

* Visit the live demo at [dnasplash.com](https://dnasplash.com).


## How it works 

DNA Splash allows a user to asign a color value to each of the four base pairs for a segment of dna. The coloring algorthm runs through the sequence of base pairs starting with the first four and calculates a color based on the frequency of each base pair. The mixed color is converted into a pixel and this process then shifts over 1 base pair and repeats until the end of the dna sequence is reached. The result is an image representing a visual representation of the dna sequence.

![alt text](http://dnasplash.com/images/diagram1.jpg)


## Installation

Clone the Git repo

    git clone https://github.com/seancheno/dna-splash-server/
    cd dna-splash-server
    
Add S3 keys and RDS info to `config.py` and build with docker-compose.

    docker-compose up --build
       

## Notes

The genome sequence for each species is provided by the University of California Santa Cruz and can be found [here](http://hgdownload.cse.ucsc.edu/downloads.html).