# Gaussian-Flow

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
