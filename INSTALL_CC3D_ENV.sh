#!/usr/bin/sh

pyvrsn=3.8 # Conda python version.
env=cc3d_2020 # conda environment for CC3D installation.
vrsn=4.2.5  # CC3D version. Don't change it!
vrsnwodt=${vrsn//./}

dir= $HOME # Installation directory for CC3D
srcdir= ${dir}/CC3D_GIT # Source Directory for CC3D.
bdir= ${dir}/cc3d_${vrsnwodt}_build # Build Directory for CC3D.

cd ${dir}
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source $HOME/.bashrc
conda activate
conda create -n $env python=$pyvrsn
conda activate $env
conda install -c conda-forge numpy scipy pandas jinja2 webcolors vtk=8.2 pyqt pyqtgraph deprecated qscintilla2 jinja2 chardet cmake swig=3 requests
conda install -c conda-forge  scipy=1.7.0
conda install -c compucell3d tbb_full_dev
pip install libroadrunner
pip install antimony

conda activate base

sudo apt-get install -y g++ build-essential git libglu1-mesa libxi-dev libxmu-dev libglu1-mesa-dev
ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
mkdir $srcdir
cd $srcdir
git clone https://github.com/CompuCell3D/CompuCell3D.git .
git clone https://github.com/CompuCell3D/cc3d_build_scripts.git
cd cc3d_build_scripts/linux/400
python build.py --prefix=$dir/cc3d_${vrsnwodt} --source-root=$srcdir --build-dir=$bdir --version=${vrsn} --cores=2 --conda-env-name=$env


