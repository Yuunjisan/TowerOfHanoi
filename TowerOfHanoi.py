import ccm  # CCMSUITE framework
from ccm.model import Model
from ccm.production import ProductionSystem
from ccm.lib.actr.dm import Memory
from ccm.lib.actr.buffer import Buffer

class TowerOfHanoi(Model, object):
    def __init__(self):
        super(TowerOfHanoi, self).__init__()
        self.goal_buffer = Buffer()  #buffer for goals
        self.retrieval_buffer = Buffer()  #buffer for memory

        #declarative memory (connect to the retrieval buffer)
        self.dm = Memory(buffer=self.retrieval_buffer)

        #initialize rules and knowledge
        self.initialize_knowledge()

        self.pegs = {
            'left': [3, 2, 1],  'middle': [],'right': []}
        self.move_count = 0

    def initialize_knowledge(self):
        #add procedural rules for moving disks
        self.dm.add('rule from:left to:middle')
        self.dm.add('rule from:left to:right')
        self.dm.add('rule from:middle to:left')
        self.dm.add('rule from:middle to:right')
        self.dm.add('rule from:right to:left')
        self.dm.add('rule from:right to:middle')

        # Add declarative facts about disk sizes
        self.dm.add('disk size:1 smaller_than:2')
        self.dm.add('disk size:2 smaller_than:3')
        self.dm.add('disk size:3 smaller_than:None')

    def move_disk(self, disk, source, target):
        """Perform a move by updating the pegs and visualizing the state."""
        #increment move count
        self.move_count += 1

        #move the disk from source peg to target peg
        self.pegs[source].remove(disk)
        self.pegs[target].append(disk)

        #sort the target peg to maintain visualization order
        self.pegs[target].sort(reverse=True)

        #print the move and the current state of the pegs
        print("Move {}: Disk {} from {} to {}".format(self.move_count, disk, source, target))
        self.display_pegs()

    def display_pegs(self):
        """Display the current state of the pegs in a visual format. Uses A, B, C for peg names instead of left, middle, right"""
        print("\nCurrent Peg State:")

        #find maximum height of any peg
        max_height = max(len(disks) for disks in self.pegs.values())

        #print pegs from top to bottom
        for height in range(max_height - 1, -1, -1):
            line = []
            # Map left->A, middle->B, right->C
            for peg in ['left', 'middle', 'right']:
                if height < len(self.pegs[peg]):
                    disk = self.pegs[peg][height]
                    disk_str = "[{}]".format(disk)
                    line.append(disk_str.center(6))
                else:
                    line.append("|".center(6))
            print("".join(line))

        #print base and labels with A, B, C
        print("-" * 18)
        print("  A     B     C  ".center(18))
        print("=" * 30)

    def solve(self, n_disks, source, auxiliary, target):
        """Solve the Tower of Hanoi problem recursively by setting appropriate goals"""
        if n_disks == 1:
            #move the smallest disk
            self.move_disk(1, source, target)
            return

        #recursive solution:
        self.solve(n_disks - 1, source, target, auxiliary)
        self.move_disk(n_disks, source, target)
        self.solve(n_disks - 1, auxiliary, source, target)

#run the model
if __name__ == "__main__":
    model = TowerOfHanoi()


    print("Solving Tower of Hanoi for 3 disks:")
    model.display_pegs()
    model.solve(3, 'left', 'middle', 'right')

    print("\nTotal Moves: {}".format(model.move_count))

    print("\nContents of DM:")
    for chunk in model.dm.dm:
        print(chunk)