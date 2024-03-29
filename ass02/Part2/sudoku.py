from sys import exit
from copy import deepcopy
from itertools import combinations



class SudokuError(Exception):
    def __init__(self, message):
        self.message = message


class Sudoku():
    def __init__(self, filename):
        self.matrix = []
        self.filename = filename
        self.latex_prefix = [
                r'\documentclass[10pt]{article}',
                r'\usepackage[left=0pt,right=0pt]{geometry}',
                r'\usepackage{tikz}',
                r'\usetikzlibrary{positioning}',
                r'\usepackage{cancel}',
                r'\pagestyle{empty}',
                r'',
                r'\newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},',
                r'                               label=above right:{\tiny #2},',
                r'                               label=below left:{\tiny #3},',
                r'                               label=below right:{\tiny #4}]{#5};}}',
                '',
                r'\begin{document}',
                '',
                r'\tikzset{every node/.style={minimum size=.5cm}}',
                '',
                r'\begin{center}',
                r'\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline',
                ]
        #   check the validity of input, and generate matrix
        with open(filename) as input_file:
            for line in input_file:
                if not line.isspace():
                    # check each value is an integer and between 0 and 9
                    matrix_row = []
                    for e in line.strip().replace(" ", ""):
                        try:
                            if int(e)>=0 and int(e)<=9:
                                matrix_row.append(int(e))
                            else:
                                # print('some integer out of range')
                                raise SudokuError('Incorrect input')
                                sys.exit()
                        except ValueError:
                            # print('some are not integer')
                            raise SudokuError('Incorrect input')
                            sys.exit()
                    # check the length of each row is 9
                    if len(matrix_row) != 9:
                        # print('check the length of each row is 9')
                        raise SudokuError('Incorrect input')
                        sys.exit()
                    self.matrix.append(matrix_row)
        # check the length of column is 9
        if len(self.matrix) != 9:
            # print('check the length of column is 9')
            raise SudokuError('Incorrect input')
            sys.exit()
        # initialize marked matrix
        self.marked_matrix = [[0 for j in range(9)] for j in range(9)]
        self._mark_matrix()
        # re_generate marked matrix untill nothing to generate
        while(self._remark_matrix_by_forced_digits()):
            self._remark_matrix()
        # sort marked matrix
        for row in self.marked_matrix:
            for cell in row:
                cell.sort()



    def _mark_matrix(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    # row set
                    set_row = set(self.matrix[i])
                    # column set
                    set_column = set()
                    for _ in range(9):
                        set_column.add(self.matrix[_][j])
                    # box set
                    set_box = set()
                    for box_i in range(i // 3 *3, i // 3 *3 + 3):
                        for box_j in range(j // 3 *3, j // 3 *3 + 3):
                            set_box.add(self.matrix[box_i][box_j])
                    # generate cell: {1, 2, 3, 4, 5, 6, 7, 8 ,9} - row - column - box
                    set_cell = set([1, 2, 3, 4, 5, 6, 7, 8 ,9]) - set_row - set_column - set_box
                    self.marked_matrix[i][j] = list(set_cell)
                else:
                    self.marked_matrix[i][j] = list([self.matrix[i][j]])



    def _remark_matrix_by_forced_digits(self):
        having_changed = False
        # scan for each empty cell
        for i in range(9):
            for j in range(9):
                if len(self.marked_matrix[i][j]) > 1:
                    # pick an cadidate value e from the cell
                    for e in self.marked_matrix[i][j]:
                        # generate a set contains values in other cells of the same box
                        other_cell_same_box = set()
                        for box_i in range(i // 3 *3, i // 3 *3 + 3):
                            for box_j in range(j // 3 *3, j // 3 *3 + 3):
                                if box_i != i or box_j != j:    # other cell
                                    other_cell_same_box |= set(self.marked_matrix[box_i][box_j])
                        # find whether e is unique in its box
                        if e not in other_cell_same_box:
                            self.marked_matrix[i][j] = [e]
                            having_changed = True
                            break
        return having_changed



    def _remark_matrix(self):
        copied_marked_matrix = deepcopy(self.marked_matrix)
        for i in range(9):
            for j in range(9):
                if len(copied_marked_matrix[i][j]) > 1:
                    # row set
                    set_row = set()
                    for cell in copied_marked_matrix[i]:
                        if len(cell) == 1:
                            set_row.add(cell[0])
                    # column set
                    set_column = set()
                    for _ in range(9):
                        if len(copied_marked_matrix[_][j]) == 1:
                            set_column.add(copied_marked_matrix[_][j][0])
                    # box set
                    set_box = set()
                    for box_i in range(i // 3 *3, i // 3 *3 + 3):
                        for box_j in range(j // 3 *3, j // 3 *3 + 3):
                            if len(copied_marked_matrix[box_i][box_j]) == 1:
                                set_box.add(copied_marked_matrix[box_i][box_j][0])
                    # generate cell: {1, 2, 3, 4, 5, 6, 7, 8 ,9} - row - column - box
                    set_cell = set([1, 2, 3, 4, 5, 6, 7, 8 ,9]) - set_row - set_column - set_box
                    # print("set_row=", set_row)
                    # print("set_column=", set_column)
                    # print("set_box=", set_box)
                    # print("set_cell=", set_cell)
                    self.marked_matrix[i][j] = list(set_cell)




    def preassess(self):
        # check numbers in each row is unique
        for row in self.matrix:
            existed_number = {0}
            for e in row:
                if e != 0:
                    if e in existed_number:
                        print('There is clearly no solution.')
                        return
                    else:
                        existed_number.add(e)
        # check numbers in each column is unique
        for j in range(9):
            existed_number = {0}
            for i in range(9):
                e = self.matrix[i][j]
                if e != 0:
                    if e in existed_number:
                        print('There is clearly no solution.')
                        return
                    else:
                        existed_number.add(e)
        # generate cells
        matrix_cell = []
        for nb_of_cell_i in range(3):
            for nb_of_cell_j in range(3):
                cell = []
                for i in range(nb_of_cell_i*3, 3 + nb_of_cell_i*3):
                    for j in range(nb_of_cell_j*3, 3 + nb_of_cell_j*3):
                        cell.append(self.matrix[i][j])
                matrix_cell.append(cell)
        # check numbers in each cell is unique
        for cell in matrix_cell:
            existed_number = {0}
            for e in cell:
                if e != 0:
                    if e in existed_number:
                        print('There is clearly no solution.')
                        return
                    else:
                        existed_number.add(e)
        print('There might be a solution.')



    def bare_tex_output(self):
        # generate latex file name
        latex_bare_filename = ""
        for s in self.filename:
            if s != ".":
                latex_bare_filename += s
            else:
                break
        latex_bare_filename += "_bare.tex"
        # create and handle latex file
        with open(latex_bare_filename, "w+") as output_file:
            # convert matrix to matrix_string, where every none zero value is string, and zero value is empty string
            matrix_string = []
            for row in self.matrix:
                row_string = []
                for e in row:
                    if e == 0:
                        row_string.append('')
                    else:
                        row_string.append(str(e))
                matrix_string.append(row_string)
            # write latex file
            for line in self.latex_prefix:
                output_file.write(line + "\n")
            for i in range(9):
                output_file.write(r"% Line " + str(i+1) + "\n")
                output_file.write(r"\N{}{}{}{}{" + matrix_string[i][0]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][1]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][2]
                                  + r"} &" + "\n"
                                  + r"\N{}{}{}{}{" + matrix_string[i][3]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][4]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][5]
                                  + r"} &" + "\n"
                                  + r"\N{}{}{}{}{" + matrix_string[i][6]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][7]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][8]
                                  + r"}"
                                  )
                if i+1 in (1, 2, 4 ,5 ,7 ,8):
                    output_file.write(r" \\ \hline" + "\n" + "\n")
                if i+1 in (3, 6):
                    output_file.write(r" \\ \hline\hline" + "\n" + "\n")
                if i+1 == 9:
                    output_file.write(r" \\ \hline\hline" + "\n"
                                        + r"\end{tabular}"  + "\n"
                                        + r"\end{center}" + "\n"
                                        + "\n"
                                        + r"\end{document}" + "\n"
                                        )



    def forced_tex_output(self):
        # generate latex file name
        latex_forced_filename = ""
        for s in self.filename:
            if s != ".":
                latex_forced_filename += s
            else:
                break
        latex_forced_filename += "_forced.tex"
        # create and handle latex file
        with open(latex_forced_filename, "w+") as output_file:
            # convert marked_matrix to matrix_string, where every none zero value is string, and zero value is empty string
            matrix_string = []
            for row in self.marked_matrix:
                row_string = []
                for cell in row:
                    if len(cell) == 1:
                        row_string.append(str(cell[0]))
                    else:
                        row_string.append('')
                matrix_string.append(row_string)
                # print(matrix_string)
            # write latex file
            for line in self.latex_prefix:
                output_file.write(line + "\n")
            for i in range(9):
                output_file.write(r"% Line " + str(i+1) + "\n")
                output_file.write(r"\N{}{}{}{}{" + matrix_string[i][0]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][1]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][2]
                                  + r"} &" + "\n"
                                  + r"\N{}{}{}{}{" + matrix_string[i][3]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][4]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][5]
                                  + r"} &" + "\n"
                                  + r"\N{}{}{}{}{" + matrix_string[i][6]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][7]
                                  + r"} & \N{}{}{}{}{" + matrix_string[i][8]
                                  + r"}"
                                  )
                if i+1 in (1, 2, 4 ,5 ,7 ,8):
                    output_file.write(r" \\ \hline" + "\n" + "\n")
                if i+1 in (3, 6):
                    output_file.write(r" \\ \hline\hline" + "\n" + "\n")
                if i+1 == 9:
                    output_file.write(r" \\ \hline\hline" + "\n"
                                        + r"\end{tabular}"  + "\n"
                                        + r"\end{center}" + "\n"
                                        + "\n"
                                        + r"\end{document}" + "\n"
                                        )



    def marked_tex_output(self):
        # generate latex file name
        latex_marked_filename = ""
        for s in self.filename:
            if s != ".":
                latex_marked_filename += s
            else:
                break
        latex_marked_filename += "_marked.tex"
        # create and handle latex file
        with open(latex_marked_filename, "w+") as output_file:
            # convert marked_matrix to matrix_string
            matrix_string = []
            for row in self.marked_matrix:
                row_string = []
                for cell in row:
                    cell_string = ""
                    if len(cell) == 1:
                        cell_string = "{}{}{}{}{" + str(cell[0]) + "}"
                    else:
                        # top left
                        cell_string += "{"
                        if 1 in cell and 2 not in cell:
                            cell_string += "1"
                        if 1 not in cell and 2 in cell:
                            cell_string += "2"
                        if 1 in cell and 2 in cell:
                            cell_string += "1 2"
                        cell_string += "}{"
                        # top right
                        if 3 in cell and 4 not in cell:
                            cell_string += "3"
                        if 3 not in cell and 4 in cell:
                            cell_string += "4"
                        if 3 in cell and 4 in cell:
                            cell_string += "3 4"
                        cell_string += "}{"
                        # bottom left
                        if 5 in cell and 6 not in cell:
                            cell_string += "5"
                        if 5 not in cell and 6 in cell:
                            cell_string += "6"
                        if 5 in cell and 6 in cell:
                            cell_string += "5 6"
                        cell_string += "}{"
                        # bottom right
                        if 7 in cell and 8 not in cell and 9 not in cell:
                            cell_string += "7"
                        if 7 not in cell and 8 in cell and 9 not in cell:
                            cell_string += "8"
                        if 7 not in cell and 8 not in cell and 9 in cell:
                            cell_string += "9"
                        if 7 in cell and 8 in cell and 9 not in cell:
                            cell_string += "7 8"
                        if 7 in cell and 8 not in cell and 9 in cell:
                            cell_string += "7 9"
                        if 7 not in cell and 8 in cell and 9 in cell:
                            cell_string += "8 9"
                        if 7 in cell and 8 in cell and 9 in cell:
                            cell_string += "7 8 9"
                        cell_string += r"}{}"
                    row_string.append(cell_string)
                matrix_string.append(row_string)
            # write latex file
            for line in self.latex_prefix:
                output_file.write(line + "\n")
            for i in range(9):
                output_file.write(r"% Line " + str(i+1) + "\n")
                output_file.write(r"\N" + matrix_string[i][0]
                                + r" & \N" + matrix_string[i][1]
                                + r" & \N" + matrix_string[i][2]
                                + r" &" + "\n"
                                + r"\N" + matrix_string[i][3]
                                + r" & \N" + matrix_string[i][4]
                                + r" & \N" + matrix_string[i][5]
                                + r" &" + "\n"
                                + r"\N" + matrix_string[i][6]
                                + r" & \N" + matrix_string[i][7]
                                + r" & \N" + matrix_string[i][8]
                                )
                if i+1 in (1, 2, 4 ,5 ,7 ,8):
                    output_file.write(r" \\ \hline" + "\n" + "\n")
                if i+1 in (3, 6):
                    output_file.write(r" \\ \hline\hline" + "\n" + "\n")
                if i+1 == 9:
                    output_file.write(r" \\ \hline\hline" + "\n"
                                        + r"\end{tabular}"  + "\n"
                                        + r"\end{center}" + "\n"
                                        + "\n"
                                        + r"\end{document}" + "\n"
                                        )



    def worked_tex_output(self):
        self.flag_not_finish = True
        self._debug = False
        # generate worked_matrix in which cells are represented by set
        self.worked_matrix = []
        for row in self.marked_matrix:
            worked_row = []
            for cell in row:
                worked_row.append(set(cell))
            self.worked_matrix.append(worked_row)
        # print('before change data structure')
        # generate worked list
        self.flag_not_finish = True
        while self.flag_not_finish:
            self.flag_not_finish = False
            self._remove_preemptive_row()
            self._remark_worded_matrix()            
            self._remove_preemptive_column()
            self._remark_worded_matrix()                
            self._remove_preemptive_box()
            self._remark_worded_matrix()
        # for debug sudoku_4
        # self.worked_matrix = [[{6}, {3}, {9}, {5}, {7}, {4}, {1}, {8}, {2}],
        #                       [{5}, {4}, {1}, {8}, {2}, {9}, {3}, {7}, {6}],
        #                       [{7}, {8}, {2}, {6}, {1}, {3}, {9}, {5}, {4}],
        #                       [{1}, {9}, {8}, {4}, {6}, {7}, {5}, {2}, {3}],
        #                       [{3}, {6}, {5}, {9}, {8}, {2}, {4}, {1}, {7}],
        #                       [{4}, {2}, {7}, {1}, {3}, {5}, {8}, {6}, {9}],
        #                       [{9}, {5}, {6}, {7}, {4}, {8}, {2}, {3}, {1}],
        #                       [{8}, {1}, {3}, {2}, {9}, {6}, {7}, {4}, {5}],
        #                       [{2}, {7}, {4}, {3}, {5}, {1}, {6}, {9}, {8}]
        #                      ]
        # self.worked_matrix = [
        #                       [{2}, {9}, {5}, {7}, {3, 4}, {1, 3, 4}, {8}, {6}, {1, 3, 4}],
        #                       [{4, 7}, {3}, {1}, {8}, {6}, {5}, {9}, {2}, {4, 7}],
        #                       [{8}, {4, 7}, {6}, {1, 2, 4, 9}, {9, 2, 3, 4}, {1, 2, 3, 4, 9}, {9, 4, 5}, {1, 3, 4, 9}, {1, 3, 4, 5, 7}],
        #                       [{1, 3}, {8, 1}, {7}, {9, 2, 4}, {5}, {9, 2, 4}, {9, 2, 4}, {1, 3, 8}, {6}],
        #                       [{1, 4, 6, 9}, {1, 4, 6}, {9, 2}, {3}, {8}, {7}, {9, 2, 4, 5}, {1, 4, 9}, {1, 4, 5}],
        #                       [{5}, {8, 4}, {8, 9, 2, 3}, {9, 2, 4}, {1}, {6}, {7}, {8, 9, 3, 4}, {8, 3, 4}],
        #                       [{3, 6, 7}, {8, 6, 7}, {8, 3}, {5}, {2, 3, 4, 7}, {2, 3, 4}, {1}, {8, 4}, {9}],
        #                       [{1, 9, 7}, {2}, {8, 9}, {6}, {9, 4, 7}, {1, 4, 9}, {3}, {5}, {8, 4}],
        #                       [{1, 3, 9}, {5}, {4}, {1, 9}, {9, 3}, {8}, {6}, {7}, {2}]
        #                      ]
        # change data structure of self.worked_matrix
        self.worked_matrix_list = []
        for row in self.worked_matrix:
            worked_row = []
            for cell in row:
                worked_row.append(sorted(list(cell)))
            self.worked_matrix_list.append(worked_row)
        # print('before generate tex file')
        # generate tex file
        latex_worked_filename = ""
        for s in self.filename:
            if s != ".":
                latex_worked_filename += s
            else:
                break
        latex_worked_filename += "_worked.tex"
        # create and handle latex file
        with open(latex_worked_filename, "w+") as output_file:
            # convert marked_matrix to matrix_string
            matrix_string = []
            for i in range(9):
                row_string = []
                for j in range(9):
                    # c_worded is a subset of c_marked
                    c_marked = self.marked_matrix[i][j]
                    c_worked = self.worked_matrix_list[i][j]
                    cell_string = ""
                    if c_marked == c_worked:
                        if len(c_marked) == 1:
                            cell_string = "{}{}{}{}{" + str(c_marked[0]) + "}"
                        else:
                            # top left
                            cell_string += "{"
                            if 1 in c_marked and 2 not in c_marked:
                                cell_string += "1"
                            if 1 not in c_marked and 2 in c_marked:
                                cell_string += "2"
                            if 1 in c_marked and 2 in c_marked:
                                cell_string += "1 2"
                            cell_string += "}{"
                            # top right
                            if 3 in c_marked and 4 not in c_marked:
                                cell_string += "3"
                            if 3 not in c_marked and 4 in c_marked:
                                cell_string += "4"
                            if 3 in c_marked and 4 in c_marked:
                                cell_string += "3 4"
                            cell_string += "}{"
                            # bottom left
                            if 5 in c_marked and 6 not in c_marked:
                                cell_string += "5"
                            if 5 not in c_marked and 6 in c_marked:
                                cell_string += "6"
                            if 5 in c_marked and 6 in c_marked:
                                cell_string += "5 6"
                            cell_string += "}{"
                            # bottom right
                            if 7 in c_marked and 8 not in c_marked and 9 not in c_marked:
                                cell_string += "7"
                            if 7 not in c_marked and 8 in c_marked and 9 not in c_marked:
                                cell_string += "8"
                            if 7 not in c_marked and 8 not in c_marked and 9 in c_marked:
                                cell_string += "9"
                            if 7 in c_marked and 8 in c_marked and 9 not in c_marked:
                                cell_string += "7 8"
                            if 7 in c_marked and 8 not in c_marked and 9 in c_marked:
                                cell_string += "7 9"
                            if 7 not in c_marked and 8 in c_marked and 9 in c_marked:
                                cell_string += "8 9"
                            if 7 in c_marked and 8 in c_marked and 9 in c_marked:
                                cell_string += "7 8 9"
                            cell_string += r"}{}"
                    elif len(c_worked) == 1:    # we know that len(c_marked) won't be 1
                        # top left
                        cell_string += "{"
                        if 1 in c_marked and 2 not in c_marked:
                            cell_string += "\cancel{1}"
                        if 1 not in c_marked and 2 in c_marked:
                            cell_string += "\cancel{2}"
                        if 1 in c_marked and 2 in c_marked:
                            cell_string += "\cancel{1} \cancel{2}"
                        cell_string += "}{"
                        # top right
                        if 3 in c_marked and 4 not in c_marked:
                            cell_string += "\cancel{3}"
                        if 3 not in c_marked and 4 in c_marked:
                            cell_string += "\cancel{4}"
                        if 3 in c_marked and 4 in c_marked:
                            cell_string += "\cancel{3} \cancel{4}"
                        cell_string += "}{"
                        # bottom left
                        if 5 in c_marked and 6 not in c_marked:
                            cell_string += "\cancel{5}"
                        if 5 not in c_marked and 6 in c_marked:
                            cell_string += "\cancel{6}"
                        if 5 in c_marked and 6 in c_marked:
                            cell_string += "\cancel{5} \cancel{6}"
                        cell_string += "}{"
                        # bottom right
                        if 7 in c_marked and 8 not in c_marked and 9 not in c_marked:
                            cell_string += "\cancel{7}"
                        if 7 not in c_marked and 8 in c_marked and 9 not in c_marked:
                            cell_string += "\cancel{8}"
                        if 7 not in c_marked and 8 not in c_marked and 9 in c_marked:
                            cell_string += "\cancel{9}"
                        if 7 in c_marked and 8 in c_marked and 9 not in c_marked:
                            cell_string += "\cancel{7} \cancel{8}"
                        if 7 in c_marked and 8 not in c_marked and 9 in c_marked:
                            cell_string += "\cancel{7} \cancel{9}"
                        if 7 not in c_marked and 8 in c_marked and 9 in c_marked:
                            cell_string += "\cancel{8} \cancel{9}"
                        if 7 in c_marked and 8 in c_marked and 9 in c_marked:
                            cell_string += "\cancel{7} \cancel{8} \cancel{9}"
                        # middle
                        cell_string += r"}{"+ str(c_worked[0]) +"}"
                    else:                       # both len(c_mark) and len(c_worked) are not 1
                        for index in [1, 3, 5, 7]:    # i in (1, 3, 5, 7)
                            # top left
                            need_space = False
                            cell_string += "{"
                            if index in c_worked:       # add first number, also means i in c_worked and c_marked
                                cell_string += str(index)
                                need_space = True
                            elif index in c_marked:
                                cell_string += r"\cancel{" + str(index) + r"}"
                                need_space = True
                            if index+1 in c_marked and need_space:  # add a space
                                cell_string += " "
                            if index+1 in c_worked:       # add second number
                                cell_string += str(index+1)
                                need_space = True
                            elif index+1 in c_marked:
                                cell_string += r"\cancel{" + str(index+1) + r"}"
                                need_space = True
                            if index != 7:
                                cell_string += "}"
                        if 9 in c_marked and need_space:  # add a space
                            cell_string += " "
                        if 9 in c_worked:       # add number 9
                            cell_string += r"9"
                        elif 9 in c_marked:
                            cell_string += r"\cancel{9}"
                        cell_string += r"}{}"
                    row_string.append(cell_string)
                    # print(row_string)
                # print(row_string)
                matrix_string.append(row_string)
            # write latex file
            for line in self.latex_prefix:
                output_file.write(line + "\n")
            for i in range(9):
                output_file.write(r"% Line " + str(i+1) + "\n")
                output_file.write(r"\N" + matrix_string[i][0]
                                + r" & \N" + matrix_string[i][1]
                                + r" & \N" + matrix_string[i][2]
                                + r" &" + "\n"
                                + r"\N" + matrix_string[i][3]
                                + r" & \N" + matrix_string[i][4]
                                + r" & \N" + matrix_string[i][5]
                                + r" &" + "\n"
                                + r"\N" + matrix_string[i][6]
                                + r" & \N" + matrix_string[i][7]
                                + r" & \N" + matrix_string[i][8]
                                )
                if i+1 in (1, 2, 4 ,5 ,7 ,8):
                    output_file.write(r" \\ \hline" + "\n" + "\n")
                if i+1 in (3, 6):
                    output_file.write(r" \\ \hline\hline" + "\n" + "\n")
                if i+1 == 9:
                    output_file.write(r" \\ \hline\hline" + "\n"
                                        + r"\end{tabular}"  + "\n"
                                        + r"\end{center}" + "\n"
                                        + "\n"
                                        + r"\end{document}" + "\n"
                                        )


    def _remove_preemptive_row(self):
        for i in range(9):
            self._remove_preemptive_single_row(i)


    def _remove_preemptive_single_row(self, i):
        # calculate the max size of preemptive set
        # minutes 1 because counting all unsolved cell to be a preemptive cell is meaningless
        nb_of_unsolved_cells = 0
        for j in range(9):
            if len(self.worked_matrix[i][j]) == 1:
                nb_of_unsolved_cells += 1
        max_size_of_preemptive_set = 9 - nb_of_unsolved_cells - 1
        # try to find preemtive set
        for size_of_preemptive_set in range(2, max_size_of_preemptive_set + 1):
            # generate the set of index of preemptive set combination of index
            candidates = set()
            for j in range(9):
                if len(self.worked_matrix[i][j]) > 1 and len(self.worked_matrix[i][j]) <= size_of_preemptive_set:
                    candidates.add(j)
            combinations_of_index_set = combinations(candidates, size_of_preemptive_set)
            # check where an index set can make a preemptive set
            for index_set in combinations_of_index_set:
                preemptive_set = set()
                preemptive_set_cells = []
                for j in index_set:
                    # print(i+1, j+1, self.worked_matrix[i][j])
                    preemptive_set |= self.worked_matrix[i][j]
                    preemptive_set_cells.append([i + 1, j + 1])
                if len(preemptive_set) == size_of_preemptive_set:
                    # find a preemptive set, cross related numbers in other cells
                    other_index_set = set([0, 1, 2, 3, 4, 5, 6, 7, 8]) - set(index_set)
                    for j in other_index_set:
                        saved_cell = self.worked_matrix[i][j].copy()
                        self.worked_matrix[i][j] -= preemptive_set
                        if self.worked_matrix[i][j] != saved_cell:
                            self.flag_not_finish = True
                    if self._debug and self.flag_not_finish:
                        print('preemptive set:', preemptive_set, "on row", i+1, ",", preemptive_set_cells)


    def _remove_preemptive_column(self):
        for j in range(9):
            self._remove_preemptive_single_column(j)


    def _remove_preemptive_single_column(self, j):
        # calculate the max size of preemptive set
        # minutes 1 because counting all unsolved cell to be a preemptive cell is meaningless
        nb_of_unsolved_cells = 0
        for i in range(9):
            if len(self.worked_matrix[i][j]) == 1:
                nb_of_unsolved_cells += 1
        max_size_of_preemptive_set = 9 - nb_of_unsolved_cells - 1
        # try to find preemtive set
        for size_of_preemptive_set in range(2, max_size_of_preemptive_set + 1):
            # generate the set of index of preemptive set combination of index
            candidates = set()
            for i in range(9):
                if len(self.worked_matrix[i][j]) > 1 and len(self.worked_matrix[i][j]) <= size_of_preemptive_set:
                    candidates.add(i)
            combinations_of_index_set = combinations(candidates, size_of_preemptive_set)
            # check where an index set can make a preemptive set
            for index_set in combinations_of_index_set:
                preemptive_set = set()
                preemptive_set_cells = []
                for i in index_set:
                    # print(i+1, j+1, self.worked_matrix[i][j])
                    preemptive_set |= self.worked_matrix[i][j]
                    preemptive_set_cells.append([i + 1, j + 1])
                if len(preemptive_set) == size_of_preemptive_set:
                    # find a preemptive set, cross related numbers in other cells
                    other_index_set = set([0, 1, 2, 3, 4, 5, 6, 7, 8]) - set(index_set)
                    for i in other_index_set:
                        saved_cell = self.worked_matrix[i][j].copy()
                        self.worked_matrix[i][j] -= preemptive_set
                        if self.worked_matrix[i][j] != saved_cell:
                            self.flag_not_finish = True
                    if self._debug and self.flag_not_finish:
                        print('preemptive set:', preemptive_set, "on column", j+1, ",", preemptive_set_cells)


    def _remove_preemptive_box(self):
        # for no_of_box 0, 1, 2, i is in range(0, 3)
        # for no_of_box 3, 4, 5, i is in range(3, 6)
        # for no_of_box 6, 7, 8, i is in range(6, 9)
        # therefore:        i in range(no_of_box // 3 * 3, no_of_box // 3 * 3 + 3)
        # for no_of_box 0, 3, 6, j is in range(0, 3)
        # for no_of_box 1, 4, 6, j is in range(3, 6)
        # for no_of_box 2, 5, 8, j is in range(6, 9)
        # therefore:        j in range(no_of_box % 3 * 3, no_of_box % 3 * 3 + 3)
        for no_of_box in range(9):
            self._remove_preemptive_single_box(no_of_box)


    def _remove_preemptive_single_box(self, no_of_box):
        # calculate the max size of preemptive set and complete_set_of index
        nb_of_unsolved_cells = 0
        complete_index_set = set()
        for i in range(no_of_box // 3 * 3, no_of_box // 3 * 3 + 3):
            for j in range(no_of_box % 3 * 3, no_of_box % 3 * 3 + 3):
                complete_index_set.add((i, j))
                if len(self.worked_matrix[i][j]) == 1:
                    nb_of_unsolved_cells += 1
        max_size_of_preemptive_set = 9 - nb_of_unsolved_cells - 1
        # try to find preemtive set
        for size_of_preemptive_set in range(2, max_size_of_preemptive_set + 1):
            # generate the index pair of preemptive set
            candidates = set()
            for i in range(no_of_box // 3 * 3, no_of_box // 3 * 3 + 3):
                for j in range(no_of_box % 3 * 3, no_of_box % 3 * 3 + 3):
                    if len(self.worked_matrix[i][j]) > 1 \
                            and len(self.worked_matrix[i][j]) <= size_of_preemptive_set:
                        candidates.add((i, j))
            # generate combination of index
            combinations_of_index_set = combinations(candidates, size_of_preemptive_set)
            for index_set in combinations_of_index_set:
                preemptive_set = set()
                preemptive_set_cells = []
                for (i, j) in index_set:
                    preemptive_set |= self.worked_matrix[i][j]
                    preemptive_set_cells.append([i + 1, j + 1])
                if len(preemptive_set) == size_of_preemptive_set:
                    # find a preemptive set, cross related numbers in other cells
                    other_index_set = complete_index_set - set(index_set)
                    for (i, j) in other_index_set:
                        saved_cell = self.worked_matrix[i][j].copy()
                        self.worked_matrix[i][j] -= preemptive_set
                        if self.worked_matrix[i][j] != saved_cell:
                            self.flag_not_finish = True
                    if self._debug and self.flag_not_finish:
                        print('preemptive set:', preemptive_set, "on box", no_of_box+1, ",", preemptive_set_cells)


    def _remark_worded_matrix(self):
        copied_matrix = deepcopy(self.worked_matrix)
        for i in range(9):
            for j in range(9):
                if len(copied_matrix[i][j]) > 1:
                    # row set
                    set_row = set()
                    for cell in copied_matrix[i]:
                        if len(cell) == 1:
                            set_row |= cell
                    # column set
                    set_column = set()
                    for _ in range(9):
                        if len(copied_matrix[_][j]) == 1:
                            set_column |= copied_matrix[_][j]
                    # box set
                    set_box = set()
                    for box_i in range(i // 3 *3, i // 3 *3 + 3):
                        for box_j in range(j // 3 *3, j // 3 *3 + 3):
                            if len(copied_matrix[box_i][box_j]) == 1:
                                set_box |= copied_matrix[box_i][box_j]
                    # generate cell: {1, 2, 3, 4, 5, 6, 7, 8 ,9} - row - column - box
                    self.worked_matrix[i][j] = self.worked_matrix[i][j] - set_row - set_column - set_box


if __name__ == '__main__':
    def print_matrix(matrix):
        for line in matrix:
            print(line, end='\n')


    sudoku = Sudoku('sudoku_5.txt')
    sudoku.worked_tex_output()
    # print_matrix(sudoku.marked_matrix)
    # print()
    # print_matrix(sudoku.worked_matrix)
