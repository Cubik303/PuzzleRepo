# Rules:
# Hitori is played on a grid of squares.
# At the beginning, each cell contains a number.
# The goal is to paint out some cells so that there are no duplicate numbers in any row or column,
#   similar to the solved state of a Sudoku puzzle (except with black squares added to the grid).

# Orthogonal connections are important as well;
#   painted-out (black) cells cannot be connected orthogonally,
#   and the other cells must be connected orthogonally in a single group
#   (i.e. no two black squares can be adjacent to each other,
#   and all un-painted squares must be connected, horizontally or vertically, to create a single shape).

from copy import deepcopy as dc

GRID = []

CELL_UNKNOWN = 0
CELL_PAINTED = 1
CELL_WHITE = 2

#Read in relevant puzzle information
def generatePuzzle():
    inputfile = open("Hitori/InputFile.txt","r")

    for line in inputfile:
        splitline = line.strip().split(",")
        GRID.append(splitline)
    inputfile.close()

def solvePuzzle(grid_status):
    progress_made = True
    while(progress_made):
        progress_made = False
        
        #If two spaces with the same numerical value are 2 spaces apart horizontally or vertically
        # then the space in the middle must be un-painted
        for row in range(1,len(GRID)-1):
            for col in range(0,len(GRID[row])):
                if(GRID[row-1][col] == GRID[row+1][col] and grid_status[row][col] == CELL_UNKNOWN):
                    grid_status[row][col] = CELL_WHITE
                    progress_made = True

        for row in range(0,len(GRID)):
            for col in range(1,len(GRID[row])-1):
                if(GRID[row][col-1] == GRID[row][col+1] and grid_status[row][col] == CELL_UNKNOWN):
                    grid_status[row][col] = CELL_WHITE
                    progress_made = True

        for row in range(0,len(GRID)):
            for col in range(0,len(GRID[row])):
                if(grid_status[row][col] == CELL_PAINTED):
                    #If any cells have been painted, all orthogonally adjacent cells must be un-painted
                    if(row > 0):
                        if(grid_status[row-1][col] == CELL_UNKNOWN):
                            grid_status[row-1][col] = CELL_WHITE
                            progress_made = True
                        elif(grid_status[row-1][col] == CELL_PAINTED):
                            ###print("Error: Adjacent Cells Painted")
                            return
                    if(col > 0):
                        if(grid_status[row][col-1] == CELL_UNKNOWN):
                            grid_status[row][col-1] = CELL_WHITE
                            progress_made = True
                        if(grid_status[row][col-1] == CELL_PAINTED):
                            ###print("Error: Adjacent Cells Painted")
                            return
                    if(row < len(GRID)-1):
                        if(grid_status[row+1][col] == CELL_UNKNOWN):
                            grid_status[row+1][col] = CELL_WHITE
                            progress_made = True
                        if(grid_status[row+1][col] == CELL_PAINTED):
                            ###print("Error: Adjacent Cells Painted")
                            return
                    if(col < len(GRID[row])-1):
                        if(grid_status[row][col+1] == CELL_UNKNOWN):
                            grid_status[row][col+1] = CELL_WHITE
                            progress_made = True
                        if(grid_status[row][col+1] == CELL_PAINTED):
                            ###print("Error: Adjacent Cells Painted")
                            return

                elif(grid_status[row][col] == CELL_WHITE):
                    #If any cells are marked un-painted, all cells of the same value in the same row or same column must be painted
                    for xrow in range(0,len(GRID)):
                        if(GRID[xrow][col] == GRID[row][col]):
                            if(grid_status[xrow][col] == CELL_UNKNOWN):
                                grid_status[xrow][col] = CELL_PAINTED
                                progress_made = True
                            elif(grid_status[xrow][col] == CELL_WHITE and xrow != row):
                                ###print("Error: Two White Cells with same value in same column")
                                return
                    for xcol in range(0,len(GRID[row])):
                        if(GRID[row][xcol] == GRID[row][col]):
                            if(grid_status[row][xcol] == CELL_UNKNOWN):
                                grid_status[row][xcol] = CELL_PAINTED
                                progress_made = True
                            elif(grid_status[row][xcol] == CELL_WHITE and xcol != col):
                                ###print("Error: Two White Cells with same value in same row")
                                return
        
        #Check if any islands of un-painted cells have only one available outlet
        island_checker = dc(grid_status)
        island_value = -1
        only_outlet_cells = []
        closed_off_islands = False
        for row in range(0,len(island_checker)):
            for col in range(0,len(island_checker[row])):
                if(island_checker[row][col] == CELL_WHITE):
                    white_cells = [[row,col]]
                    unknown_cells = []
                    while(len(white_cells) > 0):
                        xrow = white_cells[0][0]
                        xcol = white_cells[0][1]
                        island_checker[xrow][xcol] = island_value

                        #Check each neighbor
                        if(xrow > 0):
                            if(island_checker[xrow-1][xcol] == CELL_UNKNOWN):
                                unknown_cells.append([xrow-1,xcol])
                            elif(island_checker[xrow-1][xcol] == CELL_WHITE):
                                white_cells.append([xrow-1,xcol])
                        if(xcol > 0):
                            if(island_checker[xrow][xcol-1] == CELL_UNKNOWN):
                                unknown_cells.append([xrow,xcol-1])
                            elif(island_checker[xrow][xcol-1] == CELL_WHITE):
                                white_cells.append([xrow,xcol-1])
                        if(xrow < len(GRID)-1):
                            if(island_checker[xrow+1][xcol] == CELL_UNKNOWN):
                                unknown_cells.append([xrow+1,xcol])
                            elif(island_checker[xrow+1][xcol] == CELL_WHITE):
                                white_cells.append([xrow+1,xcol])
                        if(xcol < len(GRID[row])-1):
                            if(island_checker[xrow][xcol+1] == CELL_UNKNOWN):
                                unknown_cells.append([xrow,xcol+1])
                            elif(island_checker[xrow][xcol+1] == CELL_WHITE):
                                white_cells.append([xrow,xcol+1])

                        white_cells.pop(0)

                    if(len(unknown_cells) == 0):
                        closed_off_islands = True
                    if(len(unknown_cells) == 1 and unknown_cells[0] not in only_outlet_cells):
                        only_outlet_cells.append(unknown_cells[0])

                    #Create new island value to know how many islands are observed currently
                    island_value -=1

        for cell in only_outlet_cells:
            #These are cells that are the only possible outlets for an island of white cells that hasn't covered the whole grid
            grid_status[cell[0]][cell[1]] = CELL_WHITE
            progress_made = True

        if(closed_off_islands):
            if(island_value < -2):
                #There are more than 2 islands of white cells, and at least one was found to have no outlets
                ###print("Error, island observed that doesn't cover the entire grid")
                return
            
        #Check all cells have been resolved
        all_cells_resolved = True
        for row in range(0,len(GRID)):
            for col in range(0,len(GRID[row])):
                if(grid_status[row][col] == CELL_UNKNOWN):
                    all_cells_resolved = False
                    break
        if(all_cells_resolved):
            print("*"*(len(GRID[0])*2+1))
            for row in range(0,len(GRID)):
                temp_string_paint = ""
                temp_string_unpaint = ""
                for col in range(0,len(GRID[row])):
                    if(grid_status[row][col] == CELL_PAINTED):
                        temp_string_paint = temp_string_paint + "▓"
                        temp_string_unpaint = temp_string_unpaint + str(GRID[row][col])
                    elif(grid_status[row][col] == CELL_WHITE):
                        temp_string_paint = temp_string_paint + str(GRID[row][col])
                        temp_string_unpaint = temp_string_unpaint + "▓"
                print(temp_string_paint,temp_string_unpaint)
            print("*"*(len(GRID[0])*2+1))
            return
            
    # All logical progress has been found with the current implementation
    # If the loop has been exited at this point, there are still unresolved cells
    # Pick the first unresolved space, and recurse with both it being Painted and left White
    for row in range(0,len(GRID)):
        for col in range(0,len(GRID[row])):
            if(grid_status[row][col] == CELL_UNKNOWN):
                grid_status_copy = dc(grid_status)
                grid_status_copy[row][col] = CELL_PAINTED
                solvePuzzle(grid_status_copy)

                grid_status_copy = dc(grid_status)
                grid_status_copy[row][col] = CELL_WHITE
                solvePuzzle(grid_status_copy)
                return

def main():
    print("Generating puzzle from input file...",end="")
    generatePuzzle()
    print("Done.")

    grid_status = []
    for row in range(0,len(GRID)):
        grid_status.append([CELL_UNKNOWN]*len(GRID[row]))

    print("Finding solutions...")
    solvePuzzle(grid_status)

if __name__ == "__main__":
    main()