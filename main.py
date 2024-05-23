from pytube import YouTube
from flet import *
from pyperclip import paste
from time import sleep
import flet as ft


def main(page: ft.Page):

 
  #Função de download
  def informacoes(e):
    url = 'https://www.youtube.com/watch?v='

    #checagem de erro, mostra qual vídeo está sendo baixado
    try:
      yt = YouTube(url + url_texto.value)
      titulo_v = yt.title
      canal = yt.author

      views = yt.views 
      thumnail = yt.thumbnail_url
      miniatura = ft.Image(src=thumnail, width=400, height=300)

      #container que vai definir a box
      container_widget = ft.Column(
          [
              ft.Container(
                  bgcolor=ft.colors.RED_400,
                  border_radius=30,
                  width=400,
                  height=450,
                  padding=10,
                  alignment=ft.alignment.center,
                  margin=0,
                  content=ft.Column(
                      [
                        miniatura,
                        ft.Text(f"Título: {titulo_v}", weight="bold", size=20),
                        ft.Text(f"Canal: {canal}", weight="bold", size=15),
                        ft.Text(f"Views: {views}", weight="bold", size=15),
                      ]
                  )
              )
          ]
      )
      #modificações do botão download
      download_button.text = 'Download ' + yt.title
      horizontal = ft.Row(controls=[container_widget], alignment=ft.MainAxisAlignment.CENTER)
      box.content = horizontal
      page.update()

    except Exception as ex:
      print(f"Erro: {ex}")

      box.content = container_erro_centralizado
      page.update()


  def download(e):

    url = 'https://www.youtube.com/watch?v='

    try:
      yt = YouTube(url + url_texto.value)

      video = yt.streams.get_highest_resolution()

      video.download()
      #mostrar download concluido embaixo appbar na direita
      download_ok()
      page.update()
    except:
      box.content = container_erro_centralizado
      page.update()

  def download_ok():
    box_download = ft.Container(
      bgcolor=ft.colors.GREEN_400,
      border_radius=30,
      width=250,
      height=50,
      margin=10,
      content=ft.Row(
        [
          ft.Icon(ft.icons.DOWNLOAD_DONE),
          ft.Text("Download Concluido", weight='bold'),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
      )
    )
    page.add(ft.Row([box_download],alignment=ft.MainAxisAlignment.CENTER))

  def colar(e):
      url_texto.value = paste()
      informacoes(None)
      sleep(0.2)
      page.update()

  #função de tema
  def tema(e):
    if page.theme_mode == ft.ThemeMode.DARK:
      page.theme_mode = ft.ThemeMode.LIGHT
      icone_tema.name=ft.icons.SUNNY
      icone_tema.color=ft.colors.YELLOW_800
    else:
      page.theme_mode = ft.ThemeMode.DARK
      icone_tema.name=ft.icons.NIGHTLIGHT_OUTLINED
      icone_tema.color=ft.colors.BLUE_900

    page.update() 

  #Alinhamento Vertical e Horizontal
#   page.vertical_alignment = ft.MainAxisAlignment.CENTER    
#   page.horizontal_alignment = ft.MainAxisAlignment.CENTER

  #Título e tema
  page.title = "Youtube Downloader"
  page.theme_mode = ft.ThemeMode.DARK

  #Caixa de texto onde vai ficar URL
  titulo = ft.Text("Youtube Downloader", size=30, weight='bold')
  url_texto = ft.TextField(hint_text='Link', width=500, border_color='Red', border_radius=30, multiline=False, on_change=informacoes)

  #switch para mudar o tema e icone
  tema_switch = ft.Switch(value=False, scale=0.8, on_change=tema)
  icone_tema = ft.Icon(name=ft.icons.NIGHTLIGHT_OUTLINED, color=ft.colors.BLUE_900, size=25)


  #botão download e colar
  download_button = ft.ElevatedButton(text="Download", on_click=download,  height=35,  bgcolor=ft.colors.GREEN_400, color=ft.colors.WHITE, icon=ft.icons.DOWNLOAD_FOR_OFFLINE_OUTLINED, icon_color=ft.colors.WHITE,)

  paste_button = ft.ElevatedButton(text="Paste", on_click=colar, width=120, height=35, bgcolor=ft.colors.BLUE_400, color=ft.colors.WHITE, icon=ft.icons.PASTE,)

  #container de erro
  container_erro = ft.Container(
    border_radius=30,
    bgcolor=ft.colors.RED_400,
    width=400,
    height=55,
    padding=10,

    content=Column(
      [
        ft.Text("Error while trying to download the video, please check if the link is correct", text_align=ft.TextAlign.CENTER, size=15, weight='bold')
      ]
    )
  )
  container_erro_centralizado = ft.Row(controls=[container_erro], alignment=ft.MainAxisAlignment.CENTER)


  #box que vai aparecer o thumnail, titulo e canal
  box = ft.Container(visible=True)
    
  icone = ft.Container(
    bgcolor=ft.colors.WHITE,
    border_radius=100,
    height=40,
    alignment=ft.alignment.center,
    padding=5,
    margin=10,
    content=ft.Row(
      [
        icone_tema,
        tema_switch,
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    )
  )


  #Appbar
  appbar = ft.AppBar(
    leading=ft.Icon(ft.icons.CLOUD_DOWNLOAD, size=40, color=ft.colors.WHITE),
    title=ft.Text("YTBaixar", weight='bold', size=30),
    bgcolor=ft.colors.RED_400,
    actions=[
        icone,
    ],
  )
  #Container principal com título e url_texto em colunas e download_button e paste_button em linhas
  coluna = ft.Column(controls=[url_texto], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
  linha = ft.Row([coluna], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
  #Alinha o titulo verticalmente e horizontalmente

  titulo_s = ft.Column(controls=[titulo], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
  linha_s = ft.Row([titulo_s], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
  
  container_principal = ft.Container(
    content=ft.Column(
      [
        linha_s,
        linha,
        ft.Row(
          [
            download_button,
            paste_button,
          ],
          alignment=ft.MainAxisAlignment.CENTER,
        ),
        box,
      ]
    )
  )

  page.add(appbar, container_principal)


ft.app(target=main, view=ft.AppView.FLET_APP)