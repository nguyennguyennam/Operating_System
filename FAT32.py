from MBR import *

def read_entry(byte, parti, sec_per_clus, byte_per_sec):
    with open(usb_path, 'rb') as f:
        f = seek(f,byte)
        while (True):
            entry = f.read(32)
            if (entry[0] == 0x00):
                break
            elif (entry[0] == 0xE5):
                continue
            elif (entry[11] == 0x0F):

                if parti.son:
                    stt = int.from_bytes(entry[0:1], byteorder='little')
                    temp = entry[1:11] + entry[14:26] + entry[28:32]
                    for i in range(len(temp)):
                        if (i < len(temp) and temp[i] == 0xFF):
                            temp = temp[:i]
                    name = temp.decode('utf-16').strip()
                    
                    if parti.son and parti.son[-1].type != -1:
                        t = save_data(-1, name, None, None, None, None, None, None)
                        parti.son.append(t)
                    else:
                        parti.son[-1].setName(name)

            else: 
                if parti.son and parti.son[-1].type != -1:
                    file_name = entry[0:8].decode('utf-8').strip() # NAME
                else:
                    file_name = ""
                exten = entry[8:11].decode('utf-8').strip() # EXTEN
                # ATTRIBUTE
                attr = bin(int.from_bytes(entry[11:12], byteorder='little'))[2:].zfill(8) # Vị trí bị ngược lại bắt đầu từ archive, cắt bỏ tiền tố
                total_size = int.from_bytes(entry[28:32], byteorder='little')
                if (attr[4] == '1'):    # NAME VOLUME
                    file_name = entry[0:11].decode('utf-8').strip()
                    parti.setName(file_name)
                else:
                    hour = bin(int.from_bytes(entry[13:16], byteorder='little'))[2:].zfill(24)
                    da = bin(int.from_bytes(entry[16:18], byteorder='little'))[2:].zfill(16)
                    high_clus = int.from_bytes(entry[20:22], byteorder='little')
                    low_clus = int.from_bytes(entry[26:28], byteorder='little')
                    clus = high_clus * 16 ** 4 + low_clus # START
                    if (attr[3] == '1'):
                        type = 0 #FOLDER
                    elif (attr[2] == '1'):    
                        type = 1 # FILE
                    else:
                        type = -1
                    if (attr[6] == '1'):
                        hid = 1             # HIDDEN
                    else:
                        hid = 0
                    #if entry[0] == 0x2E:
                        #hid = 1
                    h = int(hour[0:5],2)
                    m = int(hour[5:11],2)
                    s = int(hour[11:17],2)
                    mili = int(hour[17:24],2)

                    year = int(da[0:7],2)
                    mon = int(da[7:11],2)
                    day = int(da[11:16],2)

                    date = DATE(day, mon, year + 1980, h, m, s) #DATE
                    if parti.son and parti.son[-1].type == -1:
                        parti.son[-1].setInfor(type, attr, date, total_size, clus, hid, 0, None)
                    else:
                        temp = save_data(type, file_name, attr, date, total_size, clus, hid, 0)
                        parti.son.append(temp)

                    
def read_FAT(sec_before_FAT, byte_per_sec, sec_FAT):
    byte = sec_before_FAT * byte_per_sec
    FAT = []
    with open(usb_path, 'rb') as file:
        file = seek(file, byte)
        temp = file.read(sec_FAT * byte_per_sec)
        for i in range(sec_FAT * byte_per_sec // 4):
            t = int.from_bytes(temp[i * 4:i * 4 + 4], byteorder='little')
            if (t == 268435455):
                t = -1 # END
            if (t == 268435447):
                t = -2 # BAD
            FAT.append(t)
    return FAT

def read_RDET(byte_RDET, parti, sec_per_clus, byte_per_sec, FAT):
    read_entry(byte_RDET, parti, sec_per_clus, byte_per_sec)

def read_folder(save_data, FAT, byte_before_parti, sec_before_FAT, num_FAT, sec_FAT, sec_per_clus, byte_per_sec):
    byte = byte_before_parti + (sec_before_FAT + num_FAT * sec_FAT +  (save_data.start - 2) * sec_per_clus) * byte_per_sec
    temp = save_data.start
    with open(usb_path, 'rb') as f:
        while(True):
            f = seek(f, byte)
            read_entry(byte, save_data, sec_per_clus, byte_per_sec)
            if ((FAT[temp] != -1) and (FAT[temp] != -2) and (FAT[temp] != 0)):
                byte = byte_before_parti + (sec_before_FAT + num_FAT * sec_FAT +  (FAT[temp] - 2) * sec_per_clus) * byte_per_sec
                temp = FAT[temp]
            else:
                break
        for i in range(2,len(save_data.son),1):
            if (save_data.son[i].type == 0):
                read_folder(save_data.son[i], FAT, byte_before_parti, sec_before_FAT, num_FAT, sec_FAT, sec_per_clus, byte_per_sec)

            
def read_save_data(save_data, FAT, byte_before_parti, sec_before_FAT, num_FAT, sec_FAT, sec_per_clus, byte_per_sec):
    if (save_data.type == 0):
        read_folder(save_data, FAT,  byte_before_parti, sec_before_FAT, num_FAT, sec_FAT, sec_per_clus, byte_per_sec)
                                    
def read_FAT32(parti):
    with open(usb_path, 'rb') as f:
        # Đọc BOOT SECTOR
        f.seek(parti.byte)
        boot_sector = f.read(512)
        byte_per_sector = int.from_bytes(boot_sector[11:13], byteorder='little')
        sector_per_cluster = int.from_bytes(boot_sector[13:14], byteorder='little')
        sector_before_FAT = int.from_bytes(boot_sector[14:16], byteorder='little')
        num_FAT = int.from_bytes(boot_sector[16:17], byteorder='little')
        sec_FAT = int.from_bytes(boot_sector[36:40], byteorder='little')
        cluster_RDET = int.from_bytes(boot_sector[44:48], byteorder='little')
        byte_RDET = parti.byte + (sector_before_FAT + num_FAT * sec_FAT +  (cluster_RDET - 2) * sector_per_cluster) * byte_per_sector

        FAT = read_FAT((parti.byte // byte_per_sector) + sector_before_FAT, byte_per_sector, sec_FAT)
        read_RDET(byte_RDET, parti, sector_per_cluster, byte_per_sector, FAT)
        for i in parti.son:
            read_save_data(i, FAT, parti.byte, sector_before_FAT, num_FAT, sec_FAT, sector_per_cluster, byte_per_sector)


    


