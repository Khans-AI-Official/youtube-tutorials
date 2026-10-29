# 08 · Build Your First Neural Network in PyTorch (Fashion-MNIST)

Code for the Khan's AI video. A small fully connected network (784 → 128 → 10) that classifies Fashion-MNIST clothing images.

## Results from the run in the video (CPU, 2 cores)

| | |
|---|---|
| Parameters | 101,770 |
| Training time (10 epochs) | 49 s |
| Validation accuracy after 10 epochs | 88.60% |
| Test accuracy (10,000 unseen images) | 87.78% |
| Hidden neurons that never activate | 19 of 128 |

Weakest classes: Pullover (71.7%) and Shirt (72.6%). Biggest confusion: 143 shirts predicted as T-shirt/top.

## Run it

```bash
pip install -r requirements.txt
python explore.py          # downloads Fashion-MNIST on first run, prints shapes and classes
python train.py            # trains for 10 epochs, saves fashion_model.pt
python evaluate.py         # test accuracy, accuracy per class, biggest mistakes
python inspect_neurons.py  # counts hidden neurons that never switch on
python predict.py          # predictions with confidence for a few test images
```

Results can differ slightly on other hardware or library versions.

Dataset: [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) by Zalando Research, MIT licence.
