import tkinter as tk
import connection as cn
import psycopg2
from ttkbootstrap import Style

class PrincipalBD:

    def __init__(self, win):

        self.objBD = cn.AppBD()

        style = Style("morph")
        style.theme_use("morph")
        style.configure("TLabel", font="Arial 12", padding=10)
        style.configure("TButton", font="Arial 12", padding=10)

        self.lbCodigo = tk.Label(win, text = 'Código do Produto:')
        self.lblNome = tk.Label(win, text = 'Nome do Produto')
        self.lblPreco = tk.Label(win, text = 'Preço')

        self.txtCodigo = tk.Entry(bd = 3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()

        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=lambda: self.fCadastrarProduto(win))
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.abrirTelaAtualizacao)
        self.btnExcluir = tk.Button(win, text = 'Excluir', command = self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text = 'Limpar', command = self.fLimparTela)
        self.btnSelecionar = tk.Button(win, text = 'Selecionar', command = self.fabrirTelaSelect)

        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)
        self.lblNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)
        self.lblPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)
        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
        self.btnSelecionar.place(x=500, y=200)

    def fabrirTelaSelect(self):

        janela_select = tk.Toplevel()
        janela_select.title('Consulta de Produtos')

        lblCodigoSelect = tk.Label(janela_select, text='Código do Produto:')
        txtCodigoSelect = tk.Entry(janela_select, bd=3)
        btnSelect = tk.Button(janela_select, text='Pesquisar', command=lambda: self.fSelecionarProduto(janela_select, txtCodigoSelect.get()))

        lblCodigoSelect.grid(row=0, column=0)
        txtCodigoSelect.grid(row=0, column=1)
        btnSelect.grid(row=1, column=0)

    def abrirTelaAtualizacao(self):

        janela_atualizacao = tk.Toplevel()
        janela_atualizacao.title('Atualização de Produtos')

        
        lblCodigoAtualizacao = tk.Label(janela_atualizacao, text='Código do Produto:')
        txtCodigoAtualizacao = tk.Entry(janela_atualizacao, bd=3)
        lblNomeAtualizacao = tk.Label(janela_atualizacao, text='Novo Nome do Produto:')
        txtNomeAtualizacao = tk.Entry(janela_atualizacao)
        lblPrecoAtualizacao = tk.Label(janela_atualizacao, text='Novo Preço:')
        txtPrecoAtualizacao = tk.Entry(janela_atualizacao)
        btnAtualizar = tk.Button(janela_atualizacao, text='Atualizar', command=lambda: self.atualizarDados(janela_atualizacao, txtCodigoAtualizacao.get(), txtNomeAtualizacao.get(), txtPrecoAtualizacao.get()))

        lblCodigoAtualizacao.grid(row=0, column=0)
        txtCodigoAtualizacao.grid(row=0, column=1)
        lblNomeAtualizacao.grid(row=1, column=0)
        txtNomeAtualizacao.grid(row=1, column=1)
        lblPrecoAtualizacao.grid(row=2, column=0)
        txtPrecoAtualizacao.grid(row=2, column=1)
        btnAtualizar.grid(row=3, column=1)

   
    def fCadastrarProduto(self, win):

        try:

            codigo, nome, preco = self.fLerCampos()
            preco_acrescido = preco * 1.10

            self.lblPrecoAcrescido = tk.Label(win, text=f"Preço acrescido: {preco_acrescido}")
            self.lblPrecoAcrescido.place(x=100, y=250)

            self.objBD.inserirDados(codigo, nome, preco_acrescido)
            self.fLimparTela()
            print('Produto Cadastrado com Sucesso!')

        except Exception as e:

            print('Não foi possível fazer o cadastro:', e)

    def atualizarPrecoAcrescido(self, event, win):

        try:

            # Obtendo o valor do preço informado pelo usuário
            preco = float(self.txtPreco.get())

            # Calculando o novo preço acrescido
            preco_acrescido = preco * 1.10

            # Atualizando o valor do preço acrescido na label
            self.lblPrecoAcrescido.config(text=f"Preço acrescido: {preco_acrescido}")

        except Exception as e:

            print('Erro ao atualizar preço acrescido:', e)



    def inserirDados(self, codigo, nome, preco_acrescido):
        
        try:

            self.objBD.abrirConexao()
            cursor = self.objBD.connection.cursor()

            postgres_insert_query = """ INSERT INTO public."produto"
                ("codigo", "nome", "preco") VALUES (%s,%s,%s)"""
            record_to_insert = (codigo, nome, preco_acrescido)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.objBD.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com sucesso na tabela PRODUTO")

        except (Exception, psycopg2.Error) as error:

            if self.objBD.connection:
                print("Falha ao inserir registro na tabela PRODUTO", error)

        finally:

            if self.objBD.connection:
                cursor.close()
                self.objBD.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def fLimparTela(self):

        try:

            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print('Campos Limpos!')

        except:

            print('Não foi possível limpar os campos.')

    def fAtualizarProduto(self):

        try:

            codigo, nome, preco = self.fLerCampos()
            preco_acrescido = preco * 1.10
            self.objBD.atualizarDados(codigo, nome, preco)
            self.fLimparTela()
            print('Produto Atualizado com Sucesso!')

        except:
        
            print('Não foi possível fazer a atualização.')

    def atualizarDados(self, janela_atualizacao, codigo, nome, preco):

        try:

            self.objBD.atualizarDados(codigo, nome, preco)

            janela_atualizacao.destroy()

            print('Produto Atualizado com Sucesso!')

        except Exception as e:

            print(f'Não foi possível fazer a atualização: {e}')



    def fExcluirProduto(self):

        try:

            codigo, _, _ = self.fLerCampos()
            
           
            self.abrirTelaAtualizacao(codigo)


            print('Produto Excluído com Sucesso!')

        except Exception as e:

            print(f'Não foi possível fazer a exclusão: {e}')

        
    def excluirDados(self, codigo):

        try:

            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_delete_query = """DELETE FROM public. "PRODUTO" where "CODIGO" = %s"""
            cursor.execute(sql_delete_query, (codigo,))
            self.connection.commit()
            count = cursor.rowcount
            print (count, "Registro excluído com sucesso na tabela PRODUTO")

        except:

            print("Falha ao excluir registro na tabela PRODUTO")

        finally:

            if(self.connection):

                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def fLerCampos(self):

        codigo = int(self.txtCodigo.get())
        nome = self.txtNome.get()
        preco = float(self.txtPreco.get())
            
        return codigo, nome, preco

    def fLerProdutos(self, codigo):

        try:

            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_select_query = """SELECT FROM public. "produto" WHERE "codigo" = %s"""
            cursor.execute(sql_select_query, (self.txtCodigo.get(),))
            rows = cursor.fetchall()
            print(rows)

            for row in rows:
                print(row)

        except (Exception, psycopg2.Error) as error:

            print("Falha ao ler registro na tabela PRODUTO", error)

    def fSelecionarProduto(self, janela_select, codigo):

        try:

            codigo = int(codigo)
            resultado = self.objBD.consultarProduto(codigo)

            if resultado:

                lblResultado = tk.Label(janela_select, text=f"Nome: {resultado['nome']}, Preço: {resultado['preco']}")
                lblResultado.grid(row=2, column=0, columnspan=2)

            else:

                lblResultado = tk.Label(janela_select, text="Produto não encontrado.")
                lblResultado.grid(row=2, column=0, columnspan=2)

        except ValueError:

            lblResultado = tk.Label(janela_select, text="Código inválido.")
            lblResultado.grid(row=2, column=0, columnspan=2)


janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title("Sistema de Cadastro")
janela.geometry("600x500")
janela.mainloop()