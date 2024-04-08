import os

class DATE:
    def __init__(self, day, mon, year, h, m, s):
        self.day = day
        self.mon = mon
        self.year = year
        self.h = h
        self.m = m
        self.s = s

class save_data:
    def __init__(self, type = None, file_name = None, attri = None, time = None, size = None, start = None, hid = None, id = None, parent = None, data = None):
        self.name = file_name
        self.type = type # 0 là FOLDER, 1 là FILE
        self.attri = attri
        self.name = file_name
        self.time = time
        self.size = size
        self.start = start #CLUSTER
        self.hidden = hid
        self.id = id
        self.parent = parent
        self.data = data
        self.son = []

    def getDate (self):
        return self.time

    def setInfor(self, type, attri, time, size, start, hid, id, data = None,name = None):
        self.type = type # 0 là FOLDER, 1 là FILE
        self.attri = attri
        self.time = time
        self.size = size
        self.start = start #CLUSTER
        self.hidden = hid
        self.id = id
        self.data = data
        
        self.son = []
    def setData(self, data):
        self.data = data
    def setName(self, file_name):
        self.name = file_name + self.name
        
class partition:
    def __init__(self, init_value, b):
        self.type = init_value # 0 là NTFS, 1 là FAT32
        self.byte = b # START
        self.name = ""
        self.size = 0
        self.id = -1
        self.son = []
    def setName(self, name):
         self.name = name
    def setId(self, id):
        self.id = id

usb_path = "\\\\.\\PhysicalDrive1"  # Địa chỉ vật lí của USB được kí hiệu trong máy là 1, xem trong disk partition

def seek(f,byte):
    while(byte > 1048576):
        f.seek(1048576, 1)
        byte = byte - 1048576
    f.seek(byte, 1)
    return f

def read_mbr(usb_path):
    u = []
    with open(usb_path, 'rb') as f:
        mbr_data = f.read(512)  # Đọc 512 byte đầu tiên (MBR)
        # Đọc thông tin về các phân vùng từ byte 446 đến byte 509 trong MBR
        partition_table = mbr_data[446:510]
        for i in range(0, 4, 1):  # Mỗi phân vùng chiếm 16 byte
            partition_entry = partition_table[i * 16:i * 16 + 16]
            partition_type = partition_entry[4]
            partition_b = int.from_bytes(partition_entry[8:12], byteorder='little') * 512
            if partition_type == 0x00:
                partition_type_int = -1
            elif partition_type == 0x07:
                partition_type_int = 0 # NTFS
            elif partition_type == 0x0B or partition_type == 0x0C:
                partition_type_int = 1 # FAT32
            else:
                partition_type_int = -1
            if (partition_type_int != -1):
                parti = partition(partition_type_int, partition_b)
                u.append(parti)
    return u

usb = read_mbr(usb_path)

def write_partition(usb):
    for i in range(len(usb)):
        print("Partition", i + 1,":", usb[i].type,"---", usb[i].byte)





            