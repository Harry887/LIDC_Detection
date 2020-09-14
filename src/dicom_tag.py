import pydicom
import pylidc as pl


def read_dicom():
    ds = pydicom.read_file(
        "data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/000001.dcm")
    print(ds)


def query():
    scans = pl.query(pl.Scan).filter(pl.Scan.slice_thickness <= 1,
                                     pl.Scan.pixel_spacing <= 0.6)
    print(scans.count())
    pid = 'LIDC-IDRI-0078'
    scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).first()
    print(scan)
    print(len(scan.annotations))

    nods = scan.cluster_annotations()
    print("%s has %d nodules." % (scan, len(nods)))
    # => Scan(id=1,patient_id=LIDC-IDRI-0078) has 4 nodules.

    for i, nod in enumerate(nods):
        print("Nodule %d has %d annotations." % (i+1, len(nods[i])))
    vol = scan.to_volume()
    print(vol.shape)
    # => (512, 512, 87)

    print("%.2f, %.2f" % (vol.mean(), vol.std()))
    # => -702.15, 812.52
    scan.visualize(annotation_groups=nods)


if __name__ == "__main__":
    query()
