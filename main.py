import flet as ft
from datetime import datetime

class Cliente:
    def __init__(self, id, nome, cpf, idade):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.idade = idade

class Quarto:
    def __init__(self, id, nome, valor, disponibilidade=True):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.disponibilidade = disponibilidade

class Reserva:
    def __init__(self, id, data_entrada, quarto, cliente, status="Ativa", data_saida=None):
        self.id = id
        self.data_entrada = data_entrada
        self.quarto = quarto
        self.cliente = cliente
        self.status = status
        self.data_saida = data_saida

class GerenciadorDeReservas:
    def __init__(self):
        self.lista_de_reservas = []
        self.lista_de_quartos = []
        self.lista_de_clientes = []

    def verQuartosDisponiveis(self):
        return [q for q in self.lista_de_quartos if q.disponibilidade]

    def verQuartosReservados(self):
        return [q for q in self.lista_de_quartos if not q.disponibilidade]

    def adicionarQuarto(self, quarto):
        self.lista_de_quartos.append(quarto)

    def removerQuarto(self, quarto_id):
        self.lista_de_quartos = [q for q in self.lista_de_quartos if q.id != quarto_id]

    def fazerReserva(self, reserva):
        if reserva.quarto.disponibilidade:
            self.lista_de_reservas.append(reserva)
            reserva.quarto.disponibilidade = False
            return True
        return False

    def encerrarReserva(self, reserva_id):
        for reserva in self.lista_de_reservas:
            if reserva.id == reserva_id and reserva.status == "Ativa":
                reserva.status = "Encerrada"
                reserva.data_saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                reserva.quarto.disponibilidade = True
                return True
        return False

    def adicionarCliente(self, cliente):
        self.lista_de_clientes.append(cliente)

    def removerCliente(self, cliente_id):
        self.lista_de_clientes = [c for c in self.lista_de_clientes if c.id != cliente_id]

def main(page: ft.Page):
    hotel = GerenciadorDeReservas()

    page.title = "Sistema de Reservas de Hotel"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def update_page():
        page.update()

    def show_message(text, color=ft.colors.RED_ACCENT_700):
        page.snack_bar = ft.SnackBar(
            ft.Text(text, color=color),
            open=True,
        )
        page.update()

    main_column = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=600
    )

    def update_main_column(content):
        main_column.controls = content
        page.update()

    def go_to_menu(e):
        update_main_column(
            [
                ft.Text("Hotel Gerenciador de Reservas", size=24, weight="bold"),
                ft.ElevatedButton("1 - Ver Quartos Disponíveis", on_click=lambda _: show_available_rooms()),
                ft.ElevatedButton("2 - Ver Quartos Reservados", on_click=lambda _: show_reserved_rooms()),
                ft.ElevatedButton("3 - Fazer uma Reserva", on_click=lambda _: show_make_reservation()),
                ft.ElevatedButton("4 - Encerrar uma Reserva", on_click=lambda _: show_end_reservation()),
                ft.ElevatedButton("5 - Gerenciar Clientes", on_click=lambda _: show_manage_clients()),
                ft.ElevatedButton("6 - Gerenciar Quartos", on_click=lambda _: show_manage_rooms()),
                ft.ElevatedButton("7 - Ver Reservas", on_click=lambda _: show_reservations()),
                ft.ElevatedButton("0 - Sair", on_click=lambda _: page.window_close()),
            ]
        )

    def show_available_rooms():
      available_rooms = hotel.verQuartosDisponiveis()

      if available_rooms:
          room_list = [ft.Text(f"ID: {room.id}, Nome: {room.nome}, Valor: {room.valor}") for room in available_rooms]
      else:
          room_list = [ft.Text("Nenhum quarto disponível.")]

      update_main_column([
          ft.Text("Quartos Disponíveis:", size=20, weight="bold"),
          ft.Column(room_list),
          ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
      ])

    def show_reserved_rooms():
      reserved_rooms = hotel.verQuartosReservados()

      if reserved_rooms:
          room_list = [ft.Text(f"ID: {room.id}, Nome: {room.nome}, Valor: {room.valor}") for room in reserved_rooms]
      else:
          room_list = [ft.Text("Nenhum quarto reservado.")]

      update_main_column([
          ft.Text("Quartos Reservados:", size=20, weight="bold"),
          ft.Column(room_list),
          ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
      ])

    def show_make_reservation():
      client_id_field = ft.TextField(label="ID do Cliente", keyboard_type=ft.KeyboardType.NUMBER)
      room_id_field = ft.TextField(label="ID do Quarto", keyboard_type=ft.KeyboardType.NUMBER)

      def make_reservation(e):
          try:
              client_id = int(client_id_field.value)
              room_id = int(room_id_field.value)

              client = next((c for c in hotel.lista_de_clientes if c.id == client_id), None)
              room = next((q for q in hotel.lista_de_quartos if q.id == room_id and q.disponibilidade), None)

              if not client:
                  show_message("ID de cliente inválido.", color=ft.colors.RED_ACCENT_700)
                  return
              if not room:
                  show_message("ID de quarto inválido ou indisponível.", color=ft.colors.RED_ACCENT_700)
                  return

              new_reservation = Reserva(len(hotel.lista_de_reservas) + 1, datetime.now().strftime("%Y-%m-%d"), room, client)
              if hotel.fazerReserva(new_reservation):
                  show_message("Reserva feita com sucesso!", color=ft.colors.GREEN_ACCENT_700)
              else:
                  show_message("Falha ao fazer a reserva.", color=ft.colors.RED_ACCENT_700)

          except ValueError:
              show_message("Entrada inválida. Por favor, insira IDs numéricos.", color=ft.colors.RED_ACCENT_700)

      update_main_column([
          ft.Text("Fazer uma Reserva", size=20, weight="bold"),
          client_id_field,
          room_id_field,
          ft.ElevatedButton("Fazer Reserva", on_click=make_reservation),
          ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
      ])

    def show_end_reservation():
      reservation_id_field = ft.TextField(label="ID da Reserva", keyboard_type=ft.KeyboardType.NUMBER)

      def end_reservation(e):
          try:
              reservation_id = int(reservation_id_field.value)
              if hotel.encerrarReserva(reservation_id):
                  show_message("Reserva encerrada com sucesso!", color=ft.colors.GREEN_ACCENT_700)
              else:
                  show_message("Falha ao encerrar a reserva. ID inválido ou reserva já encerrada.", color=ft.colors.RED_ACCENT_700)
          except ValueError:
              show_message("Entrada inválida. Por favor, insira um ID de reserva numérico.", color=ft.colors.RED_ACCENT_700)

      update_main_column([
          ft.Text("Encerrar uma Reserva", size=20, weight="bold"),
          reservation_id_field,
          ft.ElevatedButton("Encerrar Reserva", on_click=end_reservation),
          ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
      ])

    def show_reservations():
      if hotel.lista_de_reservas:
          reservation_list = []
          for reserva in hotel.lista_de_reservas:
              status = "Ativa" if reserva.status == "Ativa" else "Encerrada"
              reservation_list.append(ft.Text(
                  f"ID: {reserva.id}, Cliente: {reserva.cliente.nome}, Quarto: {reserva.quarto.nome}, "
                  f"Status: {status}, Entrada: {reserva.data_entrada}, Saída: {reserva.data_saida or 'N/A'}"
              ))
      else:
          reservation_list = [ft.Text("Nenhuma reserva encontrada.")]

      update_main_column([
          ft.Text("Reservas Atuais:", size=20, weight="bold"),
          ft.Column(reservation_list),
          ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
      ])

    def show_manage_clients():
        client_id_field = ft.TextField(label="ID do Cliente", keyboard_type=ft.KeyboardType.NUMBER)
        client_name_field = ft.TextField(label="Nome")
        client_cpf_field = ft.TextField(label="CPF")
        client_age_field = ft.TextField(label="Idade", keyboard_type=ft.KeyboardType.NUMBER)
        clients_list_column = ft.Column()

        def list_clients(e=None):
            clients_list_column.controls = []
            if hotel.lista_de_clientes:
                for client in hotel.lista_de_clientes:
                    clients_list_column.controls.append(ft.Text(
                        f"ID: {client.id}, Nome: {client.nome}, CPF: {client.cpf}, Idade: {client.idade}"))
            else:
                clients_list_column.controls.append(ft.Text("Nenhum cliente cadastrado."))
            page.update()

        def add_client(e):
            try:
                client_id = int(client_id_field.value)
                name = client_name_field.value
                cpf = client_cpf_field.value
                age = int(client_age_field.value)

                if any(not value for value in [client_id, name, cpf, age]):
                    show_message("Todos os campos são obrigatórios.", color=ft.colors.RED_ACCENT_700)
                    return

                hotel.adicionarCliente(Cliente(client_id, name, cpf, age))
                show_message("Cliente adicionado com sucesso!", color=ft.colors.GREEN_ACCENT_700)
                list_clients()
            except ValueError:
                show_message("Entrada inválida. Certifique-se de que o ID e a Idade são números.", color=ft.colors.RED_ACCENT_700)

        def remove_client(e):
            try:
                client_id = int(client_id_field.value)
                hotel.removerCliente(client_id)
                show_message("Cliente removido com sucesso!", color=ft.colors.GREEN_ACCENT_700)
                list_clients()
            except ValueError:
                show_message("Entrada inválida. Insira um ID de cliente numérico.", color=ft.colors.RED_ACCENT_700)

        list_clients()

        update_main_column([
            ft.Text("Gerenciar Clientes", size=20, weight="bold"),
            client_id_field,
            client_name_field,
            client_cpf_field,
            client_age_field,
            ft.ElevatedButton("Adicionar Cliente", on_click=add_client),
            ft.ElevatedButton("Remover Cliente", on_click=remove_client),
            ft.Text("Lista de Clientes:"),
            clients_list_column,
            ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
        ])

    def show_manage_rooms():
        room_id_field = ft.TextField(label="ID do Quarto", keyboard_type=ft.KeyboardType.NUMBER)
        room_name_field = ft.TextField(label="Nome do Quarto")
        room_price_field = ft.TextField(label="Preço do Quarto", keyboard_type=ft.KeyboardType.NUMBER)
        rooms_list_column = ft.Column()

        def list_rooms(e=None):
            rooms_list_column.controls = []
            if hotel.lista_de_quartos:
                for room in hotel.lista_de_quartos:
                    rooms_list_column.controls.append(ft.Text(
                        f"ID: {room.id}, Nome: {room.nome}, Preço: {room.valor}, Disponível: {'Sim' if room.disponibilidade else 'Não'}"
                    ))
            else:
                rooms_list_column.controls.append(ft.Text("Nenhum quarto cadastrado."))
            page.update()

        def add_room(e):
            try:
                room_id = int(room_id_field.value)
                name = room_name_field.value
                price = float(room_price_field.value)

                if any(not value for value in [room_id, name, price]):
                    show_message("Todos os campos são obrigatórios.", color=ft.colors.RED_ACCENT_700)
                    return

                hotel.adicionarQuarto(Quarto(room_id, name, price))
                show_message("Quarto adicionado com sucesso!", color=ft.colors.GREEN_ACCENT_700)
                list_rooms()
            except ValueError:
                show_message("Entrada inválida. Certifique-se de que o ID é um número inteiro e o Preço é um número.", color=ft.colors.RED_ACCENT_700)

        def remove_room(e):
            try:
                room_id = int(room_id_field.value)
                hotel.removerQuarto(room_id)
                show_message("Quarto removido com sucesso!", color=ft.colors.GREEN_ACCENT_700)
                list_rooms()
            except ValueError:
                show_message("Entrada inválida. Insira um ID de quarto numérico.", color=ft.colors.RED_ACCENT_700)

        list_rooms()

        update_main_column([
            ft.Text("Gerenciar Quartos", size=20, weight="bold"),
            room_id_field,
            room_name_field,
            room_price_field,
            ft.ElevatedButton("Adicionar Quarto", on_click=add_room),
            ft.ElevatedButton("Remover Quarto", on_click=remove_room),
            ft.Text("Lista de Quartos:"),
            rooms_list_column,
            ft.ElevatedButton("Voltar ao Menu", on_click=go_to_menu)
        ])

    page.add(main_column)
    go_to_menu(None)
    update_page()

ft.app(target=main)