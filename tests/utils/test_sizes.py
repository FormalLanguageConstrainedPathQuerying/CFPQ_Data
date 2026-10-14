from sizes import format_size_mb


def test_format_size_mb_below_one_megabyte_uses_three_decimals():
    assert format_size_mb(2472) == "0.002"
    assert format_size_mb(988000) == "0.988"
    assert format_size_mb(123456) == "0.123"


def test_format_size_mb_at_and_above_one_megabyte_uses_two_decimals():
    # 999,999 B is below one megabyte but rounds to 1.000 at three decimals.
    assert format_size_mb(999999) == "1.000"
    assert format_size_mb(1_000_000) == "1.00"
    assert format_size_mb(1_021_000) == "1.02"
    assert format_size_mb(59_987_425) == "59.99"


def test_format_size_mb_real_archive_sizes():
    # wc.tar.gz (5.0.0) and taxonomy_hierarchy.tar.gz (4.0.0), the smallest
    # and largest archives of the dataset.
    assert format_size_mb(2472) == "0.002"
    assert format_size_mb(112_652_191) == "112.65"


def test_format_size_mb_zero():
    assert format_size_mb(0) == "0.000"
