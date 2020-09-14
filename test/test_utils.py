from src.demo import load_scans, count_files, plot_HU_range


def test_load_scans():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    slice_info = load_scans(slice_path)
    print(slice_info)


def test_count_files():
    path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0106/"
    assert count_files(path) == 159


def test_plot_HU_range():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    file_name = "HU_range"
    scans = load_scans(slice_path)
    plot_HU_range(scans, file_name)
