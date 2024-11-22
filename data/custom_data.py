import os
import numpy as np
from pathlib import Path
from PIL import Image

from pointrix.dataset.utils.dataprior import CameraPrior, PointsPrior
from pointrix.dataset.base_data import BaseDataset, DATA_SET_REGISTRY
from pointrix.dataset.colmap_data import ColmapDataset
from pointrix.dataset.utils.dataset import load_from_json
from pointrix.logger.writer import Logger, ProgressLogger

from pointrix.dataset.utils.colmap  import (
    read_colmap_extrinsics,
    read_colmap_intrinsics,
    ExtractColmapCamInfo,
    read_3D_points_binary
)

class TimeCameraPrior(CameraPrior):
    def __init__(self, **kwargs):
        self.time = kwargs.pop('time')
        super().__init__(**kwargs)


@DATA_SET_REGISTRY.register()
class CustomDataset(ColmapDataset):
    
    def load_camera_prior(self, split: str):

        extrinsics = read_colmap_extrinsics(self.data_root / Path("sparse/0") / Path("images.bin"))
        intrinsics = read_colmap_intrinsics(self.data_root / Path("sparse/0") / Path("cameras.bin"))
        
        total_frames = len(extrinsics)

        cameras = []
        for idx, key in enumerate(extrinsics):
            
            colmapextr = extrinsics[key]
            colmapintr = intrinsics[colmapextr.camera_id]
            R, T, fx, fy, cx, cy, width, height = ExtractColmapCamInfo(colmapextr, colmapintr, self.scale)

            id_str = os.path.basename(colmapextr.name).split('.')[0].split('frame_')[-1]
            # frame_0001.jpg -> 1
            id_num = int(id_str) - 1
            
            camera = TimeCameraPrior(
                idx=idx, R=R, T=T,
                image_width=width, 
                image_height=height, 
                rgb_file_name=os.path.basename(colmapextr.name),
                fx=fx, fy=fy, 
                cx=cx, cy=cy, 
                time = id_num / total_frames,
            )
            cameras.append(camera)
        sorted_camera = sorted(cameras.copy(), key=lambda x: x.rgb_file_name)
        self.cameras = sorted_camera
        return self.cameras
    
    def load_observed_data(self, split):
        """
        The function for loading the observed_data.

        Parameters:
        -----------
        split: str
            The split of the dataset.
        
        Returns:
        --------
        observed_data: List[Dict[str, Any]]
            The observed_datafor the dataset.
        """
        observed_data = []
        for k, v in self.observed_data_dirs_dict.items():
            observed_data_path = self.data_root / Path(v)
            if not os.path.exists(observed_data_path):
                Logger.error(f"observed_data path {observed_data_path} does not exist.")
            observed_data_file_names = sorted(os.listdir(observed_data_path))
            cached_progress = ProgressLogger(description='Loading cached observed_data', suffix='iters/s')
            cached_progress.add_task(f'cache_{k}', f'Loading {split} cached {k}', len(observed_data_file_names))
            with cached_progress.progress as progress:
                for idx, file in enumerate(observed_data_file_names):
                    if len(observed_data) <= idx:
                        observed_data.append({})
                    if file.endswith('.npy'):
                        observed_data[idx].update({k: np.load(observed_data_path / Path(file))})
                    elif file.endswith('png') or file.endswith('jpg') or file.endswith('JPG'):
                        observed_data[idx].update({k: Image.open(observed_data_path / Path(file))})
                    else:
                        print(f"File format {file} is not supported.")
                    cached_progress.update(f'cache_{k}', step=1)
        return observed_data
