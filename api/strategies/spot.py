from algo.indicators.mm import get_MM

def analyse(data, prices):
    mm_100 = get_MM(prices, 100)
    return mm_100