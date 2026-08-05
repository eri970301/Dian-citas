import json
import os
from datetime import datetime

from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

from config import BASE_URL, HEADLESS, SCREENSHOT_FOLDER


class DianChecker:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

        self.api_result = None

    # --------------------------------------------

    def screenshot(self, name):

        os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

        filename = os.path.join(
            SCREENSHOT_FOLDER,
            datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + name + ".png"
        )

        self.page.screenshot(
            path=filename,
            full_page=True
        )

    # --------------------------------------------

    def on_response(self, response):

        if "Player.aspx/ValidadorValidar" not in response.url:
            return

        try:

            body = response.json()

            if "d" not in body:
                return

            data = json.loads(body["d"])

            detalle = data.get("DetalleAdicional")

            print("Respuesta:", detalle)

            # SOLO NOS INTERESA ESTA
            if detalle in (
                "manejadorNoEncontroColas",
                "manejadorEncontroColas"
            ):

                self.api_result = data

                print("******** RESPUESTA FINAL ********")
                print(json.dumps(data, indent=4, ensure_ascii=False))
                print("********************************")

        except Exception as ex:

            print(ex)

    def open(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS
        )

        self.page = self.browser.new_page()

        self.page.on("response", self.on_response)

        self.page.goto(
            BASE_URL,
            wait_until="networkidle"
        )

    # --------------------------------------------

    def close(self):

        try:
            self.browser.close()
        except:
            pass

        try:
            self.playwright.stop()
        except:
            pass

    # --------------------------------------------

    def check(self):

        try:

            self.open()

            self.page.locator(
                '[nombrecontrol="btnSolicitarCita"]'
            ).click()

            self.page.wait_for_timeout(1000)

            self.page.locator(
                '.btnTipoPersona[llave="1"]'
            ).click()

            self.page.wait_for_timeout(1000)

            self.page.locator(
                '.btnTipoAtencion[llave="2"]'
            ).click()

            self.page.wait_for_timeout(1000)

            self.page.locator(
                ".btnCategoria"
            ).filter(
                has_text="Devoluciones"
            ).first.click()

            print("Esperando respuesta del servidor...")

            for _ in range(40):

                if self.api_result:
                    break

                self.page.wait_for_timeout(250)

            if self.api_result is None:

                print("Nunca llegó la respuesta.")

                self.screenshot("sin_respuesta")

                return False

            encontrado = self.api_result.get("Encontrado", False)

            detalle = self.api_result.get("DetalleAdicional")

            print("Encontrado:", encontrado)
            print("Detalle:", detalle)

            if encontrado:

                self.screenshot("HAY_CITAS")

                return True

            self.screenshot("SIN_CITAS")

            return False

        except Exception as ex:

            print(ex)

            self.screenshot("ERROR")

            raise

        finally:

            self.close()