FROM anibali/pytorch:1.8.1-cuda11.1-ubuntu20.04

COPY requirements_docker.txt /opt
RUN pip install -r /opt/requirements_docker.txt
RUN  sudo mkdir -p /opt/Bm_RSD
RUN  sudo mkdir -p /opt/models
COPY Bm_RSD /opt/Bm_RSD
COPY demo.py /opt
COPY src /opt/src
COPY dset_Bm_RSD.txt /opt
COPY models/outdoor_ds.ckpt /opt/models
# semantic segmentation
COPY models/basnet_fsi.pth /opt/models
# outputs list via stdout 
WORKDIR /opt
ENTRYPOINT  ["python3", "/opt/demo.py"]  # At execution, expects args: <jpgfile>  [--mask_filename filename]  where "filename" is e.g. "mask.png"
