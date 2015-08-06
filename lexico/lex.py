"""
    Compiladores
    Junho de 2015 
    Leandro Souza da Silva 23418 
    Analisador Lexico gerado com Lex python
"""
import ply.lex as lex
import random
import os, sys

class ObjectTable(object):

    symbol = ''
    token  = ''
    Dtype  = 'NO'
    init   = 'NO'

class MyLexer(object):

    file_name_input        = 'input_dada.txt'
    file_name_scanner       = 'output_scanner.txt' 
    file_name_symbol_table = 'output_symbol_table'

    output_scanner = []
    output_symbol = []
    input_data = ''
    symbol_table = {}

    reserved = {
        'algoritmo'     :    'pr_algoritmo',
        'Inicio'        :    'pr_inicio',
        'fim_algoritmo' :    'pr_fim_algo',
        'LOGICO'        :    'pr_logico',
        'INTEIRO'       :    'pr_inteiro',
        'REAL'          :    'pr_real',
        'CARACTER'      :    'pr_caracter',
        'REGISTRO'      :    'pr_registro',
        'leia'          :    'pr_leia',
        'escreva'       :    'pr_escreva',
        'se'            :    'pr_se',
        'entao'         :    'pr_entao',
        'senao'         :    'pr_senao',
        'fim_se'        :    'pr_fim_se',
        'para'          :    'pr_para',
        'ate'           :    'pr_ate',
        'passo'         :    'pr_passo',
        'faca'          :    'pr_faca',
        'fim_para'      :    'pr_fim_para',
        'enquanto'      :    'pr_enqto',
        'fim_enquanto'  :    'pr_fim_enqto',
        'repita'        :    'pr_repita',
        'ABS'           :    'pr_abs',
        'TRUNCA'        :    'pr_trunca',
        'RESTO'         :    'pr_resto',
        'declare'       :    'pr_declare',
    }

    # List of token names.   This is always required
    tokens = [
       'ponto',
       'virgula',
       'ponto_virgula',
       'dois_pontos',
       'abre_col',
       'fecha_col',
       'abre_par',
       'fecha_par',
       'aspas',
       'identificador',
       'num_inteiro',
       'num_real',
       'const_list',
       'op_arit_mult',
       'op_arit_div',
       'op_arit_adi',
       'op_ari_sub',
       'op_atrib',
       'op_rel_igual',
       'op_rel_naoigual',
       'op_rel_maior',
       'op_rel_maiorigual',
       'op_rel_menor',
       'op_rel_menorigual',
       'op_log_nao',
       'op_log_and',
       'op_log_or',
    ] +  list(reserved.values()) 

    # Regular expression rules for simple tokens
    t_ponto               = r'\.'
    t_virgula             = r'\,'
    t_ponto_virgula       = r';'
    t_dois_pontos         = r':'
    t_abre_col            = r'\['
    t_fecha_col           = r'\]'
    t_abre_par            = r'\('
    t_fecha_par           = r'\)'
    t_aspas               = r'"'
    t_num_inteiro         = r'\d+'
    t_num_real            = r'\d+\,\d+'
    t_const_list          = r'"(.*?)"'
    t_op_arit_mult        = r'\*'
    t_op_arit_div         = r'\/'
    t_op_arit_adi         = r'\+'
    t_op_ari_sub          = r'-'
    t_op_atrib            = r'='
    t_op_rel_igual        = r'=='
    t_op_rel_naoigual     = r'!='
    t_op_rel_maior        = r'>'
    t_op_rel_maiorigual   = r'>='
    t_op_rel_menor        = r'<'
    t_op_rel_menorigual   = r'<='
    t_op_log_nao          = r'!'
    t_op_log_and          = r'&&'
    t_op_log_or           = r'\|\|'
    t_pr_algoritmo        = r'algoritmo'
    t_pr_inicio           = r'Inicio'
    t_pr_fim_algo         = r'fim_algoritmo'
    t_pr_logico           = r'LOGICO'
    t_pr_inteiro          = r'INTEIRO' 
    t_pr_real             = r'REAL'
    t_pr_caracter         = r'CARACTER'
    t_pr_registro         = r'REGISTRO'
    t_pr_leia             = r'leia'
    t_pr_escreva          = r'escreva'
    t_pr_se               = r'se'
    t_pr_entao            = r'entao'
    t_pr_senao            = r'senao'
    t_pr_fim_se           = r'fim_se'
    t_pr_para             = r'para'
    t_pr_ate              = r'ate'
    t_pr_passo            = r'passo'
    t_pr_faca             = r'faca'
    t_pr_fim_para         = r'fim_para'
    t_pr_enqto            = r'enquanto'
    t_pr_fim_enqto        = r'fim_enquanto'
    t_pr_repita           = r'repita'
    t_pr_abs              = r'ABS'
    t_pr_trunca           = r'TRUNCA'
    t_pr_resto            = r'RESTO'
    t_pr_declare          = r'declare'


    #build file with random patterns
    def build_random_file(self):

        letter = [ chr(let) for let in range(ord('A'), ord('A')+26) ] + \
                 [ chr(let) for let in range(ord('a'), ord('a')+26) ]

        number = [str(n) for n in range (0, 10)]

        all_letters =  letter + number


        patterns = [ '.', ',', ';', ':', '[', ']', '(', ')', '"', '*', '/', '+','-',
                  '=', '==', '!=', '>', '>=', '<=', '!', '&&', '||', 'algoritmo',
                  'Inicio', 'fim_algoritmo', 'LOGICO', 'INTEIRO', 'REAL', 'CARACTER',
                  'REGISTRO', 'leia', 'escreva', 'se', 'entao', 'senao', 'fim_se',
                  'para', 'ate', 'passo', 'faca', 'fim_para', 'enquanto', 'fim_enquanto',
                  'repita', 'ABS', 'TRUNCA', 'RESTO', 'declare', '\n', '\n', '\n', '\n',
        ]

        strings = []
        for i in range (50):
            strings.append('"'+''.join(random.sample([random.choice(all_letters) for i in range(10) ], 3)) + '"')
        for i in range (50):
            strings.append(''.join(random.sample([random.choice(all_letters) for i in range(10) ], 5)))

        all_patterns = patterns + strings + number + letter
        data = []
        size_data = int(sys.argv[1]) if (len(sys.argv) == 2) else 50
        for i in range (size_data):
            data.append(str(random.choice(all_patterns)))
            data.append(' ') 
        #random.shuffle(data)
        s_file = ''.join(data)
        print "Data: ", s_file
        file_patterns = open(self.file_name_input, 'w')
        file_patterns.write(s_file)
        file_patterns.close()

    #read file input
    def read_file(self):

        f = open(self.file_name_input, 'r')
        self.input_data = f.read()
        f.close()

    def get_output_scanner(self):
        return self.output_scanner

    def get_output_symbol(self):
        return self.output_symbol

    def get_input_data(self):
        return self.input_data

    # insert symbol into symbol_table
    def insert_symbol(self, symbol, token):

        if not symbol in self.symbol_table:
            obj = ObjectTable()
            obj.symbol = symbol
            obj.token = token
            self.symbol_table[symbol] = obj
            return True
        return False

    # get symbol in symbol_table
    def get_symbol(self, symbol):

        if symbol in self.symbol_table:
            return self.symbol_table[symbol]
        return None

    # update  symbol_table
    def update_symbol(self, symbol, data):

        if symbol in self.symbol_table:
            self.symbol_table[symbol].token = data.token
            self.symbol_table[symbol].Dtype = data.Dtype
            self.symbol_table[symbol].init  = data.init

            return True

        return False

    # get symbol_table
    def get_symbol_table(self):
        return self.symbol_table

    def t_identificador(self,t):
        
        r'([A-Za-z]([0-9]|[A-Za-z_]){1,30})'
        if not self.reserved.get(t.value): 
            self.insert_symbol(t.value,  'identificador')
        t.type = self.reserved.get(t.value, 'identificador') 
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character (%s, %s, %s)" % (t.value[0], t.lineno, t.lexpos))
        self.output_scanner.append('{:>20} {:>20}  {:>20}  {:>20} {:>20} '.format (
                                    'invalid character',
                                    'No type',  str(t.value[0]),
                                    str(t.lineno),str(t.lexpos) )
                                  )
        self.output_scanner.append('\n')
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):

        self.lexer = lex.lex(module=self, **kwargs)
    
    # Test it output
    def run(self,data):
        
        self.lexer.input(data)
        self.symbol_table = {}
        
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)
             self.output_scanner.append('{:>20} {:>20}  {:>20}  {:>20} {:>20} '.format (
                                         'valid character',
                                         str(tok.type),  str(tok.value),
                                         str(tok.lineno),str(tok.lexpos) )
                                        )

             self.output_scanner.append('\n')
        table = self.get_symbol_table()
        for key in table:
            self.output_symbol.append('{:>20} {:>20} {:>20}  {:>20}'.format(
                                         table[key].symbol, table[key].token, 
                                         table[key].Dtype , table[key].init
                                         ) + '\n' 
                                    )

    def save_files(self, data_input, data_scan, data_symbol):
        
        f_scan    =  open(self.file_name_scanner, 'w')
        f_tab_sym =  open(self.file_name_symbol_table, 'w')

        f_scan.write('Input Data: \n\n' + data_input +'\n\n' + 'Lexical Analyzer' + '\n\n')
        f_scan.write('{:>20} {:>20} {:>20}  {:>20} {:>20} '.format('status', 
                     'type', 'value', 'line_num', 'pos' ) + '\n\n')
        f_scan.write(''.join(self.output_scanner))

        f_tab_sym.write("Symbol Table " + '\n\n')
        f_tab_sym.write('{:>20} {:>20} {:>20}  {:>20}'.format('symbol', 'token', 'Dtype', 'init') + '\n\n')
        f_tab_sym.write(''.join(self.output_symbol))

        f_scan.close()
        f_tab_sym.close()

        self.output_scanner = []
        self.output_symbol = []

def main():

    m = MyLexer()
    m.build_random_file()
    m.build()
    m.read_file()          
    data = m.get_input_data()
    m.run(data)
    m.save_files(data, m.get_output_scanner() , m.get_output_symbol())

if __name__ == '__main__':
    main()