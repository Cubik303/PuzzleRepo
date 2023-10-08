from copy import deepcopy as dc
from itertools import permutations as perm
GRID_LAYOUT = []
ROW_CLUES = []
COL_CLUES = []

possible_cell_values = []
possible_clue_row_answers = []
possible_clue_col_answers = []

CELL_OPEN = 0
CELL_WALL = 1

#Read in relevant puzzle information
def generatePuzzle():
    inputfile = open("Kakuro/InputFile.txt","r")

    for line in inputfile:
        stripline = line.strip().split(",")
        #print(stripline)
        temp_row = []
        for col in range(0,len(stripline)):
            if("\\" in stripline[col]):
                temp_row.append(CELL_WALL)

                digit_sum_info = stripline[col].split("\\")
                if(digit_sum_info[0] != ""):
                    #Column clue information
                    COL_CLUES.append([col,len(GRID_LAYOUT)+1,-1,int(digit_sum_info[0])])
                if(digit_sum_info[1] != ""):
                    #Row clue information
                    ROW_CLUES.append([len(GRID_LAYOUT),col+1,-1,int(digit_sum_info[1])])
            else:
                temp_row.append(CELL_OPEN)
        GRID_LAYOUT.append(temp_row)
    inputfile.close()

    #Determine the end cell for each row and column clue
    for i in ROW_CLUES:
        col = i[1]
        while(col < len(GRID_LAYOUT[i[0]]) and GRID_LAYOUT[i[0]][col] == CELL_OPEN):
            i[2] = col
            col += 1

    for i in COL_CLUES:
        row = i[1]
        while(row < len(GRID_LAYOUT) and GRID_LAYOUT[row][i[0]] == CELL_OPEN):
            i[2] = row
            row += 1

def preSolveWork():
    #Verify puzzle is an actual grid:
    for row in range(1,len(GRID_LAYOUT)):
        if(len(GRID_LAYOUT[row]) != len(GRID_LAYOUT[0])):
            print("Error: Row {0} of grid doesn't match the length of 1st row".format(row))
            exit()

    #Verify Row Clues
    for row_clue in ROW_CLUES:
        for col in range(row_clue[1],row_clue[2]+1):
            #Verify entire range is open
            if(GRID_LAYOUT[row_clue[0]][col] == CELL_WALL):
                print("Error: Cell at ({0},{1}) is a wall but should be open".format(row_clue[0],col))
                exit()

        #Verify left edge is off the grid or a wall
        if(row_clue[1] > 0 and GRID_LAYOUT[row_clue[0]][row_clue[1]-1] == CELL_OPEN):
            print("Error: Row clue {0}, says Cell at ({1},{2}) should be a wall".format(row_clue,row_clue[0],row_clue[1]-1))
            exit()

        #Verify right edge is off the grid or a wall
        if(row_clue[2] < len(GRID_LAYOUT[row_clue[0]])-1 and GRID_LAYOUT[row_clue[0]][row_clue[2]+1] == CELL_OPEN):
            print("Error: Row clue {0}, says Cell at ({1},{2}) should be a wall".format(row_clue,row_clue[0],row_clue[2]+1))
            exit()

    #Verify Col Clues
    for col_clue in COL_CLUES:
        for row in range(col_clue[1],col_clue[2]+1):
            #Verify entire range is open
            if(GRID_LAYOUT[row][col_clue[0]] == CELL_WALL):
                print("Error: Cell at ({0},{1}) is a wall but should be open".format(row,col_clue[0]))
                exit()

        #Verify top edge is off the grid or a wall
        if(col_clue[1] > 0 and GRID_LAYOUT[col_clue[1]-1][col_clue[0]] == CELL_OPEN):
            print("Error: Col clue {0}, says Cell at ({1},{2}) should be a wall".format(col_clue,col_clue[1]-1,col_clue[0]))
            exit()

        #Verify bottom edge is off the grid or a wall
        if(col_clue[2] < len(GRID_LAYOUT)-1 and GRID_LAYOUT[col_clue[2]+1][col_clue[0]] == CELL_OPEN):
            print("Error: Col clue {0}, says Cell at ({1},{2}) should be a wall".format(col_clue,col_clue[2]+1,col_clue[0]))
            exit()

    #Generate possible row/col digit sum solutions
    possible_digit_sums = []
    for total_digits in range(0,10):
        temp_row = []
        for digit_sum in range(0,46):
            temp_row.append([])
        possible_digit_sums.append(temp_row)

    digits = [0,0,0,0,0,0,0,0,0]
    for digits[0] in range(2,10):
        for digits[1] in range(0,max(digits[0],1)):
            for digits[2] in range(0,max(digits[1],1)):
                for digits[3] in range(0,max(digits[2],1)):
                    for digits[4] in range(0,max(digits[3],1)):
                        for digits[5] in range(0,max(digits[4],1)):
                            for digits[6] in range(0,max(digits[5],1)):
                                for digits[7] in range(0,max(digits[6],1)):
                                    for digits[8] in range(0,max(digits[7],1)):
                                        if(digits.count(0) <= 7):
                                            total_digits = 9-digits.count(0)
                                            digit_sum = sum(digits)
                                            possible_digit_sums[total_digits][digit_sum].append(list(filter((0).__ne__, digits)))

    #Generate the possible digit values for each open cell
    for row in range(0,len(GRID_LAYOUT)):
        temp_row = []
        for col in range(0,len(GRID_LAYOUT[row])):
            if(GRID_LAYOUT[row][col] == CELL_OPEN):
                temp_row.append([1,2,3,4,5,6,7,8,9])
            elif(GRID_LAYOUT[row][col] == CELL_WALL):
                temp_row.append([])
        possible_cell_values.append(temp_row)
    
    #Generate the possible digit sum answers for the given puzzle
    for i in range(0,len(ROW_CLUES)):
        possible_clue_row_answers.append(dc(possible_digit_sums[ROW_CLUES[i][2]-ROW_CLUES[i][1]+1][ROW_CLUES[i][3]]))

    for i in range(0,len(COL_CLUES)):
        possible_clue_col_answers.append(dc(possible_digit_sums[COL_CLUES[i][2]-COL_CLUES[i][1]+1][COL_CLUES[i][3]]))

def solve(pos_cell_values,pos_row_answers,pos_col_answers):

    #Continuously make updates to the puzzle where possible
    progress_made = True
    while(progress_made):
        progress_made = False

        #Check if any cells have no possible values any more (Fail state)
        #Or if all open cells have a single possible value (Win state)
        all_cells_pinned = True
        for row in range(0,len(GRID_LAYOUT)):
            for col in range(0,len(GRID_LAYOUT[row])):
                if(GRID_LAYOUT[row][col] == CELL_OPEN):
                    if(len(pos_cell_values[row][col]) == 0):
                        #This cell has no possible values anymore
                        #A logical contradiction was reached and we need to return
                        ###print("No possible values at ({0}, {1})".format(row,col))
                        return
                    elif(len(pos_cell_values[row][col]) > 1):
                        #This cell still has more than one possible value, we'll have to keep solving
                        all_cells_pinned = False

        if all_cells_pinned:
            #Win condition
            print("*"*len(GRID_LAYOUT[0]))
            for row in range(0,len(GRID_LAYOUT)):
                for col in range(0,len(GRID_LAYOUT[row])):
                    if(GRID_LAYOUT[row][col] == CELL_WALL):
                        print("#",end="")
                    else:
                        print(pos_cell_values[row][col][0],end="")
                print("\n",end="")
            print("*"*len(GRID_LAYOUT[0]))
            return

        #Check if any of the possible row/col clues are empty
        for i in range(0,len(pos_row_answers)):
            if(len(pos_row_answers[i]) == 0):
                ###print("Row Clue {0} no longer has a viable sum".format(ROW_CLUES[i]))
                return
            
        for i in range(0,len(pos_col_answers)):
            if(len(pos_col_answers[i]) == 0):
                ###print("Col Clue {0} no longer has a viable sum".format(COL_CLUES[i]))
                return
            
        #For each row clue, see if the possible digits limits any known digits in the given range
        for i in range(0,len(ROW_CLUES)):
            #Determine if any possible row clue digit-sums can be eliminated
            removed_digit_sums = []
            pos_cell_values_copy = dc(pos_cell_values)
            for digit_sum in pos_row_answers[i]:
                all_perms = list(perm(range(0,len(digit_sum))))
                valid_perm_found = False
                for perm_iter in all_perms:
                    digit_fits = True
                    for col in range(ROW_CLUES[i][1],ROW_CLUES[i][2]+1):
                        if(digit_sum[perm_iter[ROW_CLUES[i][1]-col]] not in pos_cell_values[ROW_CLUES[i][0]][col]):
                            digit_fits = False
                    if(digit_fits):
                        valid_perm_found = True

                        #If a valid digit sum was found, remove those digits from consideration later in the possible cell grid
                        for col in range(ROW_CLUES[i][1],ROW_CLUES[i][2]+1):
                            if(digit_sum[perm_iter[ROW_CLUES[i][1]-col]] in pos_cell_values_copy[ROW_CLUES[i][0]][col]):
                                pos_cell_values_copy[ROW_CLUES[i][0]][col].remove(digit_sum[perm_iter[ROW_CLUES[i][1]-col]])
                
                if(not valid_perm_found):
                    ###print("row clue {0} no longer allows possible digit sum {1}".format(ROW_CLUES[i],digit_sum))
                    removed_digit_sums.append(digit_sum)
                    progress_made = True
            
            for bad_digit_sum in removed_digit_sums:
                pos_row_answers[i].remove(bad_digit_sum)

            for col in range(ROW_CLUES[i][1],ROW_CLUES[i][2]+1):
                for digit in pos_cell_values_copy[ROW_CLUES[i][0]][col]:
                    pos_cell_values[ROW_CLUES[i][0]][col].remove(digit)
                    ###print("Removing {0} from ({1}, {2}) as it can't fit with row clue {3}".format(digit,ROW_CLUES[i][0],col,ROW_CLUES[i]))
                    progress_made = True

        #For each col clue, see if the possible digits limits any known digits in the given range
        for i in range(0,len(COL_CLUES)):
            #Determine if any possible col clue digit-sums can be eliminated
            removed_digit_sums = []
            pos_cell_values_copy = dc(pos_cell_values)
            for digit_sum in pos_col_answers[i]:
                all_perms = list(perm(range(0,len(digit_sum))))
                valid_perm_found = False
                for perm_iter in all_perms:
                    digit_fits = True
                    for row in range(COL_CLUES[i][1],COL_CLUES[i][2]+1):
                        if(digit_sum[perm_iter[COL_CLUES[i][1]-row]] not in pos_cell_values[row][COL_CLUES[i][0]]):
                            digit_fits = False
                            break
                    if(digit_fits):
                        valid_perm_found = True

                        #If a valid digit sum was found, remove those digits from consideration later in the possible cell grid
                        for row in range(COL_CLUES[i][1],COL_CLUES[i][2]+1):
                            if(digit_sum[perm_iter[COL_CLUES[i][1]-row]] in pos_cell_values_copy[row][COL_CLUES[i][0]]):
                                pos_cell_values_copy[row][COL_CLUES[i][0]].remove(digit_sum[perm_iter[COL_CLUES[i][1]-row]])
                
                if(not valid_perm_found):
                    ###print("col clue {0} no longer allows possible digit sum {1}".format(COL_CLUES[i],digit_sum))
                    removed_digit_sums.append(digit_sum)
                    progress_made = True
            
            for bad_digit_sum in removed_digit_sums:
                pos_col_answers[i].remove(bad_digit_sum)

            for row in range(COL_CLUES[i][1],COL_CLUES[i][2]+1):
                for digit in pos_cell_values_copy[row][COL_CLUES[i][0]]:
                    pos_cell_values[row][COL_CLUES[i][0]].remove(digit)
                    ###print("Removing {0} from ({1}, {2}) as it can't fit with col clue {3}".format(digit,row,COL_CLUES[i][0],COL_CLUES[i]))
                    progress_made = True

        #For each cell with only one possible digit value, that same digit cannot show up in the same row/col
        for row in range(0,len(GRID_LAYOUT)):
            for col in range(0,len(GRID_LAYOUT[row])):
                if(len(pos_cell_values[row][col]) == 1):
                    digit = pos_cell_values[row][col][0]
                    
                    #Right
                    xcol = col+1
                    while(xcol < len(GRID_LAYOUT[row]) and GRID_LAYOUT[row][xcol] == CELL_OPEN):
                        if(digit in pos_cell_values[row][xcol]):
                            ###print("Removing ({0}) from ({1},{2}), digit known at ({3},{4})".format(digit,row,xcol,row,col))
                            pos_cell_values[row][xcol].remove(digit)
                            progress_made = True
                        xcol += 1

                    #Down
                    xrow = row+1
                    while(xrow < len(GRID_LAYOUT) and GRID_LAYOUT[xrow][col] == CELL_OPEN):
                        if(digit in pos_cell_values[xrow][col]):
                            ###print("Removing ({0}) from ({1},{2}), digit known at ({3},{4})".format(digit,xrow,col,row,col))
                            pos_cell_values[xrow][col].remove(digit)
                            progress_made = True
                        xrow += 1

                    #Left
                    xcol = col-1
                    while(xcol >= 0 and GRID_LAYOUT[row][xcol] == CELL_OPEN):
                        if(digit in pos_cell_values[row][xcol]):
                            ###print("Removing ({0}) from ({1},{2}), digit known at ({3},{4})".format(digit,row,xcol,row,col))
                            pos_cell_values[row][xcol].remove(digit)
                            progress_made = True
                        xcol -= 1

                    #Up
                    xrow = row-1
                    while(xrow >= 0 and GRID_LAYOUT[xrow][col] == CELL_OPEN):
                        if(digit in pos_cell_values[xrow][col]):
                            ###print("Removing ({0}) from ({1},{2}), digit known at ({3},{4})".format(digit,xrow,col,row,col))
                            pos_cell_values[xrow][col].remove(digit)
                            progress_made = True
                        xrow -= 1

    for row in range(0,len(GRID_LAYOUT)):
        for col in range(0,len(GRID_LAYOUT[row])):
            if(len(pos_cell_values[row][col]) > 1):
                for guessed_digit in pos_cell_values[row][col]:
                    pos_cell_values_copy = dc(pos_cell_values)
                    pos_row_answers_copy = dc(pos_row_answers)
                    pod_col_answers_copy = dc(pos_col_answers)
                    pos_cell_values_copy[row][col] = [guessed_digit]
                    ###print("Guessing {0} on ({1},{2})".format(guessed_digit,row,col))
                    solve(pos_cell_values_copy,
                          pos_row_answers_copy,
                          pod_col_answers_copy)
                return

def main():
    print("Generating puzzle from input file...",end="")
    generatePuzzle()
    print("Done.")

    print("Pre-Solve Work...",end="")
    preSolveWork()
    print("Done.")

    print("Finding solutions...")
    solve(dc(possible_cell_values),
          dc(possible_clue_row_answers),
          dc(possible_clue_col_answers))

if __name__ == "__main__":
    main()