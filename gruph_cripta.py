import yfinance as yf
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages


# Функция для получения данных о криптовалюте за последнюю неделю
def get_crypto_data(crypto_symbol):
    # Получаем данные за последнюю неделю
    crypto_data = yf.download(crypto_symbol, period="7d", interval="1d")
    return crypto_data


pdf = PdfPages("Figures.pdf")


# Функция для построения графика
def gruph_crypto_price(crypto_data, crypto_symbol):
    # Создаем новый график и сохраняем его в PDF
    plt.figure(figsize=(10, 5))
    plt.plot(crypto_data['Close'], label=f'{crypto_symbol} Цена', marker='o')
    plt.title(f'{crypto_symbol} Цена за последнею неделю')
    plt.xlabel('Дата')
    plt.ylabel('Цена в (USD)')
    plt.legend()
    plt.grid(True)

    pdf.savefig()
    pdf.close()

