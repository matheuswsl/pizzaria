#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 19:17:17 2021

@author: matheus
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from abc import ABC, abstractmethod
from tkinter import messagebox as mb

class LabelBotao(tk.Frame):
    """Define o template para os widgets presentes na interface do usuário."""
    
    def __init__(self, parente, label_info=None, texto_label='', classe_input = None, 
                 input_info = None, variavel = None, **kwargs):
        super().__init__(parente, **kwargs)
        label_info = label_info or {}
        input_info = input_info or {}
        self.variavel = variavel
        if classe_input in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_info['text'] = texto_label
            input_info['variable'] = variavel
        else:
            self.label = ttk.Label(self, text=texto_label, **label_info)
            self.label.grid(row=0, column=0, sticky='ew')
            input_info['textvariable'] = variavel
        self.input = classe_input(self, **input_info)
        self.input.grid(row=1, column=0, sticky='ew')
        
    def grid(self, sticky = 'ew', padx = 10, pady = 5, **kwargs):
        super().grid(sticky = sticky, padx = padx, pady = pady, **kwargs)
        
    def get(self):
        try: 
            if self.variavel:
                return self.variavel.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0',tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError, AttributeError):
            return ''
    
    def set(self, value, *args, **kwargs):
        if type(self.variavel) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variavel:
            self.variavel.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)
    
    def reset(self):
        value = ''
        if type(self.variavel) == tk.BooleanVar:
            self.variable.set(False)
        elif self.variavel:
            self.variavel.set(value)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
        elif type(self.input) == ttk.Button:
            pass
        else:
            self.input.delete(0, tk.END)
                
        
class Aplicacao(tk.Frame):
    """Cria os widgets"""
    
    def __init__(self, parente, *args, **kwargs):
        super().__init__(parente, *args, **kwargs)
        self.widgets = {}
        
    def cria_widgets(self):
        self.widgets['titulo'] = ttk.Label(self, text='Pedido',
                    font=('Helvetica','14','bold','underline'))
        #informações da pizza
        self.widgets['info_pizza'] = ttk.Labelframe(self, 
                    text='Informações da pizza')
        self.widgets['sabor'] = LabelBotao(self.widgets['info_pizza'], 
                    texto_label='Sabor: ', classe_input=ttk.Combobox,
                    variavel = tk.StringVar(), input_info={'width':39,
                    'values':['Mussarela','Calabresa','Portuguesa']})
        self.widgets['tamanho'] = LabelBotao(self.widgets['info_pizza'], 
                    texto_label = 'Tamanho: ', classe_input=ttk.Combobox,
                    variavel = tk.StringVar(), input_info={'width':39,
                    'values':['Pequena','Media','Grande']})
        self.widgets['extras'] = ttk.LabelFrame(self, 
                    text='Extras')
        self.widgets['cebola'] = LabelBotao(self.widgets['extras'], 
                    texto_label='Cebola', classe_input=ttk.Checkbutton,
                    variavel = tk.StringVar(), input_info={'onvalue':'Sim', 
                    'offvalue':'Não'})
        self.widgets['bacon'] = LabelBotao(self.widgets['extras'], 
                    texto_label='Bacon', classe_input=ttk.Checkbutton,
                    variavel = tk.StringVar(), input_info={'onvalue':'Sim', 
                    'offvalue':'Não'})
        self.widgets['catupiry'] = LabelBotao(self.widgets['extras'], 
                    texto_label='Catupiry', classe_input=ttk.Checkbutton,
                    variavel = tk.StringVar(), input_info={'onvalue':'Sim', 
                    'offvalue':'Não'})
        #Informações Cliente
        self.widgets['info_cliente'] = ttk.LabelFrame(self, 
                    text='Informações do cliente')
        self.widgets['nome'] = LabelBotao(self.widgets['info_cliente'],
                    texto_label='Nome: ', classe_input=ttk.Entry,
                    variavel=tk.StringVar(), input_info = {'width':40})
        self.widgets['endereco'] = LabelBotao(self.widgets['info_cliente'],
                    texto_label='Endereço: ', classe_input=ttk.Entry,
                    variavel=tk.StringVar(), input_info = {'width':40})
        self.widgets['pagamento'] = LabelBotao(self.widgets['info_cliente'],
                    texto_label='Forma de Pagamento: ', classe_input=ttk.Combobox,
                    variavel=tk.StringVar(), input_info={'width':39,
                    'values':['Cartão','Dinheiro']})
        self.widgets['total'] = LabelBotao(self.widgets['info_cliente'], 
                    texto_label='Total:', classe_input=tk.Label,
                    variavel=tk.StringVar(), input_info={'bg':'white',
                    'width':40})
        self.widgets['calcula_total'] = LabelBotao(self.widgets['info_cliente'],
                    texto_label='Calcular Total', classe_input=ttk.Button,
                    input_info={'command':
                    (lambda: CalculaTotal(self.widgets).calcula_total())})
        #Informações adicionais
        self.widgets['info_adicionais'] = ttk.Labelframe(self, 
                    text='Informações adicionais')
        self.widgets['informacoes'] = LabelBotao(self.widgets['info_adicionais'],
                    classe_input=tk.Text, input_info={'width':40, 'height':3})
        #Botões
        self.widgets['botoes'] = ttk.Frame(self)
        self.widgets['limpar'] = LabelBotao(self.widgets['botoes'], 
                    classe_input=ttk.Button, texto_label='Limpar',
                    input_info={'command':
                    (lambda: LimpaFormulario(self.widgets).limpa()),
                    'width':17})
        self.widgets['visualizar'] = LabelBotao(self.widgets['botoes'], 
                    texto_label='Visualizar pedido', classe_input=ttk.Button,
                    input_info={'command':
                    (lambda: ComandoVisualizar(self.widgets).monta_impressao()),
                    'width':17})
    
    def grid(self, sticky = 'ew', **kwargs):
        super().grid(sticky = sticky, **kwargs)
        self.widgets['titulo'].grid(row=0,column=0, pady = 10)
        #Informações da pizza
        self.widgets['info_pizza'].grid(row=1,column=0, sticky='ew',
                    padx = 10, pady = 5)
        self.widgets['sabor'].grid(row=0,column=0)
        self.widgets['tamanho'].grid(row=1,column=0)
        self.widgets['extras'].grid(row=2,column=0, sticky='ew',
                    padx=10, pady=10, in_=self.widgets['info_pizza'])
        self.widgets['cebola'].grid(row=0,column=0)
        self.widgets['bacon'].grid(row=0,column=1)
        self.widgets['catupiry'].grid(row=0,column=2)
        #Informações do Cliente
        self.widgets['info_cliente'].grid(row=2,column=0, sticky='ew', padx=10,
                    pady=5)
        self.widgets['nome'].grid(row=0, column=0)
        self.widgets['endereco'].grid(row=1, column=0)
        self.widgets['pagamento'].grid(row=3,column=0)
        self.widgets['total'].grid(row=4,column=0)
        self.widgets['calcula_total'].grid(row=5,column=0,sticky='ns')
        #Informações adicionais
        self.widgets['info_adicionais'].grid(row=3,column=0, sticky='ew',
                    padx=10,pady=5)
        self.widgets['informacoes'].grid(row=0,column=0, sticky = 'ew', 
                    padx=10, pady=5)
        #Botões
        self.widgets['botoes'].grid(row=4,column=0,sticky='ew', pady=10)
        self.widgets['limpar'].grid(row=0,column=0, padx=20, pady=10)
        self.widgets['visualizar'].grid(row=0,column=1, pady=10)
    
class ComandoVisualizar:
    """Prepara os inputs para serem imprimidos"""
    
    def __init__(self, widgets):
        self.widgets = widgets
         
    def recupera_valores(self):
        w = self.widgets
        valores={}          
        for chave, valor in w.items():
            if type(w[chave]) not in (ttk.Label,ttk.LabelFrame, ttk.Frame):
                valores[chave] = w[chave].get()
        valores['informacoes'] = w['informacoes'].get()
        for chave in ('cebola','bacon','catupiry'):
            if valores[chave] == '':
                valores[chave] = 'Não'
        return valores
        
    def monta_impressao(self):
        valores = self.recupera_valores()
        impressao = """Pedido:
                    \n********
                    \nNome do Cliente: %s
                    \nEndereço: %s
                    \n********
                    \nPizza:
                    \n_______
                    \nSabor: %s
                    \nTamanho: %s
                    \nCom os adicionais:
                    \n\t-Cebola: %s
                    \n\t-Bacon: %s
                    \n\t-Catupiry: %s 
                    \n********
                    \nTOTAL: %s
                    \nForma de pagamento: %s
                    \n********
                    \nInformações adicionais:
                    \n%s"""%(valores['nome'], valores['endereco'], 
                    valores['sabor'],valores['tamanho'],valores['cebola'],
                    valores['bacon'],valores['catupiry'], valores['total'],
                    valores['pagamento'], valores['informacoes'])
        Visualiza(impressao).visualizar()
        
class Visualiza:
    
    def __init__(self, impressao):
        self.impressao = impressao
        
    def visualizar(self):
        janela = tk.Toplevel()
        janela.geometry('350x450')
        pedido = scrolledtext.ScrolledText(janela, width=40, height = 25)
        pedido.insert('1.0',self.impressao)
        pedido.grid(row=0,column=0,padx=10,pady=10)
        
class Pizza(ABC):
    
    def __init__(self):
        self.total = None
        
    @abstractmethod
    def custo(self):
        pass
    
class Mussarela(Pizza):
    
    def custo(self):
        return 19.00
    
class Calabresa(Pizza):
    
    def custo(self):
        return 24.90
    
class Portuguesa(Pizza):
    
    def custo(self):
        return 28.50
    
class Extras(Pizza):
    
    def __init__(self, pizza):
        self.pizza = pizza
        
    def custo(self):
        pass

class Cebola(Extras):
    
    def custo(self):
        return 2.00 + self.pizza.custo()

class Bacon(Extras):
    
    def custo(self):
        return 3.00 + self.pizza.custo()
        
class Catupiry(Extras):
    
    def custo(self):
        return 3.50 + self.pizza.custo()
        
class Tamanho(Pizza):
    
    def __init__(self, pizza):
        self.pizza = pizza
    
    def custo(self):
        pass
    
class Grande(Tamanho):
    
    def custo(self):
        return 1.5 * self.pizza.custo()
        
class Media(Tamanho):
    
    def custo(self):
        return self.pizza.custo()
    
class Pequena(Tamanho):
    
    def custo(self):
        return 0.7 * self.pizza.custo()
    
class SeparaExtras:
    """Cria um dicionário contendo apenas os ingrdientes extras""" 
    def __init__(self, widgets):
        self.widgets = widgets
    
    def separa(self):
        w = self.widgets
        extras = []
        for chave in ('cebola','bacon','catupiry'):
            if w[chave].get() == 'Sim':
                extras.append(chave)
        return extras                
        
class CalculaTotal:
    """Calcula o valor total"""
    
    def __init__(self, widgets):
        self.widgets = widgets
    
    def formata(self, total):
        total = 'R$ %.2f'%(total)
        self.widgets['total'].set(total.replace('.',','))

    def calcula_total(self):
        w = self.widgets
        if FazVerificacao(w).verifica_sabor():
            comando = ''
            extras = SeparaExtras(w).separa()
            for ingrediente in extras:
                comando = comando + ingrediente.title() + '('
            comando = (comando + w['tamanho'].get() + '(' + w['sabor'].get() 
                + '()' + (len(extras) + 1) * ')' + '.custo()')
            self.formata(eval(comando))
                
class FazVerificacao:
    
    def __init__(self, entrada):
        self.entrada = entrada
    
    def verifica_sabor(self):
        """Verifica se foi associado algum sabor de pizza"""
        if self.entrada['sabor'].get():
            return True
        else:
            mb.showerror(title='Pizzaria do Luigi', 
                message='Por favor, escolha um sabor de pizza')
            
class LimpaFormulario:
    
    def __init__(self, widgets):
        self.widgets = widgets
        
    def limpa(self):
        for chave, valor in self.widgets.items():
            if type(self.widgets[chave]) not in (ttk.LabelFrame, ttk.Label,
                   ttk.Frame):
                self.widgets[chave].reset()
    
janela = tk.Tk()
janela.title('Pizzaria do Luigi')
janela.geometry('370x700')
janela.resizable(False,False)

app = Aplicacao(janela)
app.cria_widgets()
app.grid(row=0,column=0)


janela.mainloop()
        
        