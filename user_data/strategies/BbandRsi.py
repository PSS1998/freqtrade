# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# --------------------------------


class BbandRsi(IStrategy):
    """

    author@: Gert Wohlgemuth

    converted from:

    https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/BbandRsi.cs

    """
	"""
	note
	author@: Parsa Sadri
	
	sell strategy is extremly good.
	buy strategy has delay till it's profitable but in general is a simple and good strategy
	two trades simultaneously is optimal but if you want less risk make more trades simultaneously
	"""

    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.1,
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.25

    # Optimal ticker interval for the strategy
    ticker_interval = '5m'

    def populate_indicators(self, dataframe: DataFrame) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'] < 30) &
                    (dataframe['close'] < dataframe['bb_lowerband'])

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'] > 70)

            ),
            'sell'] = 1
        return dataframe
