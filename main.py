import time
import ccxt
from core.market_data import get_price, get_candles
from core.strategy import avaliar_entrada, gerenciar_saida
from core.logger import registrar_trade
from interfaces.telegram_bot import enviar_telegram

binance = ccxt.binance({
    'enableRateLimit': True
})

symbol = "BTC/USDT"
modo_compra = False
preco_compra = None
menor_preco = None
tempo_entrada = None


def main():
    global modo_compra, preco_compra, menor_preco, tempo_entrada
    print("🔄 Robô em modo simulado iniciado...")

    while True:
        candles = get_candles(binance, symbol)

        if not candles:
            print("[AVISO] Não foi possível obter os candles.")
            time.sleep(5)
            continue

        preco_info = get_price(binance, symbol)
        if not preco_info['bid'] or not preco_info['ask']:
            print("[AVISO] Não foi possível obter o order book.")
            time.sleep(5)
            continue

        if not modo_compra:
            if avaliar_entrada(candles):
                preco_compra = preco_info['ask']
                if preco_compra:
                    mensagem = f"✅ *COMPRA SIMULADA - MAKER*\nAtivo: {symbol}\nPreço de entrada: ${preco_compra:.2f}"
                    enviar_telegram(mensagem)
                    registrar_trade("COMPRA", preco_compra)
                    modo_compra = True
                    menor_preco = preco_compra
                    tempo_entrada = time.time()
        else:
            preco_atual = preco_info['bid']
            if preco_atual:
                menor_preco = min(menor_preco, preco_atual)
                tempo_operacao = int(time.time() - tempo_entrada)
                print(f"💹 Preço atual (BID): ${preco_atual} | Tempo: {tempo_operacao}s")

                decisao = gerenciar_saida(
                    preco_compra, preco_atual, menor_preco, tempo_operacao
                )

                if decisao:
                    resultado = preco_atual - preco_compra
                    mensagem = f"🚪 *{decisao}*\nSaindo a: ${preco_atual:.2f}\nResultado: ${resultado:.2f}\nTempo: {tempo_operacao}s"
                    enviar_telegram(mensagem)
                    registrar_trade(decisao, preco_atual, resultado, preco_compra)
                    modo_compra = False
                    preco_compra = None
                    menor_preco = None
                    tempo_entrada = None

        time.sleep(10)


if __name__ == "__main__":
    main()

