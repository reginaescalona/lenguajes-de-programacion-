import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Personajes de Naruto"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO  

    # Función para obtener datos de la API
    def fetch_characters():
        url = "https://dattebayo-api.onrender.com/characters"  # URL de la API
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("characters", [])
            else:
                return []  
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return []

    # Crear una tarjeta para cada personaje (con imagen nombre 3 jutsus y aldea)
    def create_character_card(character):
       
        image_url = character.get("images", [""])[0]
        if not image_url:
            image_url = "https://via.placeholder.com/150"
            
      
        name = character.get("name", "Nombre no disponible")
        
       
        jutsus = character.get("jutsu", ["Jutsus no disponibles"])[:3]
        
        
        village = character.get("personal", {}).get("affiliation", ["Aldea no disponible"])

        return ft.Card(
            elevation=5,
            content=ft.Container(
                padding=10,
                content=ft.Column(
                    [
                        ft.Image(
                            src=image_url,
                            width=150,
                            height=150,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(10),
                        ),
                        ft.Text(name, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Jutsus: {', '.join(jutsus)}", size=14, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Aldea: {', '.join(village)}", size=14, text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        )

    
    characters = fetch_characters()

    # Crear un GridView para mostrar las tarjetas
    grid_view = ft.GridView(
    
        expand=True,
        runs_count=2,         
        max_extent=300,  
        child_aspect_ratio=0.8, 
        spacing=20,             
        run_spacing=20,         
    )

    
    def update_cards(filtered):
        grid_view.controls.clear()
        for char in filtered:
            grid_view.controls.append(create_character_card(char))
        page.update()

   
    search_input = ft.TextField(
        label="Buscar por nombre",
        expand=True,
    )

    
    def search_changed(e):
        search_term = search_input.value.lower()
        if search_term:
            filtered = [char for char in characters if search_term in char.get("name", "").lower()]
        else:
            filtered = characters
        update_cards(filtered)

    search_input.on_change = search_changed

    
    page.add(search_input, grid_view)
    update_cards(characters)

# Ejecutar la aplicación
ft.app(target=main)
