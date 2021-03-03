import sys
import csv

class SuperBlock:
    """Creates a class for the information relating to the superblock."""
    def __init__(self, row):
        self.num_of_blocks = int(row[1])
        self.num_of_inodes = int(row[2])
        self.block_size = int(row[3])
        self.inode_size = int(row[4])
        self.blocks_per_group = int(row[5])
        self.inode_per_group = int(row[6])
        self.first_nonres_inode = int(row[7])

class Group:
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


def main():
    inconsistencies_found = false
    free_blocks = []
    free_inodes = []
    try:
        with open(file) as csvfile:
            for row in csvfile:
                if row[0] == 'SUPERBLOCK':
                    superblock = SUPERBLOCK(row)
                elif row[0] == 'GROUP':
                    gorup = Group(row)
                elif row[0] = 'BFREE':
                    free_blocks.append(int(row[1]))
                elif row[0] = 'IFREE':
                    free_inodes.append(int(row[1])) #IRFREE action
                elif row[0] = 'INODE':
                    #INODE action
                elif row[0] = 'DIRENT':
                    DIRENT(row)#DIRENT action
                elif row[0] = 'INDIRECT':
                    #INDIRECT action
                else:
                    #Invalid option

                
    except:
        exit(1) #might need to do some other stuff instead




    if inconsistencies_found:
        sys.exit(2)

    sys.exit(0)

if __name__ == '__main__':
    main()



