# cc3d-scipyOptimize

Code to optimize parameters for our CompuCell3d model to fit Death Galaxy Data. 

## Installation

In ubuntu-20.04, The installation steps that are required are written in INSTALL_CC3D_ENV.sh. I am hoping that running this file would  install all the required packages. The following steps can be taken before running this script

* Clone the repository.
* Open INSTALL_CC3D_ENV.sh and change the value of variable `dir`  to the \path\of\the\directory where you want to download, build and install CC3D. Currently it installs in the  directory pointed out by `$HOME` variable in bash .
* Run  `bash -i INSTALL_CC3D_ENV.sh` in terminal to install CC3D and run the code.
* If, for any reason, we are required to run the code again then just use `bash -i run_code.sh`. 
