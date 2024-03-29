{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import krakenex\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from pykrakenapi import KrakenAPI\n",
    "from datetime import datetime\n",
    "\n",
    "def get_OHLC(pair, t, interval):\n",
    "    k = krakenex.API()\n",
    "    data = k.query_public('OHLC', {'pair':pair, 'interval':interval})\n",
    "    def process_OHLC(data,pair,t):\n",
    "        a = data['result'][pair]\n",
    "        b =a[-t:]\n",
    "        time=[]\n",
    "        OHLC_mat =np.zeros((t,7)) \n",
    "        for n in range(0,t):\n",
    "            time.append(datetime.fromtimestamp(b[n][0]))    \n",
    "\n",
    "        for y in range(0,t):\n",
    "            for i in range(1,8):\n",
    "                OHLC_mat[y][i-1]=float(b[y][i])\n",
    "        \n",
    "        df = pd.DataFrame(OHLC_mat,columns=['Open','High', 'Low', 'Close', 'Vwap', 'Volume', 'Count'],index=time)\n",
    "        \n",
    "        return df\n",
    "    return process_OHLC(data,pair,t)\n",
    "\n",
    "def get_spread(pair, t):\n",
    "    k = krakenex.API()\n",
    "    data = k.query_public('Spread', {'pair':pair})\n",
    "    def process_spread(data, pair, t):\n",
    "        a = data['result'][pair]\n",
    "        b =a[-t:]\n",
    "        time=[]\n",
    "        spread_mat =np.zeros((t,2))\n",
    "        for n in range(0,t):\n",
    "            time.append(datetime.fromtimestamp(b[n][0]))    \n",
    "\n",
    "        for y in range(0,t):\n",
    "            for i in range(1,3):\n",
    "                spread_mat[y][i-1]=float(b[y][i])\n",
    "        \n",
    "        df = pd.DataFrame(spread_mat,columns=['Bid','Ask'],index=time)\n",
    "        return df\n",
    "    \n",
    "    return process_spread(data,pair,t)\n",
    "\n",
    "\n",
    "def get_trades(pair, t):\n",
    "    k = krakenex.API()\n",
    "    data = k.query_public('Trades', {'pair':pair})\n",
    "    def process_trades(data,pair,t):\n",
    "        a = data['result'][pair]\n",
    "        b =a[-t:]\n",
    "        time=[]\n",
    "        trades_mat =np.zeros((t,5)) \n",
    "        for n in range(0,t):\n",
    "            time.append(datetime.fromtimestamp(b[n][2]))\n",
    "        \n",
    "        price=[]\n",
    "        volume = []\n",
    "        bs = []\n",
    "        ml = []\n",
    "        misc=[]\n",
    "        for i in range(0, len(b)):\n",
    "            price.append(b[i][0])\n",
    "            volume.append(b[i][1])\n",
    "            bs.append(b[i][3])\n",
    "            ml.append(b[i][4])\n",
    "            misc.append(b[i][5])\n",
    "        \n",
    "        df = pd.DataFrame(columns=['Price','Volume', 'Buy/Sell','Market/Limit', 'Misc'],index=time)\n",
    "        df['Price']=price\n",
    "        df['Volume']=volume\n",
    "        df['Buy/Sell']=bs\n",
    "        df['Market/Limit']=ml\n",
    "        df['Misc']=misc\n",
    "        return df\n",
    "    \n",
    "    return process_trades(data,pair,t)\n",
    "\n",
    "def get_orderBook(pair, t, BA):\n",
    "    k = krakenex.API()\n",
    "    data = k.query_public('Depth', {'pair':pair})\n",
    "    def process_depth(data,pair,t):\n",
    "        asks = data['result'][pair]['asks'][-t:]\n",
    "        bids = data['result'][pair]['bids'][-t:]\n",
    "        time_ask=[]\n",
    "        time_bid=[]\n",
    "        for n in range(0,t):\n",
    "            time_ask.append(datetime.fromtimestamp(asks[n][2]))\n",
    "            time_bid.append(datetime.fromtimestamp(bids[n][2]))\n",
    "        \n",
    "        depth_mat_ask =np.zeros((t,2))\n",
    "        depth_mat_bid = np.zeros((t,2))\n",
    "        for y in range(0,t):\n",
    "            for i in range(0,2):\n",
    "                depth_mat_ask[y][i]=float(asks[y][i])\n",
    "                depth_mat_bid[y][i]=float(bids[y][i])\n",
    "        df_ask = pd.DataFrame(depth_mat_ask,columns=['Price','Volume'],index=time_ask)\n",
    "        df_bid = pd.DataFrame(depth_mat_bid,columns=['Price','Volume'],index=time_bid)\n",
    "        \n",
    "        if BA == 'ask':\n",
    "            return df_ask\n",
    "        if BA == 'bid':\n",
    "            return df_bid\n",
    "    \n",
    "    return process_depth(data, pair, t)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
