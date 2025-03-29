MAX_PREJUIZO = 10.0  
MARGEM_MINIMA_LUCRO = 0.05  
LIMITE_PERDA_PERCENTUAL = 0.001  
DRAWDOWN_PERCENTUAL = 0.001  
TRAILING_ATIVO = True
TRAILING_PERCENTUAL = 0.0015 


def avaliar_entrada(candles):
    if len(candles) < 2:
        return False

    _, _, _, _, close_prev, _ = candles[-2]
    _, _, _, _, close_last, _ = candles[-1]

    return close_last < close_prev


def avaliar_saida(preco_compra, preco_atual, margem_minima=MARGEM_MINIMA_LUCRO):
    return preco_atual > preco_compra + margem_minima


def avaliar_stop(preco_compra, preco_atual, limite_perda=LIMITE_PERDA_PERCENTUAL):
    return preco_atual <= preco_compra * (1 - limite_perda)


def avaliar_drawdown(preco_atual, menor_preco, percentual=DRAWDOWN_PERCENTUAL):
    return preco_atual <= menor_preco * (1 - percentual)


def avaliar_limite_prejuizo(preco_compra, preco_atual, max_prejuizo=MAX_PREJUIZO):
    return (preco_compra - preco_atual) >= max_prejuizo


def avaliar_trailing(preco_compra, preco_atual, maior_preco, percentual=TRAILING_PERCENTUAL):
    if not TRAILING_ATIVO:
        return False
    # Sair se caiu X% a partir do topo
    return preco_atual <= maior_preco * (1 - percentual)


def gerenciar_saida(preco_compra, preco_atual, menor_preco, tempo_na_operacao,
                    margem_minima=MARGEM_MINIMA_LUCRO,
                    limite_perda=LIMITE_PERDA_PERCENTUAL,
                    max_tempo=180):
    maior_preco = max(preco_compra, preco_atual)

    if avaliar_saida(preco_compra, preco_atual, margem_minima):
        return "LUCRO"
    if avaliar_trailing(preco_compra, preco_atual, maior_preco):
        return "TRAILING"
    if avaliar_stop(preco_compra, preco_atual, limite_perda):
        return "STOP"
    if avaliar_drawdown(preco_atual, menor_preco):
        return "DRAWDOWN"
    if avaliar_limite_prejuizo(preco_compra, preco_atual):
        return "MAX_PREJUIZO"
    if tempo_na_operacao >= max_tempo:
        return "TEMPO"
    return None
