# Blue whale photo-identification with LoFTR <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Building the Docker image](#building-the-docker-image)
- [Testing with sample images](#testing-with-sample-images)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Reference](#reference)

## Introduction

This repo contains the source code accompanying the paper "[Automated blue whale photo-identification using local feature matching](https://www.researchgate.net/publication/364141248_Automated_blue_whale_photo-identification_using_local_feature_matching)". Its purpose is to show that new local feature matching techniques such as LoFTR (or SuperGlue or HardNet or ...) can be used successfully to photo-identify blue whales (balaenoptera musculus). Good results have also been obtained for fin whales, i.e. balaenoptera physalus. The process is as follows: the image is first segmented to isolate the whale's body from the background, then a feature matcher finds correspondences between the segmented image and reference images from known whale individuals. The most likely candidate is the one with the "best" correspondences between its reference images and the image being analyzed. Since the approach is totally generic, it should be easy to adapt it to the photo-identification of other species.

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
for CPU execution or
```shell
nvidia-docker run -v .:/input <image name> /input/query1.jpg
```
for GPU execution.

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

The test images are provided courtesy of [MICS](https://www.rorqual.com/english/home)

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


