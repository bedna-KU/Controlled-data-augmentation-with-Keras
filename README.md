# Controlled data augmentation with Keras

## Why
Blog in Slovak language https://linuxos.sk/blog/zumpa/detail/umela-inteligencia-data-augmentation/

## Installation
```
git clone https://github.com/bedna-KU/Controlled-data-augmentation-with-Keras.git
cd Controlled-data-augmentation-with-Keras
python3 -m pip install -r requirements.txt
```

## Options
    --count count of generated images
    --input directory with input images
    --output directory for output augmented images (if no set then output = input)
    --action show or save

## Parameters
Change in file keras_data_aug.py

![Keras data augmentation parameters](https://raw.githubusercontent.com/bedna-KU/Controlled-data-augmentation-with-Keras/master/keras_data_augmentation_parameters.jpg)

## Preview augmented images
python3 keras_data_aug.py --count 25 --input "images" --output "images_aug" --action show

![Preview images](https://raw.githubusercontent.com/bedna-KU/Controlled-data-augmentation-with-Keras/master/Preview_window_keras_data_augmentation.png)

## Save augmented images
python3 keras_data_aug.py --count 25 --input "images" --output "images_aug" --action save

# Controlled data augmentation without Keras - blur and noise

## Options
    --input directory with input images
    --output directory for output augmented images (if no set then output = input)
    --action show, blur or noise

## Preview augmented images
python3 blur_and_noise.py --input images --output images_aug --action show

![Preview images](https://raw.githubusercontent.com/bedna-KU/Controlled-data-augmentation-with-Keras/master/blur_and_noise.png)

## Save blur images
python3 blur_and_noise.py --input images --output images_aug --action blur

## Save noise images
python3 blur_and_noise.py --input images --output images_aug --action noise
