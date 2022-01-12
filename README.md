# Answering open-ended questions based on images using deep learning approach
A simple desktop Graphical User Interface for VQA (CNN+LSTM baseline model) system. Trained the VQA model on various standard CNNs like ResNet,VGG, Xception etc.

Visual question answering is an emerging problem which involves two of the major disciplines of artificial intelligence namely computer vision and natural language processing. This problem deals with answering various question related to an image which requires complete understanding of image as well as the question. The nature of questions, which are not restricted to a simple yes/no answers, makes it a challenging task for the machine. Understanding of the image is provided with the help of features extracted by convolutional neural networks. The question is analyzed using long short term memory(LSTM) recurrent neural networks. 

Steps to run the GUI Implementation (using pre trained weights - no trainig required)- 
1) Download the weights file from link given. Download the json and corresponding h5 file. Default is the vgg19 model, change the code accordingly for other models(in vqa_change .py)
[weights file](https://drive.google.com/open?id=10Y-Lhv8zObkVosJsVHU2xKLZvnQPL_n2)
2) Run the guitest.py file from terminal

Preprocess and training the network - 
1) Download the dataset from the main [VQA website](https://visualqa.org/download.html)
2) Download the required json files from this [link](https://drive.google.com/open?id=1-mLFx7JaSGE50tZG8Plg4DFUu3qzDAlC) and store them in Preprocessing folder.
3) Run the Preprocessing.ipynb notebook.
4) Output will be 3 npy files for image features, 1 npy for question features and 1 for labels.The generated npy files should be placed in the Training folder.
5) Run the Training.ipynb notebook to train the network
