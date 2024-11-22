# [CVPR 2024 Highlight] Gaussian-Flow: 4D Reconstruction with Dynamic 3D Gaussian Particle

This is the official implementation of *Gaussian-Flow: 4D Reconstruction with Dynamic 3D Gaussian Particle*. 
> Note: We swiched to the [Pointrix](https://github.com/pointrix-project/pointrix) framework for a more efficient and cleaner implementation. The codebase is still under development and will be updated frequently.

### [Project Page](https://nju-3dv.github.io/projects/Gaussian-Flow/) | [Paper](https://openaccess.thecvf.com/content/CVPR2024/papers/Lin_Gaussian-Flow_4D_Reconstruction_with_Dynamic_3D_Gaussian_Particle_CVPR_2024_paper.pdf) | [Arxiv](https://arxiv.org/abs/2312.03431)

![Teaser](assets/teaser_traj2.png)

## Prepare the Environment

First, install the latest version of `pointrix`:

```bash
git clone https://github.com/pointrix-project/pointrix.git --recursive
cd pointrix
python -m pip install -r requirements.txt
python -m pip install .
```

Next, install `polyfourier`:

```bash
python -m pip install git+https://github.com/Linyou/polyfourier.git
```

## Running the Experiments

To run the `Nerfies Dataset` experiments, use the following command:

```bash
python launch.py --config configs/nerfies.yaml datapipeline.dataset.data_path='path/to/nerfies/dataset'
```

> **Note:** The latest `pointrix` includes a web GUI for monitoring the training process. Access it by opening a browser and navigating to `http://localhost:8918`.

## Custom Datasets

If you wish to reconstruct a custom dataset, you can running the following command:

```bash
# Install Colmap
conda install -c conda-forge colmap

# Install nerfstudio
python -m pip install nerfstudio

# Precessing the data
ns-process-data {images, video} --data {DATA_PATH} --output-dir {PROCESSED_DATA_DIR}

# Running the reconstruction
python launch.py --config configs/custom.yaml datapipeline.dataset.data_path='path/to/custom/dataset'
```

## Acknowledgement

Thanks to the developers and contributors of the following open-source repositories, whose invaluable work has greatly inspire our project:

- [Pointrix](https://github.com/pointrix-project/pointrix): A differentiable point-based rendering framework.
- [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting): 3D Gaussian Splatting for Real-Time Radiance Field Rendering.

## Citation

If you find this codebase useful, please consider cite our work.

```latex
@inproceedings{lin2024gaussian,
  title={Gaussian-flow: 4d reconstruction with dynamic 3d gaussian particle},
  author={Lin, Youtian and Dai, Zuozhuo and Zhu, Siyu and Yao, Yao},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={21136--21145},
  year={2024}
}
```
