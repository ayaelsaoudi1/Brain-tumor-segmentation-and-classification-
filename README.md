# Brain Tumor Segmentation and Classification

## Project Abstract

In this project, our main focus has been on addressing the critical issue of brain tumor identification and classification using the power of advanced computer technologies and medical imaging techniques. By employing CNN and U-Net models on Kaggle datasets, we achieved strong results in brain tumor segmentation and classification. The workflow involves preprocessing MRI scans, training models with appropriate metrics, and fine-tuning hyperparameters to deploy successful models for clinical automation.

We aimed to develop a comprehensive solution that combines Convolutional Neural Networks (CNNs) and U-Net to achieve accurate tumor classification and precise segmentation in MRI scans. To ensure the effectiveness of our models, we diligently preprocessed the MRI images by applying various adjustments, such as normalizing pixel values and resizing images to a common resolution. Additionally, we utilized data augmentation techniques to generate a more diverse and comprehensive training dataset, enhancing the model's ability to generalize and perform well on unseen data. Moreover, we created a user-friendly graphical interface powered by the PyQt5 library. This interface enables medical professionals to interact seamlessly with our technology, making the process of brain tumor analysis more intuitive and accessible.

## Data Used

The dataset employed in this study was sourced from Kaggle, a reputable platform for machine learning resources. It was meticulously organized into two distinct folders, each serving a crucial role in our research endeavors.

1. **Brain MRI Scans**: This folder contained high-resolution MRI scans focusing on cases with tumors. The images were stored in Portable Network Graphics (PNG) format to ensure optimal image quality and fidelity.

2. **Masked Tumors**: This folder contained the corresponding masked tumor images. The masks were created to highlight the tumor regions in white against a black background, facilitating the precise localization of tumors.

Both folders contained an identical number of images, totaling 3064 pairs, ensuring fairness during model training and evaluation. This dataset provided a robust foundation for our tumor detection and analysis models.

- **URL to the dataset used for U-Net training**: [Kaggle Brain Tumor Segmentation Dataset](https://www.kaggle.com/datasets/nikhilroxtomar/brain-tumor-segmentation)

The dataset used to train and test the CNN model is similarly sourced from Kaggle, offering a comprehensive set of MRI images categorized into multiple brain tumor classes.

- **URL to the dataset used for CNN model training**: [Kaggle Brain Tumor Classification Dataset](https://www.kaggle.com/sartajbhuvaji/brain-tumor-classification-mri)

## GUI Results

We leveraged the powerful capabilities of the **PyQt5** library to create a user-friendly graphical user interface (GUI). PyQt5, a Python binding for the Qt framework, enabled us to develop a feature-rich, cross-platform desktop application. This interactive interface allowed users to upload MRI images, detect tumors, and view results such as segmented tumor images and classifications of tumor types.

The graphical interface was designed to be intuitive, offering an accessible platform for clinicians and researchers to interact with the system. Figure 43 below showcases the GUI, where users can select an MRI image, process it by clicking the "Detect" button, and view both the tumor segmentation and classification result.

For more information about the project, check the [report here](https://github.com/ayaelsaoudi1/Brain-tumor-segmentation-and-classification-/blob/main/Brain%20Tumor%20Segmentation%20and%20Classification.pdf).
