# Blue whale photo-identification with LoFTR <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Building the Docker image](#building-the-docker-image)
- [Testing with sample images](#testing-with-sample-images)
- [Contributors and Acknowledgments](#contributors-and-acknowledgments)
- [Licenses](#licenses)
- [Reference](#reference)
  - [Citation](#citation)


## Introduction

## Building the Docker image

In order to facilitate the use of the provided source code, a Dockerfile is supplied with
Building the Docker image is as follows:

```shell
sudo docker build .
```

## Testing with sample images

Images of two blue whales (B271 and B275) are bundled with the source code to allow for a quick test. Once the Docker image is built, simply type:
```shell
docker run -v .:/input <image name> /input/query1.jpg
```
or
```shell
nvidia-docker run -v .:/input <image name> /input/query1.jpg
```

The output should be:
```
Downloading: "https://github.com/DagnyT/hardnet/raw/master/pretrained/train_liberty_with_aug/checkpoint_liberty_with_aug.pth" to /home/user/.cache/torch/hub/checkpoints/checkpoint_liberty_with_aug.pth
100%|██████████| 5.10M/5.10M [00:00<00:00, 114MB/s]
Downloading: "https://download.pytorch.org/models/resnet34-333f7ec4.pth" to /home/user/.cache/torch/hub/checkpoints/resnet34-333f7ec4.pth
100%|██████████| 83.3M/83.3M [00:02<00:00, 31.9MB/s]Opening dataset dset_Bm_RSD.txt
2 candidates
B275:23.913230895996094 -> Most likely candidate
B271:9.846597671508789 
```

## Acknowledgments

* LoFTR: https://github.com/zju3dv/LoFTR

* BASNet: https://github.com/xuebinqin/BASNet

## License

This work is released under an MIT license.

## Reference

Please reference this work using the following citation.

```bibtex
@inproceedings{inproceedings,
author = {Lalonde, Marc and Landry, David and Sears, Richard},
title = {Automated blue whale photo-identification using local feature matching},
booktitle = {Proc. CVAUI 2022},
year = {2022},
month = {August}, 
address = {Montreal, Canada}
}
```


