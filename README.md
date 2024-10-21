# blackhat

Sorting hat algorithm for images taken with the BlackGEM telescope array. BlackGEM is a three telescope array (currently) that takes photometric images on a 10,000 x 10,000 pixel custom fabricated CCD, where each telescope is equipped with six custom defined photometric filters. Each night, BlackGEM generates ~1000 images, and each image needs to be classified as Red, Orange, Yellow, or Green, denoting the average quality of the image. At the moment, we use fixed parameter ranges that roughly correspond to the quality of an image, however, we would like to develop a more data driven approach to classifying the images. The point of __blackhat__ is to classify an image based on the quality of a subset of random cutouts taken from the whole image. 


# Astronomical Image Classification Pipeline

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

A machine learning pipeline for classifying large astronomical images by analyzing cutouts using CNNs and aggregating predictions with a feed-forward neural network.

## Features

- Extracts fixed and random non-overlapping cutouts from large images.
- Classifies cutouts into four categories: good, acceptable, bad, unusable.
- Aggregates cutout predictions to classify the entire image.
- Utilizes PyTorch for model development and MLflow for experiment tracking.

## Installation

I'll eventaully provide a proper requirements wheel

## Project Structure

 - src/
  - __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_preparation.py
│   │   ├── datasets.py
│   │   └── transforms.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cnn_model.py
│   │   ├── whole_image_model.py
│   │   └── layers.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── train_cutout_classifier.py
│   │   ├── train_whole_image_classifier.py
│   │   └── utils.py
│   ├── inference/
│   │   ├── __init__.py
│   │   └── classify_image.py
│   └── config/
│       ├── __init__.py
│       └── config.yaml
├── data/
│   ├── fixed_positions.csv
│   └── sample_images/
│       └── (place small sample images here)
├── notebooks/
│   ├── exploratory_data_analysis.ipynb
│   └── model_evaluation.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_data_preparation.py
│   ├── test_models.py
│   └── test_training.py
├── scripts/
│   ├── download_data.sh
│   └── preprocess_data.py
├── mlruns/
│   └── (MLflow tracking directory)
└── docs/
    ├── installation.md
    ├── usage.md
    └── api_reference.md


## Contributing

 - Cole Johnston
 - Paul Vreeswijk


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

 - C. Johnston would like to thank the broader BlackGEM consortium team for their discussion and advice in building the algorithm. 

