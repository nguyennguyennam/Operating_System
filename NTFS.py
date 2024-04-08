from MBR import *
import datetime


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
def read_MFT(byte_MFT, parti, byte_entry, sec_per_clus, byte_per_sec):
    with open(usb_path, 'rb') as f:
        f = seek(f, byte_MFT)
        #while (True):
        #if(True):
        for i in range(0,100,1):
            type = -1
            entry = f.read(byte_entry)
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
                    nano_sec = int.from_bytes(attri[start_attri_data:start_attri_data + 8], byteorder='little') #TIME
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
                    f_size = int.from_bytes(attri[48:56], byteorder='little')  # SIZE
                start_attri = start_attri + size
            temp = save_data(type, file_name, attri, None, f_size, None, hid, id, id_parent)
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
        
        read_MFT(byte_MFT, parti, byte_entry, sector_per_cluster, byte_per_sector)
read_NTFS(usb[0])
print(usb[0].name)
print("-----------------------------------")
for i in usb[0].son:
    if (i.hidden == 0):
        print(i.name)
        if (i.type == 0):
            for j in i.son:
                if (j.hidden == 0):
                    print(" 1   ",j.name)
                    if (j.type == 0):
                        for k in j.son:
                            if (k.hidden == 0):
                                print("     2       ",k.name)
