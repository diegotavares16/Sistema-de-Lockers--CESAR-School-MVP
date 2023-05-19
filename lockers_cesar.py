from datetime import datetime, timedelta
import os
import csv

os.system("cls")
lockers_disponiveis = {}


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


# cria os lockers os lockers disponiveis
for i in range(1, 11):
    lockers_disponiveis[str(i)] = {"disponivel": True}


# função para informar os lockers
def listar_lockers_disponiveis():
    for numero_locker, status_locker in lockers_disponiveis.items():
        if status_locker["disponivel"]:
            if status_locker["pendente"]:
                print(f"Locker {numero_locker}: Pendente pela secretaria")
            else:
                print(f"Locker {numero_locker}: Disponível")
        else:
            print(f"Locker {numero_locker}: Indisponível")


# função para informar os lockers disponiveis junto com a senha dele (apenas administrador pode executar a função)
def listar_locker_ocupado():
    print("Lockers ocupados:")
    for numero_locker, status_locker in lockers_disponiveis.items():
        if not status_locker["disponivel"]:
            print(f"Locker {numero_locker} - Senha: {status_locker['senha']}")


def listar_lockers_pendentes():
    print("Lockers pendentes:")
    for numero_locker, status_locker in lockers_disponiveis.items():
        if status_locker["pendente"]:
            print(f"Locker {numero_locker} - Senha: {status_locker['senha']}")


# informar/alterar a senha do locker (apenas administrador pode executar a função)
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


# função para reservar o locker
def reservar_locker():
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
                    salvar_lockers()
                    print(f"O locker {numero_locker} foi reservado com sucesso!")
                    print(
                        f"A senha do locker selecionado é {lockers_disponiveis[numero_locker]['senha']}"
                    )
                    print(f"O locker ficará reservado até {data_vencimento}")
                else:
                    print("Valor inválido")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro válido.")
        else:
            print(f"O locker {numero_locker} já está indisponível.")
    else:
        print("Número de locker inválido. Por favor, digite um número válido.")


# função para liberar o locker
def liberar_locker():
    print("Lockers ocupados:")
    for numero_locker, status_locker in lockers_disponiveis.items():
        if not status_locker["disponivel"] and not status_locker["pendente"]:
            print(f"Locker {numero_locker}")

    numero_locker = input("Digite o número do locker que deseja liberar: ")

    if numero_locker in lockers_disponiveis:
        if (
            not lockers_disponiveis[numero_locker]["disponivel"]
            and not lockers_disponiveis[numero_locker]["disponivel"]
        ):
            senha_locker = input("Digite a senha do cadeado do locker: ")
            if lockers_disponiveis[numero_locker]["senha"] == senha_locker:
                lockers_disponiveis[numero_locker]["disponivel"] = True
                lockers_disponiveis[numero_locker]["pendente"] = True
                salvar_lockers()
                print(
                    f"O locker {numero_locker} foi liberado com sucesso. Por favor, devolva o cadeado na secretaria mais próxima!"
                )
            else:
                print("Senha incorreta. Locker não liberado.")
        else:
            print(f"O locker {numero_locker} já está disponível.")
    else:
        print("Número de locker inválido. Por favor, digite um número válido.")


# função para renovar o locker quando estiver perto de expirar
def renovar_ou_liberar_locker(numero_locker):
    data_vencimento = lockers_disponiveis[numero_locker]["data_vencimento"]
    dias_para_vencer = (data_vencimento - datetime.now()).days
    if dias_para_vencer <= 0:
        print(
            f"O tempo de locação do locker {numero_locker} expirou. Por favor, entregue o cadeado na secretaria mais próxima."
        )
        lockers_disponiveis[numero_locker]["disponivel"] = True
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
            salvar_lockers()
            print(f"O locker {numero_locker} foi liberado com sucesso!")
    else:
        print("Locker ainda está válido.")


def verificar_lockers_vencidos():
    print("Lockers vencidos:")
    for numero_locker, dados_locker in lockers_disponiveis.items():
        if not dados_locker["disponivel"]:
            data_vencimento_str = dados_locker["data_vencimento"].split()[0]
            data_vencimento = datetime.strptime(data_vencimento_str, "%Y-%m-%d")
            if datetime.now() > data_vencimento:
                print(
                    f"Locker {numero_locker} - Data de vencimento: {data_vencimento_str}"
                )


# menu do usuário
def menu_usuario():
    while True:
        print("\nBem-vindo ao sistema de lockers do CESAR!")
        print("Selecione uma opção:")
        print("1. Reservar locker")
        print("2. Liberar locker")
        print("3. Voltar para o menu de usuário.")

        opcao = input("Digite a opção desejada: \n")

        if opcao == "1":
            reservar_locker()
        elif opcao == "2":
            liberar_locker()
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")


# menu do administrador
def menu_administrador():
    while True:
        print("\nBem-vindo ao menu do administrador!")
        print("Selecione uma opção:")
        print("1. Listar status dos lockers")
        print("2. Listar apenas lockers ocupados")
        print("3. Adicionar/Alterar senha do locker")
        print("4. Listar lockers pendentes")
        print("5. Voltar para seleção de usuário.")

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
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")


carregar_lockers()
verificar_lockers_vencidos()
# login
while True:
    tipo_usuario = input(
        "Você é usuário ou administrador? \n1.Usuário\n2.Administrador\n3.Sair\n"
    ).lower()

    if tipo_usuario == "1":
        menu_usuario()
    elif tipo_usuario == "2":
        menu_administrador()
    elif tipo_usuario == "3":
        break

    else:
        print("Tipo de usuário inválido. Por favor, digite um valor que seja válido.\n")
