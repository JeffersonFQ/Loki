import webview

# Função para abrir uma janela com um WebView
def open_webview():
    webview.create_window('Exemplo WebView', 'https://www.exemplo.com')
    webview.start()

# Chame open_webview() onde você precisar abrir a página
open_webview()
