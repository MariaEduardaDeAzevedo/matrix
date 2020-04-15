#coding: utf-8

'''
Módulo voltado para estudo de Álgebra Linear
'''
def remove_row(m, l):
        matrix = dict()

        cont = 0
        for i in range(m.get_rows()):
            if i != l - 1:
                matrix[cont] = m.get_row(i)
                cont += 1

        new_matrix = Matrix()
        new_matrix.set_matrix(matrix)

        return new_matrix

def remove_column(m, c):
    matrix = dict()

    for i in range(m.get_rows()):
        row = m.get_row(i)
        row.pop(c - 1)
        matrix[i] = row

    new_matrix = Matrix()
    new_matrix.set_matrix(matrix)

    return new_matrix

class MatrixError(Exception):
    '''
    Classe de exceções do tipo Matrix
    '''
    def __init__(self, mensage):
        self.mensage = mensage

class Matrix:
    '''
    Classe que representa uma matriz, na qual é possível realizar várias operações
    '''
    def __init__(self, l=0, c=0, e=0):
        '''
        Construtor que recebe um número de linhas, de colunas e o elemento a ser
        inserido em todas as células da matriz criada. Caso nenhum parâmetro seja
        passado, cria-se uma matriz vazia e caso o elemento não seja exigido, cria-se
        uma matriz nula.
        '''
        matrix = dict()
        for i in range(l):
            matrix[i] = [e] * c
        
        self.l = l
        self.c = c
        self.matrix = matrix

    def __str__(self):
        '''
        String que representa um objeto Matrix
        '''
        if (self.get_columns() == self.get_rows() == 0):
            return "[]0x0"

        retorno = ""
        for k in self.matrix.keys():
            retorno += str(self.matrix.get(k))
            if k != self.l - 1:
                retorno += "\n"
        return retorno + str(self.l) + "x" + str(self.c)

    def __add__(self, m):
        '''
        Soma duas matrizes com o uso so operador +
        '''
        try:
            soma = dict()
            for k in self.matrix.keys():
                l = list()
                for i in range(self.c):
                    l.append(self.matrix[k][i] + m.get_matrix()[k][i])
                soma[k] = l
            sum_matrix = Matrix()
            sum_matrix.set_matrix(soma)
            return sum_matrix
        except:
            raise MatrixError("Matrices dimensions aren't the same")

    def __mul__(self, m):
        '''
        Multiplica duas matrizes com o uso so operador *
        '''
        if self.get_columns() != m.get_rows():
            raise MatrixError("Multiplication is impossible")
        else:
            multiplication = Matrix(self.get_rows(), m.get_columns())

            for i in multiplication.get_matrix().keys():
                for j in range(len(multiplication.get_matrix()[i])):
                    row = self.get_row(i)
                    column = m.get_column(j)
                    res = 0
                    for k in range(len(row)):
                        res += row[k] * column[k]
                        print(row[k], column[k], res)
                    multiplication.set_element(i + 1, j + 1, res)
            
            return multiplication

                
    def scalar_multiplication(self, n):
        '''
        Realiza uma multiplicação por escalar
        '''
        for k in self.matrix.keys():
            for i in range(self.c):
                self.matrix[k][i] *= n

    def get_row(self, l):
        '''
        Retorna uma linha especifica da matriz, indicada pelo indice da mesma
        '''
        try:
            row = list()
            for i in range(len(self.matrix[l])):
                row.append(self.matrix[l][i])

            return row

        except:
            raise MatrixError(f"Row {l} doesn't exists")

    
    def get_column(self, c):
        '''
        Retorna uma coluna especifica da matriz, indicada pelo indice da mesma
        '''
        try:
            column = list()
            for k in self.matrix.keys():
                column.append(self.matrix[k][c])
            return column
        except:
            raise MatrixError(f"Column {c} doesn't exists")

    def set_row(self, row, l):
        '''
        Substitui uma linha indicada da matriz pela nova linha passada
        '''
        self.matrix[l - 1] = row
    
    def set_column(self, column, c):
        '''
        Substitui uma coluna indicada da matriz pela nova coluna passada
        '''
        for i in range(self.l):
            self.matrix[i][c-1] = column[i]

    def get_transpose(self):
        '''
        Retorna a matriz transposta da matriz em questão
        '''
        transpose = dict()
        for i in range(self.c):
            transpose[i] = self.get_column(i)

        m = Matrix()
        m.set_matrix(transpose)
        return m

    def set_element(self, l, c, e):
        '''
        Substitui o elemento indicado na posição (l,c) da matriz pelo novo elemento
        passado
        '''
        try:
            self.matrix.get(l - 1)[c - 1] = e        
        except:
            raise MatrixError(f"Position M({l},{c}) doesn't exist")

    def get_element(self, l, c):
        '''
        Retorna o elemento da posição (l,c) da matriz
        '''
        try:
            return self.matrix.get(l - 1)[c - 1]
        except:
            raise MatrixError(f"Position M({l},{c}) doesn't exist")

    def get_columns(self):
        '''
        Retorna o número de colunas da matriz
        '''
        return self.c

    def get_rows(self):
        '''
        Retorna o número de linhas na matriz
        '''
        return self.l

    def get_matrix(self):
        '''
        Retorna o dicionario que representa internamente a matriz
        '''
        return self.matrix

    def set_matrix(self, d):
        '''
        Importa um dicionario que representa a matriz
        '''
        self.matrix = d
        self.l = len(d.keys())
        self.c = len(d[0])

    def is_square(self):
        '''
        Verifica se a matriz é quadrada
        '''
        if self.c == self.l:
            return True
        return False

    def get_main_diagonal(self):
        '''
        Retorna a diagonal principal
        '''
        if not self.is_square():
            raise MatrixError("This matrix isn't square")    
        
        diagonal = list()
        for i in range(self.c):
            diagonal.append(self.get_element(i + 1, i + 1))

        return diagonal

    def get_secondary_diagonal(self):
        '''
        Retorna a diagonal secundária
        '''
        if not self.is_square():
            raise MatrixError("This matrix isn't square")    
        
        diagonal = list()
        p = self.c - 1
        for i in range(self.l):
            diagonal.append(self.get_element(i + 1, p + 1))
            p -= 1
        return diagonal

    def det(self):
        '''
        Calcula o determinante da matriz
        '''
        if not self.is_square():
            raise MatrixError("This Matrix isn't square")
        
        if self.c == self.l == 2:
            main_diagonal = self.get_main_diagonal()
            secondary_diagonal = self.get_secondary_diagonal()
            return (main_diagonal[0]*main_diagonal[1]) - (secondary_diagonal[0]*secondary_diagonal[1])

        new_matrix = remove_column(self, 1)
        column = self.get_column(1)

        det = 0

        for i in range(len(column)):
            m = remove_row(new_matrix, i + 1)
            det += column[i] * pow(-1, 2 + i) * m.det()

        return det

class LinearSystem:
    '''
    Classe que representa um sistema linear e opera sobre o mesmo
    '''
    def __init__(self, variables, matrix):
        '''
        Construtor que inicializa um sistema linear partindo de uma
        lista de variaveis e a matriz completa que representa o sistema
        '''
        self.variables = variables
        self.matrix = matrix

    def get_solution(self):
        '''
        Calcula as soluções, caso o sistema seja possível e determinado. Caso
        contrário, retorna uma string com a classificação do sistema.
        '''
        incomplete_matrix = remove_column(self.matrix, self.matrix.get_columns())
        result_column = self.matrix.get_column(self.matrix.get_columns() - 1)
        d = incomplete_matrix.det()
        det_variables = list()

        for i in range(len(self.variables)):
            m = remove_column(self.matrix, self.matrix.get_columns())
            m.set_column(result_column, i)
            det_variables.append(m.det())

        if d == 0:
            for e in det_variables:
                if e != 0:
                    return "Impossible System"
            return "Indeterminate System"
        
        solution = dict()

        for i in range(len(det_variables)):
            solution[self.variables[i]] = det_variables[i] / d

        return solution
