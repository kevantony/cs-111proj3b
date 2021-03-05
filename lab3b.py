import sys
import csv


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
        self.indirextion = int(row[2])
        self.logical_block_offset = int(row[3])
        self.indierct_block_number = int(row[4])
        self.reference_block_number = int(row[5])


class INODE:
    def __init__(self, row):
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

def inode_errors(inodes, free_inodes, superblock, group):
    alloc_inodes = []

    for inode in inodes:
        if inode.inode_number != 0:
            inode_val = inode.inode_number
            alloc_inodes.append(inode_val)
            if inode_val in free_inodes:
                alloc_inodes.append(inode_val)
                print("ALLOCATED INODE {inode_num} ON FREELIST".format(inode_num = inode_val))
        
            
    for alloc_inode_val in range(superblock.first_nonres_inode, group.total_num_inodes_in_group):
        if alloc_inode_val not in alloc_inodes and alloc_inode_val not in free_inodes:
            print("UNALLOCATED INODE {inode_num} NOT ON FREELIST".format(inode_num = alloc_inode_val))



    


def main():
    
    inconsistencies_found = False
    free_blocks = []
    free_inodes = []
    inodes = []
    direct_entries = []
    indirect_entries = []

    if(len(sys.argv) != 2):
        print("Error in the input argument.")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                if row[0] == 'SUPERBLOCK':
                    superblock = SUPERBLOCK(row)
                    #print("supblock")
                elif row[0] == 'GROUP':
                    group = GROUP(row)
                    #print("group")
                elif row[0] == 'BFREE':
                    free_blocks.append(int(row[1]))
                    #print("freeblocks")
                elif row[0] == 'IFREE':
                    free_inodes.append(int(row[1]))  # IRFREE action
                    #print("freeinodes")
                elif row[0] == 'INODE':
                    inode = INODE(row)
                    inodes.append(inode)
                    #print("inodes")
                elif row[0] == 'DIRENT':
                    dirent = DIRENT(row)  # DIRENT action
                    direct_entries.append(dirent)
                    #print("dirents")
                elif row[0] == 'INDIRECT':
                    indirect_entry = INDIRECT(row)  # INDIRECT action
                    indirect_entries.append(indirect_entry)
                    #print("indirectentrs")
    except:
        print("Unable to read csv.")
        sys.exit(1)  # might need to do some other stuff instead

    if group.num_free_blocks != (group.total_num_blocks_in_group - len(free_blocks)):
        print("")

    

    inode_errors(inodes, free_inodes, superblock, group)

    if inconsistencies_found:
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
