from wnpmonsoon.netcdfdata import NetcdfData


def test_first_point():
    nc = NetcdfData(file_)
    assert nc.pr_unit_conversion() == nc.variable[0, 0, 0]


def test_middle_point():
    assert()
