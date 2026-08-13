from config import Settings
from tabdeal_api import TabdealAPI


def run():
    cfg = Settings()
    client = TabdealAPI(cfg.base_url)
    print("TABDEAL ANALYSIS ONLY")
    print("Symbol:", cfg.symbol)
    print("Live mode:", cfg.live_trading)
    print("Ping:", client.ping())


if __name__ == "__main__":
    run()
