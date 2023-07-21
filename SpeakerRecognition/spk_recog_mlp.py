#!/usr/bin/env python3
"""Training script for Multi-layer Feedforward Neural Network.

Copyright (C) 2023 by Akira TAMAMORI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Commentary:
# 抽出済のxvectorを使った話者認識
# ただし識別器は全結合層からなるニューラルネットワーク

import glob
import os
from collections import namedtuple

import numpy as np
import torch
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from torch import nn, optim


def init_manual_seed(random_seed: int):
    """Initialize manual seed."""
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_feats(cfg: DictConfig):
    """Load features and labels."""
    feat_dir = os.path.join(cfg.xvector.root_dir, cfg.xvector.feat_dir)
    feats = {}
    labels = {}
    for actor in cfg.actor:
        feats[actor] = []
        labels[actor] = []
        for emotion in cfg.emotion:
            feat_files = glob.glob(feat_dir + actor + f"/{actor}_{emotion}_*.npy")
            for feat_file in feat_files:
                xvector = np.load(feat_file)
                xvector = np.expand_dims(xvector, axis=0)
                feats[actor].append(xvector)
                if actor == "tsuchiya":
                    labels[actor].append(0)
                elif actor == "fujitou":
                    labels[actor].append(1)
                elif actor == "uemura":
                    labels[actor].append(2)
        feats[actor] = np.concatenate(feats[actor])
    feats = np.concatenate(list(feats.values()))
    labels = np.concatenate(list(labels.values()))
    return feats, labels


class MyDataset(torch.utils.data.Dataset):
    """Dataset."""

    def __init__(self, feats, labels, transform=None):
        """Initialize class."""
        self.transform = transform
        self.feats = feats
        self.labels = labels

    def __len__(self):
        """Return the size of the dataset.

        Returns:
            int: size of the dataset
        """
        return self.feats.shape[0]

    def __getitem__(self, idx):
        """Get a pair of input and target.

        Args:
            idx (int): index of the pair

        Returns:
            tuple: input and target in numpy format
        """
        feat = self.feats[idx, :]
        label = self.labels[idx]
        return (feat, label)


def get_dataloader(cfg, feats, labels, train_index, test_index):
    """Get Dataloaders for training and test."""
    x_train_val = feats[train_index]
    t_train_val = labels[train_index]
    x_test = feats[test_index]
    t_test = labels[test_index]

    scaler = StandardScaler()
    scaler.fit(x_train_val)
    x_train_val_std = scaler.transform(x_train_val)
    x_test_std = scaler.transform(x_test)

    train_dataloader = torch.utils.data.DataLoader(
        dataset=MyDataset(feats=x_train_val_std, labels=t_train_val),
        batch_size=cfg.training.n_batch,
        shuffle=True,
        drop_last=True,
    )
    test_dataloader = torch.utils.data.DataLoader(
        dataset=MyDataset(feats=x_test_std, labels=t_test),
        batch_size=cfg.training.n_batch,
        shuffle=False,
        drop_last=False,
    )
    return train_dataloader, test_dataloader


class MultiLayerPerceptron(nn.Module):
    """Class MultiLayerPerceptron."""

    def __init__(self, cfg, n_classes=3):
        """Initialize class."""
        super().__init__()
        x_dim = cfg.model.x_dim
        h_dim = cfg.model.h_dim
        n_layers = cfg.model.n_layers
        self.n_layers = n_layers  # number of hidden layers
        self.n_classes = n_classes  # number of classes (= number of sections)

        layers = nn.ModuleList([])
        layers += [nn.Linear(x_dim, h_dim)]
        layers += [nn.Linear(h_dim, h_dim) for _ in range(self.n_layers)]
        layers += [nn.Linear(h_dim, n_classes)]
        self.layers = nn.ModuleList(layers)

        bnorms = [nn.BatchNorm1d(h_dim) for _ in range(self.n_layers + 1)]
        self.bnorms = nn.ModuleList(bnorms)

        self.activation = nn.ReLU()
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, inputs):
        """Perform forward propagation."""
        hidden = inputs
        for i in range(self.n_layers):
            hidden = self.activation(self.bnorms[i](self.layers[i](hidden)))
        output = self.layers[-1](self.activation(hidden))  # (n_classes)
        return output

    def get_loss(self, inputs, labels):
        """Compute loss function."""
        outputs = self.forward(inputs)
        loss = self.criterion(outputs, labels)
        return loss, outputs


def get_classifier(cfg: DictConfig, device: torch.device, n_classes: int = 3):
    """Instantiate classifier."""
    return MultiLayerPerceptron(cfg, n_classes=n_classes).to(device)


def get_optimizer(cfg: DictConfig, model):
    """Instantiate optimizer."""
    optimizer_class = getattr(optim, cfg.training.optim.optimizer.name)
    optimizer = optimizer_class(
        model.parameters(), **cfg.training.optim.optimizer.params
    )
    return optimizer


def get_lr_scheduler(cfg: DictConfig, optimizer):
    """Instantiate scheduler."""
    lr_scheduler_class = getattr(
        optim.lr_scheduler, cfg.training.optim.lr_scheduler.name
    )
    lr_scheduler = lr_scheduler_class(
        optimizer, **cfg.training.optim.lr_scheduler.params
    )
    return lr_scheduler


def training_epoch(
    cfg: DictConfig, train_dataloader, test_dataloader, modules, device: torch.device
):
    """Perform training in a epoch."""
    var = {"epoch_loss": 0.0, "test_loss": 0.0, "correct": 0, "total": 0, "acc": 0.0}
    modules.model.train()
    for epoch in range(1, cfg.training.n_epoch + 1):
        print(f"Epoch {epoch:2d}: ", end="")
        var["epoch_loss"] = 0.0
        var["correct"] = 0
        var["total"] = 0
        for data, label in train_dataloader:
            data = data.to(device).float()
            label = label.to(device).long()
            modules.optimizer.zero_grad()
            loss, outputs = modules.model.get_loss(data, label)
            _, predicted = torch.max(outputs, 1)
            loss.backward()
            modules.optimizer.step()
            var["epoch_loss"] += loss.item()
            var["correct"] += (predicted == label).sum().item()
            var["total"] += label.size(0)
        if modules.lr_scheduler is not None:
            modules.lr_scheduler.step()

        print(
            f" train_loss: {var['epoch_loss'] / len(train_dataloader):.6f} - ",
            end="",
        )
        acc = 100 * float(var["correct"] / var["total"])
        print(
            f"accuracy: {acc:.6f}% ({var['correct']}/{var['total']})",
            end="",
        )

        var["test_loss"] = 0.0
        var["correct"] = 0
        var["total"] = 0
        modules.model.eval()
        with torch.no_grad():
            for data, label in test_dataloader:
                data = data.to(device).float()
                label = label.to(device).long()
                loss, outputs = modules.model.get_loss(data, label)
                var["test_loss"] += loss.item()
                _, predicted = torch.max(outputs, 1)
                var["correct"] += (predicted == label).sum().item()
                var["total"] += label.size(0)
        print(
            f"    test_loss: {var['test_loss'] / len(test_dataloader):.6f} - ",
            end="",
        )
        var["acc"] = 100 * float(var["correct"] / var["total"])
        print(f"accuracy: {var['acc']:.6f}% ({var['correct']}/{var['total']})")


def compute_acc(dataloader, model, device):
    """Compute classification accuracy."""
    pred = []
    correct_label = []
    model.eval()
    with torch.no_grad():
        for data, label in dataloader:
            feat = data.to(device).float()
            label = label.to(device).long()
            outputs = model(feat)
            _, predicted = torch.max(outputs, 1)
            correct_label.append(label.to("cpu").detach().numpy().copy())
            pred.append(predicted.to("cpu").detach().numpy().copy())
            _, predicted = torch.max(outputs, 1)
    pred = np.concatenate(pred)
    correct_label = np.concatenate(correct_label)
    print(classification_report(correct_label, pred, digits=4))


def main(cfg):
    """Perform training for speaker recognition using xvectors."""
    print(OmegaConf.to_yaml(cfg), flush=True)  # dump configuration
    init_manual_seed(cfg.training.seed)
    feats, labels = load_feats(cfg)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    TrainingModules = namedtuple(
        "TrainingModules",
        ["model", "optimizer", "lr_scheduler"],
    )
    skf = StratifiedKFold(
        n_splits=cfg.training.n_splits, shuffle=True, random_state=cfg.training.seed
    )
    for i, (train_index, test_index) in enumerate(skf.split(feats, labels)):
        print(f"Start training of {i}-th split:")
        train_dataloader, test_dataloader = get_dataloader(
            cfg, feats, labels, train_index, test_index
        )
        model = get_classifier(cfg, device)
        optimizer = get_optimizer(cfg, model)
        lr_scheduler = None
        if cfg.training.use_scheduler:
            lr_scheduler = get_lr_scheduler(cfg, optimizer)
        modules = TrainingModules(
            model=model,
            optimizer=optimizer,
            lr_scheduler=lr_scheduler,
        )
        training_epoch(cfg, train_dataloader, test_dataloader, modules, device)
        compute_acc(test_dataloader, model, device)


if __name__ == "__main__":
    with initialize(version_base=None, config_path="."):
        config = compose(config_name="config")
    main(config)
