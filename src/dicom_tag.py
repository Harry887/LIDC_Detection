import pydicom

ds = pydicom.read_file(
    "data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/000001.dcm")
print(ds)
