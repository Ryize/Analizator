import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages
import os


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







    # plt.savefig("output.jpg")
    #
    # # Saving figure by changing parameter values
    # plt.savefig("output2", facecolor='y', bbox_inches="tight",
    #             pad_inches=0.3, transparent=True)
    # plt.close()
    # pdf.close()
    # plt.show()




# # Основная функция
# def main():
#     # Ввод символа криптовалюты (например, BTC-USD для Bitcoin)
#     crypto_symbol = input("Введите символ криптовалюты (например, BTC-USD): ")
#
#     # Получаем данные о криптовалюте
#     crypto_data = get_crypto_data(crypto_symbol)
#
#     # Строим график
#     gruph_crypto_price(crypto_data, crypto_symbol)
#
#
# if __name__ == "__main__":
#     main()