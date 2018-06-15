import pytest
from ..tools import image_analysis as ia
import numpy as np
from itertools import product



def test_nearest_pixel():
    assert ia.ImageTools.nearest_pixel(1) == 1
    assert ia.ImageTools.nearest_pixel(1.25) == 1
    assert ia.ImageTools.nearest_pixel(1.65) == 2
    assert ia.ImageTools.nearest_pixel([1, 1.25, 1.65]) == [1, 1, 2]
    test_array = np.ndarray(shape=(2,2), dtype=float)
    assert np.allclose(test_array.round(),
                       ia.ImageTools.nearest_pixel(test_array),
                       rtol=0.1,
                       atol=0.1,
                       equal_nan=True)
    with pytest.raises(TypeError):
        ia.ImageTools.nearest_pixel(['string'])


def test_in_ellipse():
    center = (0, 0)
    width = 1
    height = 1
    for x, y in product(np.random.uniform(-2, 2, 100), np.random.uniform(-2, 2, 100)):
        assert ia.ImageTools.in_ellipse(x, y, center, width, height) == (x**2 + y**2 <=1)
