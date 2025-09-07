from authorship_attribution.models import Verifier
from authorship_attribution.train import load_model, train

__all__ = ["train", "load_model", "Verifier"]


def main() -> None:
    print("Hello from authorship-attribution!")
