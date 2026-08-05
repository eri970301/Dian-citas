from notifier import TelegramNotifier

telegram = TelegramNotifier()

telegram.send("✅ GitHub Actions está funcionando correctamente.")
"""
from dian_checker import DianChecker
from notifier import TelegramNotifier

checker = DianChecker()
telegram = TelegramNotifier()

print("Consultando DIAN...")

try:

    disponible = checker.check()

    print("Disponible:", disponible)

    if disponible:

        telegram.send(
            "🚨 ¡Hay citas disponibles para Videoatención - Devoluciones!\n\nhttps://agendamiento.dian.gov.co/"
        )

except Exception as ex:

    telegram.send(
        f"⚠️ Error monitor DIAN\n\n{ex}"
    )

    raise
    """
