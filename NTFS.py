from MBR import *
import datetime

def convert_nanoseconds_to_time(nanoseconds):
    # Tính số giây, phút, giờ, vv từ số nano giây
    total_seconds = nanoseconds / 1e9  # Chuyển đổi nano giây thành giây
    total_minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(total_minutes, 60)
    days, hours = divmod(hours, 24)

    # Tạo một đối tượng datetime từ số giây tính được
    start_date = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    result_date = start_date + delta

    return result_date

def complement(x):
    temp = x ^ 0b11111111
    temp = temp + 1
    return temp
def add(parti, t):
    if (parti.id == t.parent):
        parti.son.append(t)
        return
    for i in parti.son:
        add(i, t)
def read_MFT(byte_MFT, parti, byte_entry, sec_per_clus, byte_per_sec, byte_before_parti):
    with open(usb_path, 'rb') as f:
        f = seek(f, byte_MFT)

        for i in range(0,100,1):
            type = -1
            entry = f.read(byte_entry)
            data = ""
            f_size = 0
            start = 0
            id = 0
            hid = 1
            if (entry[0:4] != b'FILE'):
                continue
            if (entry[22] == 0x00 or entry[22] == 0x02):
                continue
            start_attri = int.from_bytes(entry[20:22], byteorder='little')
            id = int.from_bytes(entry[44:48], byteorder='little') # Id save_data
            while(True):
                size = int.from_bytes(entry[start_attri + 4:start_attri+ 8], byteorder='little')
                if (size == 0):
                    break
                attri = entry[start_attri:start_attri + size]
                
                attri_type = int.from_bytes(attri[0:4], byteorder='little')
                attri_type = attri_type // 16
                if (attri_type == 1):
                    start_attri_data = int.from_bytes(attri[20:22], byteorder='little')
                    nano_sec = int.from_bytes(attri[start_attri_data:start_attri_data + 8], byteorder='little') *100  #TIME
                    save_nano_sec = convert_nanoseconds_to_time(nano_sec) 
                    save_date = DATE(save_nano_sec.day, save_nano_sec.month, save_nano_sec.year, save_nano_sec.hour, save_nano_sec.minute, save_nano_sec.second)
                if (attri_type == 3):
                    start_attri_data = int.from_bytes(attri[20:22], byteorder='little')
                    id_parent = int.from_bytes(attri[start_attri_data:start_attri_data + 6], byteorder='little')    # ID PARENT
                    if (parti.id == -1):
                        parti.setId(id_parent)
                    
                    attr = bin(int.from_bytes(attri[start_attri_data + 56:start_attri_data + 60], byteorder='little'))[2:].zfill(32)
                    attr = attr[::-1]
                    if (attr[1] == '1'):
                        hid = 1 # HIDDEN
                    else:
                        hid = 0
                    if (attr[5] == '1'):
                        type = 1    # FILE
                    if (attr[28] == '1'):
                        type = 0    # FOLDER
                    len = int.from_bytes(attri[start_attri_data + 64:start_attri_data + 65], byteorder='little')
                    space = int.from_bytes(attri[start_attri_data + 65:start_attri_data + 66], byteorder='little')
                    if (space > 1):
                        space = space - 1
                    else:
                        space = 2
                    file_name_length = len * space
                    file_name = attri[start_attri_data + 66:start_attri_data + 66 + file_name_length].decode('utf-16').strip()
                if (attri_type == 6):
                    start_attri_data = int.from_bytes(attri[20:22], byteorder='little')
                    len = int.from_bytes(attri[16:20], byteorder='little')

                    name = attri[start_attri_data:start_attri_data + len].decode('utf-16').strip() # NAME OF VOLUME

                    parti.setName(name)
                if (attri_type == 8):
                    if (attr[2] != '1'):
                        if int.from_bytes(attri[8:9], byteorder='little') == 0: # non-resident = 0
                            start_attri_data = int.from_bytes(attri[20:22], byteorder='little')
                            f_size = int.from_bytes(attri[16:20], byteorder='little')  # SIZE
                            print("***", f_size, "----", file_name)
                            if hid == 0:
                                #data = attri[start_attri_data:start_attri_data+ f_size].decode('utf-8')
                                try:
                                    data = attri[start_attri_data:start_attri_data+ f_size].decode('utf-8', errors='strict')
                                    print("***")
                                    print(data)
                                except UnicodeDecodeError as e:
                                    data = None

                        else:
                            start_attri_data = int.from_bytes(attri[20:22], byteorder='little')
                            f_size = int.from_bytes(attri[48:56], byteorder='little')  # SIZE
                            start = int.from_bytes(attri[74:77], byteorder='little')
                            print(file_name,"---", start * sec_per_clus * byte_per_sec + byte_before_parti)
                            with open(usb_path, 'rb') as file:
                                file = seek(file, start * sec_per_clus * byte_per_sec + byte_before_parti)
                                temp = file.read(3)
                                try:
                                    data = file.read(f_size).decode('utf-8')
                                except UnicodeDecodeError as e:
                                    print(file_name)
                                    print(e)
                                    data = None
                            #     print(data)
                start_attri = start_attri + size
            temp = save_data(type, file_name, attri, save_date, f_size, None, hid, id, id_parent, data)
            add(parti, temp)
            
def read_NTFS(parti):
    with open(usb_path, 'rb') as f:
        f.seek(parti.byte)
        vbr = f.read(512)
        byte_per_sector = int.from_bytes(vbr[11:13], byteorder='little')
        sector_per_cluster = int.from_bytes(vbr[13:14], byteorder='little')
        cluster_MFT = int.from_bytes(vbr[48:56], byteorder='little')
        temp_byte_entry = int.from_bytes(vbr[64:65], byteorder='little')
        byte_entry = 2 ** complement(temp_byte_entry)
        byte_MFT = parti.byte + cluster_MFT * sector_per_cluster * byte_per_sector
        
        read_MFT(byte_MFT, parti, byte_entry, sector_per_cluster, byte_per_sector, parti.byte)
       


