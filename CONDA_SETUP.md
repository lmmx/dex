```
conda create -n dex python=3.10 -y
conda activate dex
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
pip install spindex[surya]
```
