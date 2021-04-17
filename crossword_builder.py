import numpy as np
import random

class Crossword:
    def __init__(self, mat, dict):
        self.grid = mat
        self.grid_info = dict

    def print_grid(self):
        print('\n')
        for i in self.grid:
            for j in i:
                if j <0:
                    print('.',end=' ')
                elif j > 0:
                    print(chr(j),end=' ')
                else:
                    print(' ', end=' ')
            print()

    def print_grid_info(self):
        print('\n----------- GRID ------------\n')
        for word in self.grid_info:
            print(word, '\t: ',grid_info[word]['cord'],'\t',grid_info[word]['type'])
        print('\n\n')


#global-variables (because me == noob coder)
grid_info = {}
temp_grid_info = {}
mat = []
loose_cw = True

# some small-job functions :

def copy_dict(original):
    new = {}
    for word in original:
        new[word] = {'cord':original[word]['cord'], 'type':original[word]['type']}
    
    return new

def adjust_mat(arr):
    rows = arr.shape[0]
    cols = arr.shape[1]
    flag = 1
    while rows<15:
        arr = add_rows(arr, 1, 'down') 
        rows += 1

    while cols<15:
        arr = add_columns(arr, 1, 'right')
        cols += 1

    return arr

def add_columns(arr, num, mode):

    dummy = np.array( [ [0 for i in range(num) ] for i in range(arr.shape[0])] )

    if mode == 'right':
        arr = np.concatenate((arr, dummy), axis=1)
    elif mode == 'left':
        arr = np.concatenate((dummy, arr), axis=1)
    
    return arr

def add_rows(arr, num, mode):

    dummy = np.array( [ [0 for i in range(arr.shape[1]) ] for i in range(num)] )

    if mode == 'down':
        arr = np.concatenate((arr, dummy), axis=0)
    elif mode == 'up':
        arr = np.concatenate((dummy, arr), axis=0)
    
    return arr



#Crossword building functions :

def updateGridInfo(r,c):
    global temp_grid_info
    for word in temp_grid_info:
        temp_grid_info[word]['cord'] = ( temp_grid_info[word]['cord'][0] + r, temp_grid_info[word]['cord'][1] + c )
                
def findInsertions(word, grid_info):
    co_ords=[]
    for testword in grid_info:
        for p,c in enumerate(word):
             for pos,char in enumerate(testword):
                 if char==c:
                    new_coord = list(grid_info[testword]['cord'])

                    if grid_info[testword]['type'] == 'a':
                        new_coord[1] = new_coord[1] + pos
                        align = 'd'
                    else:
                        new_coord[0] = new_coord[0] + pos
                        align = 'a'

                    co_ords.append( [tuple(new_coord),p,align] )

        # links[testword] = co_ords
            
    return co_ords

def prefill_adjustments(word, co_ords, cpos, mode):

    arr = mat.copy()

    r_update = 0
    c_update = 0

    total_rows = arr.shape[0]
    total_cols = arr.shape[1]
    
    if mode == 'a':
        start_filling_at = [co_ords[0], co_ords[1] - cpos]

        cols_req_left = cpos
        cols_req_right = len(word) - cpos - 1

        cols_avail_left = co_ords[1]
        cols_avail_right = total_cols - co_ords[1] - 1

        if cols_req_left > cols_avail_left:
            cols_to_be_added = cols_req_left - cols_avail_left
            arr = add_columns(arr, cols_to_be_added, 'left')
            c_update = cols_to_be_added
            
        
        if cols_req_right > cols_avail_right:
            cols_to_be_added = cols_req_right - cols_avail_right
            arr = add_columns(arr, cols_to_be_added, 'right')


    if mode == 'd':
        start_filling_at = [ co_ords[0] - cpos, co_ords[1]]

        rows_req_up = cpos
        rows_req_down = len(word) - cpos - 1

        rows_avail_up = co_ords[0]
        rows_avail_down = total_rows - co_ords[0] - 1

        if rows_req_up > rows_avail_up:
            rows_to_be_added = rows_req_up - rows_avail_up
            arr = add_rows(arr, rows_to_be_added, 'up')
            r_update = rows_to_be_added
        
        if rows_req_down > rows_avail_down:
            rows_to_be_added = rows_req_down - rows_avail_down
            arr = add_rows(arr, rows_to_be_added, 'down')

    updateGridInfo(r_update, c_update)
    # print('r_update = ',r_update,'\tc_update = ',c_update)

    start_filling_at = ( start_filling_at[0] + r_update, start_filling_at[1] + c_update)

    return arr,start_filling_at

def fill(arr, word, start_point, mode):

    cursor_r = start_point[0]
    cursor_c = start_point[1]


    if mode == 'a':
        try:
            if arr[cursor_r][cursor_c-1] != 0  or arr[cursor_r][cursor_c+len(word)] != 0 :  #if new_word looks(in the grid) as a continuation of another word
                # print("Word continued ERROR")
                return mat,False
        except:
            pass
        for c in word:
            try:
                if arr[cursor_r][cursor_c] == 0 or arr[cursor_r][cursor_c] == ord(c):   #if no overwriting
                    
                    #some more error handling below for sparse crosswords
                    if loose_cw == True and arr[cursor_r][cursor_c] == 0:
                        try:
                            if arr[ cursor_r -1 ][cursor_c] != 0:               #if not empty above
                                return mat,False
                        except:
                            pass

                        try:
                            if arr[cursor_r + 1 ][cursor_c] != 0:               #if not empty below
                                return mat,False
                        except:
                            pass

                    arr[cursor_r][cursor_c] = ord(c)    #non error case
                else:
                    # print("Overwriting ERROR")
                    return mat,False
            except:
                return mat,False
            cursor_c += 1



    if mode == 'd':
        try:
            if arr[cursor_r-1][cursor_c] != 0 or arr[cursor_r+len(word)][cursor_c] != 0:
                # print("Word continued ERROR")
                return mat,False
        except:
            pass
        for c in word:
            try:
                if arr[cursor_r][cursor_c] == 0 or arr[cursor_r][cursor_c] == ord(c):   #if no overwriting

                    #some more error handling below
                    if loose_cw == True and arr[cursor_r][cursor_c] == 0:
                        try:
                            if arr[cursor_r][ cursor_c-1] != 0:         #if nonempty to left
                                return mat,False
                        except:
                            pass

                        try:
                            if arr[cursor_r][ cursor_c+1] != 0:         #if nonempty to right
                                return mat,False
                        except:
                            pass
                    
                    arr[cursor_r][cursor_c] = ord(c)    #the non error case
                else:
                    # print("Overwriting ERROR")
                    return mat,False
            except:
                return mat,False
            cursor_r += 1

    return arr,True

def builder(all_words):
    global mat
    global grid_info
    global temp_grid_info

    startword = random.choice(all_words)
    mat = np.array( [[ord(startword[i]) for i in range(len(startword))]])

    grid_info = {   
                    startword   :   {'cord':(0,0),'type':'a'}
                }

    all_words.remove(startword)

    # ---------------------------------- Crossword Creation Code -------------------------------
    temp_grid_info = copy_dict( grid_info )
    stopper = 50
    while len(all_words) != 0 and stopper > 0:

        myword = random.choice( all_words )
        insertions = findInsertions(myword, grid_info )

        # print('\n\n-------- word : ',myword,'--------------')
        word_added =False
        for trial in insertions:
            # print(trial)
            temp_grid_info = copy_dict( grid_info )

            arr,start_at = prefill_adjustments(myword, trial[0], trial[1], trial[2])

            arr,result = fill(arr, myword, start_at, trial[2])

            if result == True :
                mat = arr.copy()                                            #succesful insertion hence we commit our changes           
                grid_info = copy_dict(temp_grid_info)

                grid_info[myword] = {'cord':start_at,'type':trial[2]}       #making an addition to grid_info
                word_added = True
                break
        
        if word_added == True:
            all_words.remove(myword)

        # printmat()

        stopper -= 1

    #---------------------------------------------------------------------------------------------

    if len(all_words) == 0:
        return True
    else:
        return False





# Some debugging/printing functions :
def printmat():
    print('\n')
    for i in mat:
        for j in i:
            if j <0:
                print('.',end=' ')
            elif j > 0:
                print(chr(j),end=' ')
            else:
                print(' ', end=' ')
        print()

def print_gridinfo():
    print('\n----------- GRID ------------\n')
    for word in grid_info:
        print(word, '\t: ',grid_info[word]['cord'],'\t',grid_info[word]['type'])
    print('\n\n')

# input : a list of words
# output : a crossword object
def give_crossword(word_list):
    global mat
    while(True):

        all_words = word_list.copy()

        result = builder(all_words)
        #below is some filtering to get only GOOD-looking crosswords
        ratio = mat.shape[0]/mat.shape[1]

        if result==True and max(mat.shape) <=15 and abs(1-ratio) < 0.3:
            mat = adjust_mat(mat)
            return Crossword(mat, grid_info)


# mycw = give_crossword(all_words)

# mycw.print_grid()
# mycw.print_grid_info()
