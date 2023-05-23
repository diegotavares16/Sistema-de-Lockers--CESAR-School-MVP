from datetime import datetime, timedelta
from getpass import getpass
import os
import csv

os.system("cls")
lockers_disponiveis = {}
usuarios = {}


# cadastramento de usuário e administrador
def cadastrar_usuario():
    email_usuario = input("Digite seu email: ")
    senha_usuario = getpass("Digite sua senha: ")
    tipo_usuario = input("Digite o tipo de usuário (1 - Usuário, 2 - Administrador): ")

    if tipo_usuario not in ["1", "2"]:
        print(
            "Tipo de usuário inválido. Por favor, escolha 1 para Usuário ou 2 para Administrador."
        )
        return

    confirmacao = input("Confirmar cadastro? (s/n): ")

    if confirmacao.lower() == "s":
        if any(u["email"] == email_usuario for u in usuarios.values()):
            print("Usuário já cadastrado!")
        else:
            numero_usuario = str(len(usuarios) + 1)

            usuarios[numero_usuario] = {
                "numero": numero_usuario,
                "disponivel": True,
                "senha": senha_usuario,
                "data_vencimento": "",
                "pendente": True,
                "email": email_usuario,
                "tipo": tipo_usuario,
            }
            salvar_usuarios()
            salvar_lockers()
            print("Usuário cadastrado com sucesso!")
    else:
        print("Cadastro cancelado.")


# Função de login
def fazer_login():
    email_usuario = input("Digite seu email: ")
    senha_usuario = getpass("Digite sua senha: ")

    for usuario in usuarios.values():
        if usuario["email"] == email_usuario and usuario["senha"] == senha_usuario:
            tipo_usuario = usuario["tipo"]

            if tipo_usuario == "1":
                print("Login de usuário realizado com sucesso!")
                menu_usuario(usuario)
            elif tipo_usuario == "2":
                print("Login de administrador realizado com sucesso!")
                menu_administrador()
            return

    print("Credenciais inválidas. Tente novamente.")


# Carregar todos os usuários
def carregar_usuarios():
    with open("usuarios.csv", "r") as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        for linha in leitor_csv:
            numero_usuario = linha["numero"]
            usuarios[numero_usuario] = {
                "numero": linha["numero"],
                "disponivel": linha["disponivel"] == "True",
                "senha": linha["senha"],
                "data_vencimento": linha["data_vencimento"],
                "pendente": linha["pendente"] == "True",
                "email": linha["email"],
                "tipo": linha["tipo"],
                "locker": linha["locker"],
            }


# Salvar todos os usuários
def salvar_usuarios():
    with open("usuarios.csv", "w", newline="") as arquivo:
        campos = [
            "numero",
            "disponivel",
            "senha",
            "data_vencimento",
            "pendente",
            "email",
            "tipo",
            "locker",
        ]
        escritor_csv = csv.DictWriter(arquivo, fieldnames=campos)
        escritor_csv.writeheader()
        for usuario in usuarios.values():
            escritor_csv.writerow(usuario)


# Carregar todos os lockers
def carregar_lockers():
    with open("lockers.csv", "r", newline="") as arquivo_csv:
        reader = csv.DictReader(arquivo_csv)
        for linha in reader:
            numero_locker = linha["numero"]
            disponivel = linha.get("disponivel", "True") == "True"
            senha = linha.get("senha", "")
            data_vencimento = linha["data_vencimento"]
            pendente = linha.get("pendente", "True") == "True"

            lockers_disponiveis[numero_locker] = {
                "disponivel": disponivel,
                "senha": senha,
                "data_vencimento": data_vencimento,
                "pendente": pendente,
            }


# Salvar todos os lockers
def salvar_lockers():
    with open("lockers.csv", "w", newline="") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(
            ["numero", "disponivel", "senha", "data_vencimento", "pendente"]
        )
        for numero_locker, dados_locker in lockers_disponiveis.items():
            disponivel = dados_locker["disponivel"]
            senha = dados_locker["senha"]
            data_vencimento = dados_locker.get("data_vencimento", "")
            pendente = dados_locker["pendente"]
            writer.writerow(
                [numero_locker, disponivel, senha, data_vencimento, pendente]
            )


# Cria os lockers os lockers disponiveis
for i in range(1, 11):
    lockers_disponiveis[str(i)] = {"disponivel": True}


# Função para informar os lockers e sua disponibilidade
def listar_lockers_disponiveis():
    for numero_locker, status_locker in lockers_disponiveis.items():
        if status_locker["disponivel"]:
            if status_locker["pendente"]:
                print(f"Locker {numero_locker}: Pendente pela secretaria")
            else:
                print(f"Locker {numero_locker}: Disponível")
        else:
            print(f"Locker {numero_locker}: Indisponível")


# Função para informar os lockers ocupados junto com o usuário e a senha dele (apenas administrador pode executar a função)
def listar_locker_ocupado():
    print("Lockers ocupados:")
    for numero_locker, status_locker in lockers_disponiveis.items():
        if not status_locker["disponivel"]:
            usuario = None
            for u in usuarios.values():
                if u["locker"] == numero_locker:
                    usuario = u
                    break
            if usuario:
                print(
                    f"Locker {numero_locker} - Usuário: {usuario['email']} - Senha: {status_locker['senha']}"
                )
            else:
                print(
                    f"Locker {numero_locker} - Usuário não encontrado - Senha: {status_locker['senha']}"
                )


# Lista todos os lockers pendentes para alguem da secretaria mudar a senha do cadeado
def listar_lockers_pendentes():
    print("Lockers pendentes:")
    for numero_locker, status_locker in lockers_disponiveis.items():
        if status_locker["pendente"]:
            print(f"Locker {numero_locker} - Senha: {status_locker['senha']}")


# Informar/alterar a senha do locker (apenas administrador pode executar a função)
def senha_locker():
    numero_locker = input("Digite o número do locker que deseja adicionar a senha: ")
    if numero_locker in lockers_disponiveis:
        senha_locker = input("Digite a senha de 4 dígitos do locker: ")
        if len(senha_locker) == 4 and senha_locker.isdigit():
            lockers_disponiveis[numero_locker]["senha"] = senha_locker
            lockers_disponiveis[numero_locker]["pendente"] = False
            salvar_lockers()
            print(f"A senha do locker {numero_locker} foi adicionada com sucesso!")
        else:
            print("A senha do locker deve possuir 4 dígitos")
    else:
        print("Número de locker inválido. Por favor, digite um número válido.")


# Função para reservar o locker
def reservar_locker(usuario):
    if not usuario["disponivel"]:
        print("Você já possui um locker reservado. Não é possível reservar mais de um.")
        return

    print("Lockers disponíveis:")
    listar_lockers_disponiveis()
    numero_locker = input("Digite o número do locker que deseja reservar: ")
    if numero_locker in lockers_disponiveis:
        if (
            lockers_disponiveis[numero_locker]["disponivel"]
            and not lockers_disponiveis[numero_locker]["pendente"]
        ):
            try:
                dias = int(
                    input("Digite o número de dias que deseja alugar o locker: ")
                )
                if dias >= 0:
                    lockers_disponiveis[numero_locker]["disponivel"] = False
                    data_vencimento = datetime.now() + timedelta(days=dias)
                    lockers_disponiveis[numero_locker][
                        "data_vencimento"
                    ] = data_vencimento
                    usuario["disponivel"] = False
                    usuario["locker"] = numero_locker
                    salvar_lockers()
                    salvar_usuarios()
                    print(f"O locker {numero_locker} foi reservado com sucesso!")
                    print(
                        f"A senha do locker selecionado é {lockers_disponiveis[numero_locker]['senha']}"
                    )
                    print(f"O locker ficará reservado até {data_vencimento}")

                    lockers_disponiveis[numero_locker]["disponivel"] = False
                    salvar_lockers()

                else:
                    print("Valor inválido")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro válido.")
        else:
            print(f"O locker {numero_locker} já está indisponível.")
    else:
        print("Número de locker inválido. Por favor, digite um número válido.")


# Função para liberar o locker
def liberar_locker(usuario):
    if usuario["disponivel"]:
        print("Você não possui um locker reservado no momento.")
        return

    numero_locker = usuario["locker"]

    if not lockers_disponiveis[numero_locker]["disponivel"]:
        senha_locker = input("Digite a senha do cadeado do locker: ")
        if lockers_disponiveis[numero_locker]["senha"] == senha_locker:
            lockers_disponiveis[numero_locker]["disponivel"] = True
            lockers_disponiveis[numero_locker]["pendente"] = True
            usuario["disponivel"] = True
            salvar_lockers()
            salvar_usuarios()
            print(
                f"O locker {numero_locker} foi liberado com sucesso. Por favor, devolva o cadeado na secretaria mais próxima!"
            )
        else:
            print("Senha incorreta. Locker não liberado.")
    else:
        print(f"O locker {numero_locker} já está disponível.")


# Função para renovar o locker quando estiver perto de expirar
def renovar_ou_liberar_locker(numero_locker):
    data_vencimento = lockers_disponiveis[numero_locker]["data_vencimento"]
    dias_para_vencer = (data_vencimento - datetime.now()).days
    if dias_para_vencer <= 0:
        print(
            f"O tempo de locação do locker {numero_locker} expirou. Por favor, entregue o cadeado na secretaria mais próxima."
        )
        lockers_disponiveis[numero_locker]["disponivel"] = True
        lockers_disponiveis[numero_locker]["pendente"] = True
        salvar_lockers()
    elif dias_para_vencer <= 2:
        print(f"O tempo de locação do locker {numero_locker} está prestes a expirar.")
        print("O que deseja fazer?")
        print("1. Renovar locker")
        print("2. Liberar locker")
        opcao = input("Digite a opção desejada: \n")
        if opcao == "1":
            dias = int(input("Digite o número de dias que deseja renovar o locker: "))
            data_vencimento = data_vencimento + timedelta(days=dias)
            lockers_disponiveis[numero_locker]["data_vencimento"] = data_vencimento
            salvar_lockers()
            print(f"O locker {numero_locker} foi renovado com sucesso!")
            print(f"O locker ficará reservado até {data_vencimento}")
        elif opcao == "2":
            lockers_disponiveis[numero_locker]["disponivel"] = True
            lockers_disponiveis[numero_locker]["pendente"] = True
            salvar_lockers()
            print(f"O locker {numero_locker} foi liberado com sucesso!")
    else:
        print("Locker ainda está válido.")


# Função para verificar os lockers vencidos
def verificar_lockers_vencidos():
    print("Lockers vencidos:")
    for numero_locker, dados_locker in lockers_disponiveis.items():
        if not dados_locker["disponivel"]:
            data_vencimento_str = datetime.strptime(
                dados_locker["data_vencimento"], "%Y-%m-%d %H:%M:%S.%f"
            )
            data_vencimento = data_vencimento_str.date()

            if datetime.now().date() > data_vencimento:
                print(
                    f"Locker {numero_locker} - Data de vencimento: {data_vencimento_str}"
                )


# Menu do usuário
def menu_usuario(usuario):
    while True:
        print("\nBem-vindo ao sistema de lockers do CESAR!")
        print("Selecione uma opção:")
        print("1. Reservar locker")
        print("2. Liberar locker")
        print("3. Voltar para o menu de usuário.")

        opcao = input("Digite a opção desejada: \n")

        if opcao == "1":
            reservar_locker(usuario)
        elif opcao == "2":
            liberar_locker(usuario)
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")


# Menu do administrador
def menu_administrador():
    while True:
        print("\nBem-vindo ao menu do administrador!")
        print("Selecione uma opção:")
        print("1. Listar status dos lockers")
        print("2. Listar apenas lockers ocupados")
        print("3. Adicionar/Alterar senha do locker")
        print("4. Listar lockers pendentes")
        print("5. Verificar lockers vencidos")
        print("6. Voltar para seleção de usuário.")

        opcao = input("Digite a opção desejada: \n")

        if opcao == "1":
            print("Lockers disponíveis:")
            listar_lockers_disponiveis()
        elif opcao == "2":
            listar_locker_ocupado()
        elif opcao == "3":
            senha_locker()
        elif opcao == "4":
            listar_lockers_pendentes()
        elif opcao == "5":
            verificar_lockers_vencidos()
        elif opcao == "6":
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")


carregar_usuarios()
carregar_lockers()
while True:
    print("\nSelecione uma opção:")
    print("1. Cadastrar usuário")
    print("2. Fazer login")
    print("3. Sair")

    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        fazer_login()
    elif opcao == "3":
        salvar_usuarios()
        break
    else:
        print("Opção inválida. Por favor, selecione uma opção válida.")
