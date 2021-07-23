#!/usr/bin/sh
set -e
pyvrsn=3.7 # Conda python version.
env=cc3d_2020 # conda environment for CC3D installation.
vrsn=4.2.5  # CC3D version. Don't change it!
vrsnwodt=${vrsn//./}
currdir=$PWD
dir=$HOME # Installation directory for CC3D
echo $dir
srcdir=${dir}/CC3D_GIT # Source Directory for CC3D.
bdir=${dir}/cc3d_${vrsnwodt}_build # Build Directory for CC3D.
instldir=$dir/cc3d_${vrsnwodt}
cd ${dir}

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
# unable to use 'source' command. Instead using '.' in next line
. $HOME/.bashrc
conda activate
conda create -n $env python=$pyvrsn
conda activate $env
conda install -y -c conda-forge numpy scipy pandas jinja2 webcolors vtk=8.2 pyqt pyqtgraph deprecated qscintilla2 jinja2 chardet cmake swig=3 requests
conda install -y -c conda-forge  scipy=1.7.0
conda install -y -c compucell3d tbb_full_dev
pip install libroadrunner
pip install antimony

conda activate base

sudo apt-get install -y g++ build-essential git libglu1-mesa libxi-dev libxmu-dev libglu1-mesa-dev
sudo ln -sf /usr/lib/x86_64-linux-gnu /usr/lib64
mkdir $srcdir
cd $srcdir
git clone https://github.com/CompuCell3D/CompuCell3D.git .
git clone https://github.com/CompuCell3D/cc3d_build_scripts.git
cd cc3d_build_scripts/linux/400
export CPLUS_INCLUDE_PATH=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")
python build.py --prefix=$instldir --source-root=$srcdir --build-dir=$bdir --version=${vrsn} --cores=1 --conda-env-name=$env
conda activate $env
pypath=$(which python)
pydirpath=$(dirname "$pypath")
cp -r $currdir $instldir/Demos/CallableCC3D/
cd $instldir/Demos/CallableCC3D/cc3d-scipyOptimize
bash cc3d_caller_env_var_set_linux.sh $instldir $pydirpath

python main_opt_nutrient_stress_mitosis.py

