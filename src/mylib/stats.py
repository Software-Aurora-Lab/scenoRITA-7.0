from bisect import bisect_left
from typing import List, Tuple

import numpy as np
from scipy.stats import mannwhitneyu, rankdata


def print_header(text: str):
    title_length = len(text)
    print("=" * title_length)
    print(text)
    print("=" * title_length)


def statistical_difference_test(
    A: List[float], B: List[float], verbose: bool = True
) -> Tuple[float, float]:
    """
    Mann-Whitney U Test
    :param A: sample A
    :param B: sample B
    :param verbose: print the test result
    :return: U1, p
    """
    # Null hypothesis: the distributions of both samples are equal.
    # Alternative hypothesis: the distributions of both samples are not equal.
    # If p-value is less than the significance level (alpha),
    #   we reject the null hypothesis.
    # alpha = 0.05
    U1, p = mannwhitneyu(A, B)
    if verbose:
        print_header("Mann-Whitney U Test")
        print("U1=%.3f, p=%.3f" % (U1, p))
        if p > 0.05:
            print("Same distribution (fail to reject H0)")
        else:
            print("Different distribution (reject H0)")
        print()

    return U1, p


def effect_size_test(
    A: List[float], B: List[float], verbose: bool = True
) -> Tuple[float, str]:
    """
    Vargha and Delaney A12 Test
    :param A: sample A
    :param B: sample B
    :param verbose: print the test result
    :return: A12, significance
    """
    # A12 non-parametric effect size test
    m = len(A)
    n = len(B)
    assert m == n, "The two samples must have the same size."
    r = rankdata(A + B)
    r1 = sum(r[:m])

    A12 = (r1 / m - (m + 1) / 2) / n
    levels = [0.147, 0.33, 0.474]  # effect sizes from Hess and Kromrey, 2004
    magnitude = ["negligible", "small", "medium", "large"]
    scaled_A = (A12 - 0.5) * 2

    significance = magnitude[bisect_left(levels, abs(scaled_A))]

    if verbose:
        print_header("Vargha and Delaney A12 Test")
        print("A12=%.3f, magnitude=%s" % (A12, significance))

    return A12, significance


def compare(A: List[float], B: List[float]):
    print_header("Sample Data")
    print("Sample A:", A)
    print("Sample B:", B)
    print()

    statistical_difference_test(A, B, True)
    effect_size_test(A, B, True)


if __name__ == "__main__":
    A = list(np.random.rand(10))
    B = list(np.random.rand(10))

    compare(A, B)
