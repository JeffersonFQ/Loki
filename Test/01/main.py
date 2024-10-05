import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_dismissal(e):
        page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        # Limpa o conteúdo atual
        conteudo.controls.clear()
        
        # Altera o conteúdo com base no índice selecionado
        if e.selected_index == 0:
            conteudo.controls.append(ft.Text("Você selecionou Item 1", size=30))
        elif e.selected_index == 1:
            conteudo.controls.append(ft.Text("Você selecionou Item 2", size=30))
        elif e.selected_index == 2:
            conteudo.controls.append(ft.Text("Você selecionou Item 3", size=30))

        conteudo.update()

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )

    # Conteúdo principal
    conteudo = ft.Column()
    conteudo.controls.append(ft.Text("Selecione um item no menu.", size=20))

    # Adicionando o botão para abrir o drawer
    page.add(ft.ElevatedButton("Show drawer", on_click=lambda e: page.open(drawer)))
    page.add(conteudo)

ft.app(main)
