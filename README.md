# SHA3-MAC – coursework project  
[![CI](https://github.com/PaJuloyDedys/SHA3-MAC/actions/workflows/ci.yml/badge.svg)](https://github.com/PaJuloyDedys/SHA3-MAC/actions)

CLI-утиліта для **генерації та перевірки HMAC-SHA-3**  
(підтримуються теги 224/256/384/512 біт, а також бенчмарки й автоматичні тести).

## Встановлення

```bash
git clone https://github.com/PaJuloyDedys/SHA3-MAC.git
cd SHA3-MAC
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e ./src          # editable install для короткої команди `python -m hmac_sha3`
