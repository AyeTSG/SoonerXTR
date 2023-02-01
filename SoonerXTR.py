# SoonerXTR: Extracts a HTC EXCA300 system.img
# Author: AyeTSG

import os

cur_node_id = -1

def roundr(n, step):
    return ((n - 1) // step + 1) * step

# these need to be done manually at the moment, but can easily be done
# using the data that gets output to console
dir_ident_list = {
    "0": "/",
    "1": "/bin/",
    "49": "/usr/",
    "50": "/usr/share/",
    "51": "/usr/share/bsk/",
    "54": "/usr/share/zoneinfo/",
    "57": "/usr/keylayout/",
    "62": "/usr/cert/",
    "64": "/usr/keychars/",
    "69": "/fonts/",
    "78": "/media/",
    "79": "/media/audio/",
    "80": "/media/audio/ringtones/",
    "89": "/sounds/",
    "97": "/lib/",
    "98": "/lib/modules/",
    "152": "/app/",
    "197": "/javalib/"
}

def read_entry(img):
    global cur_node_id

    # read file type
    file_type = img.read(4)

    #print(file_type)

    # if it's a file...
    if (file_type == b'\x01\x00\x00\x00'):
        # -- GET DIR IDENTIFIER
        dir_ident = img.read(4)
        img.read(2)

        print("PARENT NODE ID: " +
              str(int.from_bytes(dir_ident[:1], "little")))

        # -- FIND DIR

        # -- GET FILE NAME
        file_name = img.read(0xFF).decode('UTF-8')
        print("FILE: " + file_name.rstrip('\x00'))

        img.read(0x1b)

        # -- GET FILE SIZE
        file_size_low = img.read(0x04)
        #print(file_size_low)

        img.read(0x6d8)

        # -- READ THE BINARY!
        path = "mtd5_system" + dir_ident_list[str(int.from_bytes(dir_ident[:1], "little"))]

        print(path)

        if (os.path.exists(path) == False):
            os.makedirs(path)

        f = open(path + file_name.rstrip('\x00'), "wb")

        f.write(img.read(int.from_bytes(file_size_low, "little")))

        f.close()

        ## == GET NEXT ENTRY
        img.seek(roundr(img.tell(), 0x800))

        #print(hex(img.tell()))
        cur_node_id += 1

        print("NODE: " + str(cur_node_id))
        print(os.linesep)

    # if it's a dir...
    if (file_type == b'\x03\x00\x00\x00'):
        # -- GET DIR IDENTIFIER
        dir_ident = img.read(4)
        img.read(2)

        proper_node_id = int.from_bytes(dir_ident[:1], "little")

        if (proper_node_id == 1):
            proper_node_id = 0

        print("PARENT NODE ID: " +
              str(proper_node_id))
        #f = open("mtd5_system/ident_" + str(int.from_bytes(dir_ident, "little")), "wb")
        #f.close()

        # -- GET DIR NAME
        dir_name = img.read(0xff).decode('UTF-8')

        print("DIR: " + dir_name.rstrip('\x00'))

        ## == GET NEXT ENTRY
        img.seek(roundr(img.tell(), 0x800))

        #print(hex(img.tell()))
        cur_node_id += 1

        print("NODE: " + str(cur_node_id))
        print(os.linesep)


with open("mtd5_system.img", mode="rb") as img:

    while (True):
        read_entry(img)