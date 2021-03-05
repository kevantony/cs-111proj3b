import sys
import csv


alloc_inodes = []


class SUPERBLOCK:
    """Creates a class for the information relating to the superblock."""

    def __init__(self, row):
        self.num_of_blocks = int(row[1])
        self.num_of_inodes = int(row[2])
        self.block_size = int(row[3])
        self.inode_size = int(row[4])
        self.blocks_per_group = int(row[5])
        self.inode_per_group = int(row[6])
        self.first_nonres_inode = int(row[7])


class GROUP:
    """Creates a class for the group info."""

    def __init__(self, row):
        self.total_num_blocks_in_group = int(row[2])
        self.total_num_inodes_in_group = int(row[3])
        self.num_free_blocks = int(row[4])
        self.num_free_inodes = int(row[5])
        self.blocknum_of_block_bitmap = int(row[6])
        self.blocknum_of_inode_bitmap = int(row[7])
        self.blocknum_of_first_inode_blocks = int(row[8])


class DIRENT:
    def __init__(self, row):
        self.parent_inode_number = int(row[1])
        self.logical_byte_offset = int(row[2])
        self.inode_number = int(row[3])
        self.entry_length = int(row[4])
        self.name_length = int(row[5])
        self.name = row[6]


class INDIRECT:
    def __init__(self, row):
        self.parent_inode_number = int(row[1])
        self.indirection = int(row[2])
        self.logical_block_offset = int(row[3])
        self.indirect_block_number = int(row[4])
        self.reference_block_number = int(row[5])


class INODE:
    def __init__(self, row, direct_and_indirect):
        self.inode_number = int(row[1])
        self.file_type = row[2]
        self.mode = int(row[3])
        self.owner = int(row[4])
        self.group = int(row[5])
        self.link_count = int(row[6])
        self.last_change = row[7]
        self.modification_time = row[8]
        self.last_access = row[9]
        self.file_size = int(row[10])
        self.block_space = int(row[11])
        self.block_list = direct_and_indirect[0:12]
        self.indirect_list = direct_and_indirect[12:15]


class allocated_block:
    def __init__(self, offset, level, inode_number):
        self.offset = offset
        self.level = level
        self.inode_number = inode_number

# def block_checker(free_blocks, superblock, group):


def inode_errors(inodes, free_inodes, superblock, group):
    for inode in inodes:
        if inode.inode_number != 0:
            inode_val = inode.inode_number
            alloc_inodes.append(inode_val)
            if inode_val in free_inodes:
                alloc_inodes.append(inode_val)
                print("ALLOCATED INODE {inode_num} ON FREELIST".format(
                    inode_num=inode_val))

    for alloc_inode_val in range(superblock.first_nonres_inode, group.total_num_inodes_in_group):
        if alloc_inode_val not in alloc_inodes and alloc_inode_val not in free_inodes:
            print("UNALLOCATED INODE {inode_num} NOT ON FREELIST".format(
                inode_num=alloc_inode_val))


def main():
    inconsistencies_found = False
    free_blocks = []
    free_inodes = []
    inodes = []
    direct_entries = []
    indirect_entries = []
    superblock = None
    group = None
    allocated_blocks = {}

    if(len(sys.argv) != 2):
        print("Error in the input argument.")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                if row[0] == 'SUPERBLOCK':
                    superblock = SUPERBLOCK(row)
                    # print("supblock")
                elif row[0] == 'GROUP':
                    group = GROUP(row)
                    # print("group")
                elif row[0] == 'BFREE':
                    free_blocks.append(int(row[1]))
                    # print("freeblocks")
                elif row[0] == 'IFREE':
                    free_inodes.append(int(row[1]))  # IRFREE action
                elif row[0] == 'INODE':
                    direct_and_indirect = []
                    for i in range(12, 27):
                        direct_and_indirect.append(int(row[i]))
                    inode = INODE(row, direct_and_indirect)
                    inodes.append(inode)
                    # print("inodes")
                elif row[0] == 'DIRENT':
                    dirent = DIRENT(row)  # DIRENT action
                    direct_entries.append(dirent)
                    # print("dirents")
                elif row[0] == 'INDIRECT':
                    indirect_entry = INDIRECT(row)  # INDIRECT action
                    indirect_entries.append(indirect_entry)
                    # print("indirectentrs")
    except:
        print("Unable to read csv.")
        sys.exit(1)  # might need to do some other stuff instead

    inode_errors(inodes, free_inodes, superblock, group)
    # direct_entries_errors(inodes, direct_entries, superblock)

    for inode in inodes:
        # print(inode.indirect_list)
        # if inode.file_type == 's':
        #   continue
        # print(inode.block_list)
        # print(superblock.blocks_per_group)
        for count, data_block in enumerate(inode.block_list):
            # print(count)
            if data_block != 0:
                if data_block < 0 or data_block >= superblock.num_of_blocks:
                    print("INVALID BLOCK " + str(data_block) + " IN INODE " +
                          str(inode.inode_number) + " AT OFFSET " + str(count))
                    inconsistencies_found = True
                if data_block < (group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size):
                    print("RESERVED BLOCK " + str(data_block) + " IN INODE " +
                          str(inode.inode_number) + " AT OFFSET " + str(count))
                    inconsistencies_found = True
                if data_block not in allocated_blocks:
                    allocated_blocks[data_block] = []
                    allocated_blocks[data_block].append(
                        allocated_block(count, 0, inode.inode_number))
                else:
                    allocated_blocks[data_block].append(
                        allocated_block(count, 0, inode.inode_number))

        data_block = inode.indirect_list[0]
        if data_block != 0:
            if data_block < 0 or data_block >= superblock.num_of_blocks:
                print("INVALID INDIRECT BLOCK " + str(data_block) +
                      " IN INODE " + str(inode.inode_number) + " AT OFFSET 12")
                inconsistencies_found = True
            if data_block < (group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size):
                print("RESERVED INDIRECT BLOCK " + str(data_block) +
                      " IN INODE " + str(inode.inode_number) + " AT OFFSET 12")
                inconsistencies_found = True
            if data_block not in allocated_blocks:
                allocated_blocks[data_block] = [allocated_block(
                    12, 1, inode.inode_number)]
            else:
                block = allocated_block(12, 1, inode.inode_number)
                allocated_blocks[data_block].append(block)

        data_block = inode.indirect_list[1]
        if data_block != 0:
            if data_block < 0 or data_block >= superblock.num_of_blocks:
                print("INVALID DOUBLE INDIRECT BLOCK " + str(data_block) +
                      " IN INODE " + str(inode.inode_number) + " AT OFFSET 268")
                inconsistencies_found = True
            if data_block < (group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size):
                print("RESERVED DOUBLE INDIRECT BLOCK " + str(data_block) +
                      " IN INODE " + str(inode.inode_number) + " AT OFFSET 268")
                inconsistencies_found = True
            if data_block not in allocated_blocks:
                allocated_blocks[data_block] = [allocated_block(
                    268, 2, inode.inode_number)]
            else:
                block = allocated_block(268, 2, inode.inode_number)
                allocated_blocks[data_block].append(block)

        data_block = inode.indirect_list[2]
        if data_block != 0:
            if data_block < 0 or data_block >= superblock.num_of_blocks:
                print("INVALID TRIPLE INDIRECT BLOCK " + str(data_block) +
                      " IN INODE " + str(inode.inode_number) + " AT OFFSET 65804")
                inconsistencies_found = True
            if data_block < (group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size):
                print("RESERVED TRIPLE INDIRECT BLOCK " + str(data_block) +
                      " IN INODE " + str(inode.inode_number) + " AT OFFSET 65804")
                inconsistencies_found = True
            if data_block not in allocated_blocks:
                allocated_blocks[data_block] = [allocated_block(
                    65804, 3, inode.inode_number)]
            else:
                block = allocated_block(65804, 3, inode.inode_number)
                allocated_blocks[data_block].append(block)

    for indirect in indirect_entries:
        data_block = indirect.reference_block_number
        if data_block != 0:
            if indirect.indirection == 1:
                level = "INDIRECT "
            if indirect.indirection == 2:
                level = "DOUBLE INDIRECT "
            elif indirect.indirection == 3:
                level = "TRIPLE INDIRECT "
            if data_block < 0 or data_block >= superblock.num_of_blocks:
                print("INVALID " + level + "BLOCK " + str(data_block) + " IN INODE " +
                      str(inode.inode_number) + " AT OFFSET " + str(indirect.logical_byte_offset))
                inconsistencies_found = True
            if data_block < (group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size):
                print("INVALID " + level + "BLOCK " + str(data_block) + " IN INODE " +
                      str(inode.inode_number) + " AT OFFSET " + str(indirect.logical_byte_offset))
                inconsistencies_found = True
            if data_block not in allocated_blocks:
                allocated_blocks[data_block] = [allocated_block(
                    indirect.logical_block_offset, indirect.indirection, indirect.parent_inode_number)]
            else:
                block = allocated_block(
                    indirect.logical_block_offset, indirect.indirection, indirect.parent_inode_number)
                allocated_blocks[data_block].append(block)

    for data_block in range((group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size), superblock.num_of_blocks):
        if data_block not in allocated_blocks and data_block not in free_blocks:
            print("UNREFERNCED BLOCK " + str(data_block))
            inconsistencies_found = True

    for data_block in range((group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size), superblock.num_of_blocks):
        if data_block in allocated_blocks and data_block in free_blocks:
            print("ALLOCATED BLOCK " + str(data_block) + " ON FREELIST")
            inconsistencies_found = True

    for data_block in range((group.blocknum_of_first_inode_blocks + (group.total_num_inodes_in_group*superblock.inode_size)/superblock.block_size), superblock.num_of_blocks):
        if data_block in allocated_blocks and len(allocated_blocks[data_block]) > 1:
            data = allocated_blocks[data_block]
            # print(len(data))
            for index in range(0, len(data)):
                # print(len(info))
                # print(data[index].level)
                if (data[index].level == 0):
                    print("DUPLICATE BLOCK " + str(data_block) + " IN INODE " +
                          str(data[index].inode_number) + " AT OFFSET " + str(data[index].offset))
                    inconsistencies_found = True
                elif (data[index].level == 1):
                    print("DUPLICATE INDIRECT BLOCK " + str(data_block) + " IN INODE " +
                          str(data[index].inode_number) + " AT OFFSET " + str(data[index].offset))
                    inconsistencies_found = True
                elif (data[index].level == 2):
                    print("DUPLICATE DOUBLE INDIRECT BLOCK " + str(data_block) + " IN INODE " +
                          str(data[index].inode_number) + " AT OFFSET " + str(data[index].offset))
                    inconsistencies_found = True
                else:
                    print("DUPLICATE TRIPLE INDIRECT BLOCK " + str(data_block) + " IN INODE " +
                          str(data[index].inode_number) + " AT OFFSET " + str(data[index].offset))
                    inconsistencies_found = True

    if inconsistencies_found is True:
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
