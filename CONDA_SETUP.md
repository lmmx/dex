```
conda create -n dex "python=3.9"
conda activate dex
conda install -y pytorch torchvision cudatoolkit=11.3 -c pytorch
pip install -r requirements.txt
```

For earlier versions of CUDA:
```
conda install -y "cudatoolkit<11.2" -c conda-forge
conda install -y pytorch torchvision -c pytorch
```
