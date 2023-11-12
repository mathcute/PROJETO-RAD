import psycopg2

class AppBD:

    def __init__(self):

        print("Método construtor")

    def abrirConexao(self):

        try:

            self.connection = psycopg2.connect(user = "postgres", password = "Mt1790AA@1",
                                               host = "localhost", port = "5432",
                                               database = "produtos")
            
        except (Exception, psycopg2.Error) as error:

            if(self.connection):

                print("Erro ao conectar ao Banco de Dados PostgreSQL", error)
    def inserirDados(self, codigo, nome, preco_acrescido):

        try:

            self.abrirConexao()
            cursor = self.connection.cursor()

            postgres_insert_query = """ INSERT INTO public."produto"
                ("codigo", "nome", "preco") VALUES (%s,%s,%s)"""
            record_to_insert = (codigo, nome, preco_acrescido)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com sucesso na tabela PRODUTO")

        except (Exception, psycopg2.Error) as error:

            if self.connection:

                print("Falha ao inserir registro na tabela PRODUTO", error)

        finally:

            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def excluirDados(self, codigo):
        
        try:

            self.abrirConexao()
            cursor = self.connection.cursor()
            sql_delete_query = """DELETE FROM public."produto" WHERE "codigo" = %s"""
            cursor.execute(sql_delete_query, (codigo,))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro excluído com sucesso na tabela PRODUTO")

        except (Exception, psycopg2.Error) as error:

            print("Falha ao excluir registro na tabela PRODUTO", error)

        finally:

            if self.connection:

                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def atualizarDados(self, codigo, nome, preco):

        try:

            self.abrirConexao()
            cursor = self.connection.cursor()

            preco_acrescido = float(preco) * 1.10

            sql_update_query = sql_update_query = """UPDATE public."produto" SET "nome" = %s,
                    "preco" = %s WHERE "codigo" = %s"""
            cursor.execute(sql_update_query, (nome, preco_acrescido, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print (count, "Registro atualizado com sucesso na tabela PRODUTO")

        except(Exception, psycopg2.Error) as error:

            print("Falha ao atualizar registro na tabela PRODUTO", error)

        finally:

            if(self.connection):

                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def consultarProduto(self, codigo):

        try:

            self.abrirConexao()
            cursor = self.connection.cursor()

            sql_select_query = """SELECT "nome", "preco" FROM public."produto" WHERE "codigo" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            result = cursor.fetchone()

            if result:

                nome, preco = result
                return {"nome": nome, "preco": preco}
            
            else:

                return None

        except (Exception, psycopg2.Error) as error:

            print("Falha ao consultar produto na tabela PRODUTO", error)

        finally:

            if self.connection:
                
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")