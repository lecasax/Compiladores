"""
    Compiladores
    Junho de 2015
    Leandro Souza da Silva 23418
    Analisador Lexico gerado com Lex python
"""

"""
Observacao... o simbolo # corresponde a opreacao de radiciacao.

"""
import sys
sys.path.insert(0,"../..")

import ply.lex as lex
import ply.yacc as yacc
import random
import os, sys

class ObjectTable(object):

    symbol = ''
    token  = ''
    Dtype  = 'NO'
    init   = 'NO'


class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    file_name_input         = 'input_dada.txt'
    file_name_scanner       = 'output_scanner.txt'
    file_name_symbol_table  = 'output_symbol_table'

    output_scanner = []
    output_symbol = []
    input_data = ''
    symbol_table = {}

    identificador_names = []

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=True,
                  #debugfile=self.debugfile,
                  #tabmodule=self.tabmodule)
                )
    def run(self):
        while 1:
            try:
                s = raw_input('Put your file > ')
                pt_file = open(s, 'r')
                s = pt_file.read()
                pt_file.close()
            except Exception, e:
                exit()
            if not s: continue
            yacc.parse(s)
            self.save_files()

    def save_files(self):

        table = self.get_symbol_table()
        for key in table:
            self.output_symbol.append('{:>20} {:>20} {:>20}  {:>20}'.format(
                                     table[key].symbol, table[key].token,
                                     table[key].Dtype , table[key].init
                                     ) + '\n'
                                )

        f_scan    =  open(self.file_name_scanner, 'w')
        f_tab_sym =  open(self.file_name_symbol_table, 'w')

        f_scan.write('Lexical Analyzer Error' + '\n\n')
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
        self.symbol_table = {}


class Sintatic(Parser):


    reserved = {
         #Value                       #Type
        'algoritmo'         :    'pr_algoritmo',
        'Inicio'            :    'pr_inicio',
        'fim_algoritmo'     :    'pr_fim_algo',
        'LOGICO'            :    'pr_logico',
        'INTEIRO'           :    'pr_inteiro',
        'REAL'              :    'pr_real',
        'CARACTER'          :    'pr_caracter',
        'REGISTRO'          :    'pr_registro',
        'STRUCT'            :    'pr_struct',
        'leia'              :    'pr_leia',
        'escreva'           :    'pr_escreva',
        'se'                :    'pr_se',
        'entao'             :    'pr_entao',
        'senao'             :    'pr_senao',
        'fim_se'            :    'pr_fim_se',
        'para'              :    'pr_para',
        'ate'               :    'pr_ate',
        'passo'             :    'pr_passo',
        'faca'              :    'pr_faca',
        'fim_para'          :    'pr_fim_para',
        'enquanto'          :    'pr_enqto',
        'fim_enquanto'      :    'pr_fim_enqto',
        'repita'            :    'pr_repita',
        'ABS'               :    'pr_abs',
        'TRUNCA'            :    'pr_trunca',
        'RESTO'             :    'pr_resto',
        'Declare'           :    'pr_declare',
        'Entrada'           :    'pr_entrada',
        'Saida'             :    'pr_saida',
        'Funcao'            :    'pr_funcao',
        'Procedimento'      :    'pr_procmto',
        'fim_funcao'        :    'pr_fim_funcao',
        'fim_procedimento'  :    'pr_fim_procmto',

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
       'op_arit_sub',
       'op_arit_expo',
       'op_arit_rad',
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
    t_op_arit_sub         = r'-'
    t_op_arit_expo        = r'\^'
    t_op_arit_rad         = r'\#'
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
    t_pr_declare          = r'Declare'
    t_pr_entrada          = r'Entrada'
    t_pr_saida            = r'Saida'
    t_pr_funcao           = r'Funcao'
    t_pr_procmto          = r'Procedimento'
    t_pr_fim_funcao       = r'fim_funcao'
    t_pr_fim_procmto      = r'fim_procedimento'


    #def get_output_scanner(self):
    #    return self.output_scanner

    #def get_output_symbol(self):
    #    return self.output_symbol

    #def get_input_data(self):
    #    return self.input_data

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
    """def get_symbol(self, symbol):

        if symbol in self.symbol_table:
            return self.symbol_table[symbol]
        return None
    """

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

        #r'[a-zA-Z_][a-zA-Z0-9_]*'
        r'([a-zA-Z]([0-9]|[A-Za-z_]){1,30})'
        if not self.reserved.get(t.value):
            self.insert_symbol(t.value,  'identificador')
            pass
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

    # Parsing rules

    def p_algo(self, p):
        '''algo : pr_algoritmo identificador procs pr_inicio decl cmds pr_fim_algo'''
        obj = ObjectTable()
        obj.token = 'identificador'
        obj.Dtype = p[1]
        obj.symbol = p[2]
        self.update_symbol(p[2], obj)

    def p_decl (self, p):
        '''decl : pr_declare l_ids dois_pontos tipo ponto_virgula decl
                | pr_declare l_ids dois_pontos tipo_registro ponto_virgula decl
                | empty
        '''
        if (len(p) == 7):
            pass
            obj = ObjectTable()
            obj.symbol = p[2]
            obj.token = 'identificador'
            obj.Dtype = p[4]
            self.update_symbol(p[2], obj)

    def p_l_ids(self, p):
        '''l_ids : identificador comp lids'''
        self.identificador_names.append(p[1])
        p[0] = p[1]

    def p_lids(self, p):
        '''lids : virgula l_ids
                | empty
        '''
        p[0] = p[1]

    def p_comp(self, p):
        '''comp : abre_col dim fecha_col
                | empty
        '''

    def p_dim(self, p):
        '''dim : num_inteiro ponto ponto  dims'''

    def p_dims(self, p):
        '''dims : virgula dim
                | empty
        '''

    def p_tipo(self, p):
        # para definir o registro foi preciso fazer a alteracao
        # na ultima linha.
        '''tipo : pr_logico
                | pr_caracter
                | pr_inteiro
                | pr_real
                | identificador
        '''
        #Para retornar o estado apra a  funcao que o chama
        p[0] = p[1]
        for symbol in self.identificador_names:
            obj = ObjectTable()
            obj.symbol = symbol
            obj.init = 'NO'
            obj.token = 'identificador'
            obj.Dtype = p[1]
            self.update_symbol(symbol, obj)
        self.identificador_names = []

    def p_tipo_registro(self, p):
        '''tipo_registro : pr_registro abre_par decl fecha_par'''
        p[0] = p[1]

    def p_struct(self, p):
        '''struct : pr_struct'''

    def p_reg(self, p):
        '''reg : pr_registro abre_par decl fecha_par'''
        p[0] = p[1]

    def p_registro(self, p):
        '''registro : pr_registro abre_par decl fecha_par'''
        p[0] = p[1]

    def p_cmds(self, p):
        '''cmds : pr_leia l_var cmds
                | pr_escreva l_esc cmds
                | identificador op_atrib exp cmds
                | pr_se cond pr_entao cmds sen pr_fim_se cmds
                | pr_para identificador op_atrib num_inteiro pr_ate num_inteiro pr_passo\
                num_inteiro pr_faca cmds pr_fim_para cmds
                | pr_para identificador op_atrib identificador pr_ate identificador pr_passo\
                identificador pr_faca cmds pr_fim_para cmds
                | pr_enqto cond cmds pr_fim_enqto cmds
                | identificador abre_par l_var fecha_par cmds
                | empty
        '''

    def p_l_var(self, p):
        '''l_var : var l_vrs'''
        p[0] = p[1]

    def p_l_vrs(self, p):
        '''l_vrs : virgula var
                 | empty
        '''

    def p_var(self, p):
        '''var : identificador ind'''
        p[0] = p[1]

    def p_ind(self, p):
        '''ind : abre_col num_inteiro fecha_col ind
               | ponto identificador ind
               | empty
        '''

    def p_l_esc(self, p):
        '''l_esc : const_list l_escs
                 | var l_escs
        '''
    def p_l_escs(self, p):
        '''l_escs : virgula l_esc
                  | empty
        '''

    def p_sen(self, p):
        '''sen : pr_senao cmds
               | empty
        '''


    def p_procs(self, p):
        '''procs : pr_procmto identificador pr_entrada l_var pr_saida l_var \
                   decl cmds pr_fim_funcao
                 | pr_procmto identificador pr_entrada l_var decl cmds pr_fim_procmto
        '''
        if (len(p) >= 7):
            obj = ObjectTable()
            obj.symbol = p[2]
            obj.token = 'identificador'
            obj.Dtype = p[1]
            self.update_symbol(p[2], obj)

        p[0] = p[1]

    def p_exp(self, p):
        '''exp : exp_l
               | exp_a
        '''

    def p_exp_a(self, p):
        '''exp_a : term_a muldiv exp_a
                 | term_a
        '''

    def p_term_a(self, p):
        '''term_a : fat_a adisub term_a
                  | fat_a
        '''

    def p_fat_a(self, p):
        '''fat_a : exp_a op_arit_expo exp_a
                 | exp_a op_arit_rad exp_a
                 | abre_par exp_a fecha_par
                 | func abre_par l_var fecha_par
                 | var
                 | num_inteiro
                 | num_real
        '''

    def p_muldiv(self, p):
        '''muldiv : op_arit_mult
                  | op_arit_div
        '''
    def p_adisub(self, p):
        '''adisub : op_arit_adi
                  | op_arit_sub
        '''

    def p_func(self, p):
        '''func : pr_abs
                | pr_trunca
                | pr_resto
        '''

    def p_exp_l(self, p):
        '''exp_l : rel op_log exp_l
                 | op_log_nao abre_par rel fecha_par
                 | rel
        '''

    def p_rel(self, p):
        '''rel : fat_r op_rel fat_r
        '''

    def p_fat_r(self, p):
        '''fat_r : fat_a
                  | const_list
        '''

    def p_op_log(self, p):
        '''op_log : op_log_and
                  | op_log_or
        '''

    def p_op_rel(self, p):
        '''op_rel : op_rel_igual
                  | op_rel_naoigual
                  | op_rel_maior
                  | op_rel_maiorigual
                  | op_rel_menor
                  | op_rel_menorigual
        '''

    def p_cond(self, p):
        '''cond : abre_par exp_l fecha_par'''

    def p_empty(self, p):
        'empty : '

    def p_error(self, p):
        print "Syntax error at '%s'" % p


def main():

    sintatic = Sintatic()
    sintatic.run()

if __name__ == '__main__':
    main()