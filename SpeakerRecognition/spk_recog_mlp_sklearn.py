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
# ただし識別器は全結合層からなるニューラルネットワーク in scikit-learn

import glob
import os

import numpy as np
import scipy.stats
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


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


def get_dataset(feats, labels, train_index, test_index):
    """Get train/test data."""
    x_train_val = feats[train_index]
    t_train_val = labels[train_index]
    x_test = feats[test_index]
    t_test = labels[test_index]
    scaler = StandardScaler()
    scaler.fit(x_train_val)
    x_train_val_std = scaler.transform(x_train_val)
    x_test_std = scaler.transform(x_test)
    return x_train_val_std, t_train_val, x_test_std, t_test


def compute_classification_report(t_test, pred, stats):
    """Compute accuracy, recall, precision, and F1-score in a cv-fold."""
    print(classification_report(t_test, pred, digits=4))
    report = classification_report(t_test, pred, digits=4, output_dict=True)
    acc = report["accuracy"] * 100
    rec = report["macro avg"]["recall"] * 100
    prec = report["macro avg"]["precision"] * 100
    f1_score = report["macro avg"]["f1-score"] * 100
    print(
        f"Accuracy = {acc:.2f}%, "
        f"Recall = {rec:.2f}%, "
        f"Precision={prec:.2f}%, "
        f"F1-score = {f1_score:.2f}%"
    )
    stats["accuracy"].append(acc)
    stats["recall"].append(rec)
    stats["precision"].append(prec)
    stats["f1_score"].append(f1_score)


def compute_stats(stats):
    """Compute accuracy, recall, precision, and F1-score over cv-splits."""
    acc_array = np.array(stats["accuracy"])
    min_int, max_int = scipy.stats.t.interval(
        alpha=0.95,
        df=len(acc_array) - 1,
        loc=np.mean(acc_array),
        scale=scipy.stats.sem(acc_array),
    )
    max_int = 100 if max_int > 100 else max_int
    mean = {"acc": 0.0, "rec": 0.0, "prec": 0.0, "f1": 0.0}
    std = {"acc": 0.0, "rec": 0.0, "prec": 0.0, "f1": 0.0}
    mean["acc"] = np.array(stats["accuracy"]).mean()
    mean["prec"] = np.array(stats["precision"]).mean()
    mean["rec"] = np.array(stats["recall"]).mean()
    mean["f1"] = np.array(stats["f1_score"]).mean()
    std["acc"] = np.array(stats["accuracy"]).std()
    std["prec"] = np.array(stats["precision"]).std()
    std["rec"] = np.array(stats["recall"]).std()
    std["f1"] = np.array(stats["f1_score"]).std()
    print(f"Averaged acc = {mean['acc']:.2f} ± {std['acc']:.2f}%")
    print(f"Averaged precision = {mean['prec']:.2f} ± {std['prec']:.2f}%")
    print(f"Averaged recall = {mean['rec']:.2f} ± {std['rec']:.2f}%")
    print(f"Averaged F1-score = {mean['f1']:.2f} ± {std['f1']:.2f}%")
    print(f"Acc with CI = {min_int:.2f}, {max_int:.2f}")


def main(cfg):
    """Perform training for speaker recognition using xvectors."""
    print(OmegaConf.to_yaml(cfg), flush=True)  # dump configuration
    feats, labels = load_feats(cfg)
    stats = {"accuracy": [], "recall": [], "precision": [], "f1_score": []}
    skf = StratifiedKFold(
        n_splits=cfg.training.n_splits, shuffle=True, random_state=cfg.training.seed
    )
    for i, (train_index, test_index) in enumerate(skf.split(feats, labels)):
        print(f"Start training of {i}-th split:")
        x_train_val_std, t_train_val, x_test_std, t_test = get_dataset(
            feats, labels, train_index, test_index
        )
        mlp = MLPClassifier(
            hidden_layer_sizes=cfg.model.layer_sizes,
            max_iter=cfg.training.n_epoch,
            batch_size=cfg.training.n_batch,
            activation=cfg.model.activation,
            learning_rate_init=cfg.training.learning_rate,
            random_state=cfg.training.seed,
        )
        mlp.fit(x_train_val_std, t_train_val)
        pred = mlp.predict(x_test_std)
        compute_classification_report(t_test, pred, stats)

    compute_stats(stats)


if __name__ == "__main__":
    with initialize(version_base=None, config_path="."):
        config = compose(config_name="config_sklearn")
    main(config)
