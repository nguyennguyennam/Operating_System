from MBR import*
from NTFS import *
from FAT32 import *

mbr_path = read_mbr (usb_path)
for partition in mbr_path:
    if partition.type == 0:
        read_NTFS(partition)
        print (partition.name)
    if partition.type == 1:
        read_FAT32(partition)