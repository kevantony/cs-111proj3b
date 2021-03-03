import sys
import csv




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



