#!/usr/bin/sh

dir=$HOME # Installation directory for CC3D
env=cc3d_2020 # conda environment for CC3D installation.
vrsn=4.2.5  # CC3D version. Don't change it!

vrsnwodt=${vrsn//./}
instldir=$dir/cc3d_${vrsnwodt}

conda activate $env

pypath=$(which python)
pydirpath=$(dirname "$pypath")

. cc3d_caller_env_var_set_linux.sh $instldir $pydirpath
python main_opt_nutrient_stress_mitosis.py
