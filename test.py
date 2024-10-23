import webview

def open_webview():
    webview.create_window('Exemplo WebView', 'https://www.exemplo.com')
    webview.start()

open_webview()
