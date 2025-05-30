import pytest
import shutil
import torch
from ssm import Trainer
from ssm.model import S4, S6, Mamba
from ssm import CopyDataset
from ssm import MetricTracker
from ssm.model.block.embedding_block import EmbeddingBlock

model_dim = 20
hid_dim = 12
output_dim = 5
vocab_size = 5
mem_tokens = 10

S4_model = S4(
    block_type="S4",
    method="convolutional",
    model_dim=model_dim,
    hid_dim=hid_dim,
    n_layers=2,
    hippo=True,
)

S6_model = S6(
    model_dim=model_dim,
    hid_dim=hid_dim,
    n_layers=2,
)

Mamba_model = Mamba(
    model_dim=model_dim,
    hid_dim=hid_dim,
    n_layers=1,
    expansion_factor=2,
    kernel_size=3,
    method="convolutional",
    hippo=True,
)

dataset = CopyDataset(
    sequence_len=50,
    batch_size=12,
    vocab_size=vocab_size,
    mem_tokens=mem_tokens,
    selective=False,
)

embedded_model = EmbeddingBlock(
    model=S4_model,
    model_dim=model_dim,
    vocab_size=vocab_size,
    out_dim=output_dim,
    mem_tokens=10,
)


@pytest.mark.parametrize("model", [S4_model, S6_model, Mamba_model])
def test_constructor(model):

    embedded_model.model = model
    metric_tracker = MetricTracker(
        repo="tests/",
        experiment="logs",
        tensorboard_logger=True,
        logging_steps=10,
    )

    Trainer(
        model=embedded_model,
        steps=100,
        test_steps=10,
        dataset=dataset,
        metric_tracker=metric_tracker,
        device="cpu",
    )


@pytest.mark.parametrize("model", [S4_model, Mamba_model])
def test_fit(model):
    embedded_model.model = model
    metric_tracker = MetricTracker(
        repo="tests/",
        experiment="logs",
        tensorboard_logger=True,
        logging_steps=10,
    )

    trainer = Trainer(
        model=embedded_model,
        dataset=dataset,
        steps=2,
        test_steps=10,
        metric_tracker=metric_tracker,
        device="cpu",
    )

    trainer.fit()
    shutil.rmtree("tests/logs/")


@pytest.mark.parametrize("tensorboard_logger", [True, False])
def test_tensorboard_logging(tensorboard_logger):

    embedded_model.model = S4_model
    metric_tracker = MetricTracker(
        repo="tests/",
        experiment="logs",
        tensorboard_logger=tensorboard_logger,
        logging_steps=10,
    )

    trainer = Trainer(
        model=embedded_model,
        dataset=dataset,
        steps=2,
        test_steps=10,
        metric_tracker=metric_tracker,
        device="cpu",
    )

    trainer.fit()

    shutil.rmtree("tests/logs/")


def test_custom_optimizer():
    embedded_model.model = S4_model
    metric_tracker = MetricTracker(
        repo="tests/",
        experiment="logs",
        tensorboard_logger=True,
        logging_steps=10,
    )

    trainer = Trainer(
        model=embedded_model,
        dataset=dataset,
        steps=2,
        metric_tracker=metric_tracker,
        test_steps=10,
        optimizer_params={"lr": 0.05, "weight_decay": 0.1},
        device="cpu",
    )

    assert isinstance(trainer.optimizer, torch.optim.Adam)
    assert trainer.optimizer.param_groups[0]["lr"] == 0.05
    assert trainer.optimizer.param_groups[0]["weight_decay"] == 0.1

    trainer = Trainer(
        model=S4_model,
        dataset=dataset,
        steps=2,
        test_steps=10,
        metric_tracker=metric_tracker,
        optimizer_class=torch.optim.SGD,
        optimizer_params={"lr": 0.07, "momentum": 0.9},
        device="cpu",
    )

    assert isinstance(trainer.optimizer, torch.optim.SGD)
    assert trainer.optimizer.param_groups[0]["lr"] == 0.07
    assert trainer.optimizer.param_groups[0]["momentum"] == 0.9


@pytest.mark.parametrize("model", [S4_model, Mamba_model])
def test_test(model):
    embedded_model.model = model
    metric_tracker = MetricTracker(
        repo="tests/",
        experiment="logs",
        tensorboard_logger=True,
        logging_steps=10,
    )

    trainer = Trainer(
        model=embedded_model,
        dataset=dataset,
        steps=2,
        metric_tracker=metric_tracker,
        test_steps=10,
        device="cpu",
    )

    trainer.fit()
    trainer.test()
    shutil.rmtree("tests/logs/")
