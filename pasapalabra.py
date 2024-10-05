from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Cargar las soluciones desde un archivo de texto
def cargar_soluciones(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        soluciones = [linea.strip() for linea in f]
    return soluciones

# Función principal para automatizar el rosco de Pasapalabra
def resolver_rosco():
    # Inicializa el navegador (asegúrate de tener el ChromeDriver configurado correctamente)
    driver = webdriver.Chrome()

    try:
        # Navegar a la página del rosco
        driver.get('https://www.antena3.com/programas/pasapalabra/rosco-virtual/')

        # Esperar a que el botón de aceptar cookies esté presente y hacer clic en él
        try:
            boton_cookies = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))
            )
            boton_cookies.click()
        except Exception as e:
            print("No se encontró el aviso de cookies o no fue necesario cerrarlo.")

        time.sleep(3)
        # Cambiar el contexto al iframe con id="pasapajuego"
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'pasapajuego'))
        )
        driver.switch_to.frame(iframe)
        # Esperar a que el contenedor con id="welcome" esté presente
        contenedor_bienvenida = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'welcome'))
        )

        time.sleep(5)

        # Dentro del contenedor, buscar el botón con el texto "Empezar"
        boton_empezar = contenedor_bienvenida.find_element(By.XPATH, './/button[contains(text(),"Empezar")]')

        # Hacer clic en el botón "Empezar"
        boton_empezar.click()

        # Esperar a que el rosco se cargue
        time.sleep(4)

        # Cargar las soluciones desde el archivo
        soluciones = cargar_soluciones('soluciones.txt')

        # Iterar por las preguntas del rosco y rellenar las respuestas
        for i in range(25):
            # Seleccionar el input de respuesta usando el id del contenedor padre
            input_campo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="respuesta"]//input'))
            )

            # Escribir la respuesta correspondiente
            input_campo.send_keys(soluciones[i])
            input_campo.send_keys(Keys.ENTER)

            # Esperar un poco antes de pasar a la siguiente letra
            time.sleep(1)

        # Pausa final para observar el resultado
        time.sleep(5)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
    finally:
        # Cerrar el navegador
        driver.quit()

# Ejecutar la función principal
if __name__ == "__main__":
    resolver_rosco()
