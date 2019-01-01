from wnpmonsoon.wind_direction import degfromnorth
import numpy as np


def test_30_deg():
    assert degfromnorth(np.sqrt(3), 1) == 240


def test_45_deg():
    assert degfromnorth(1, 1) == 225


def test_60_deg():
    assert degfromnorth(1, np.sqrt(3)) == 210


def test_90_deg():
    assert degfromnorth(0, 1) == 180


def test_120_deg():
    assert degfromnorth(-1, np.sqrt(3)) == 150


def test_135_deg():
    assert degfromnorth(1, -1) == 315


def test_150_deg():
    assert degfromnorth(-np.sqrt(3), 1) == 120


def test_180_deg():
    assert degfromnorth(-1, 0) == 90


def test_210_deg():
    assert degfromnorth(-np.sqrt(3), -1) == 60


def test_225_deg():
    assert degfromnorth(-1, -1) == 45


def test_240_deg():
    assert degfromnorth(-1, -np.sqrt(3)) == 30


def test_315_deg():
    assert degfromnorth(1, -1) == 315


def test_330_deg():
    assert degfromnorth(np.sqrt(3), -1) == 300


def test_all_as_array():
    uas = np.array([1, 1, 0, -np.sqrt(3), -1, np.sqrt(3), -1, -np.sqrt(3), -1, 1, -1, np.sqrt(3)])
    vas = np.array([1, np.sqrt(3), 1, 1, -1, -1, 0, -1, np.sqrt(3), -1, 1, -1])
    assert (degfromnorth(uas, vas) == np.array([225, 210, 180, 120, 45, 300, 90, 60, 150, 315, 135, 300])).all()
