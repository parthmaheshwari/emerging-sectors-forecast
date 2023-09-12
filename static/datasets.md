## Overview 
This page contains the information about the explored datasets for the project.

| Dataset  | Category | Dataset Size | URL | Dynamic/Static| Attributes | Access Details | Restrictions | Additional Notes |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | 
| Huge Stock Market Dataset | Financial-Public | 8539 Financial assets (Stocks and ETFs) |  https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs |  Static  |  Date, Open, High, Low, Close, Volume, OpenInt |  Open-Free |  Only till 2017 |  - |
| TwelveData API | Financial-Public | 80k+ Financial assets and fundamentals (stock, forex, ETF, indices, crypto) worldwide | https://rapidapi.com/twelvedata/api/twelve-data1 | Dynamic | datetime, open, high, low, close, volume | Open-Freemium | 800 calls/day free | 79200 calls/day @ $29/mo, 350ms latency |
| Crunchbase Financial Dataset | Financial-Private | 3MM+ funding rounds | https://support.crunchbase.com/hc/en-us/articles/360041692693-How-to-Request-Access-to-Crunchbase-s-Academic-Research-Access-Program | Static | NA | Closed-Access Requested | - | - |
| YH Finance API | Financial-Public | Stocks + Fundamentals, size NA | https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/yh-finance-complete/pricing | Dynamic | datetime, open, high, low, close, adjClose, volume | Open-Freemium | 100 calls/day free | 60000/month @ $29/mo, 300ms latency, no rate limiting* |
| Pitchbook | Financial-Private | 2.1M Deals | https://pitchbook.com/data | Dynamic | NA | Closed-Access Requested | Expensive (as per some quotes, $8k+) | - | 
| Coresignal | Financial-Private | 16.8M deals | https://dashboard.coresignal.com/pricing | Dynamic | Name, Last funding date, Last funding type, Last funding raised, Acquisition price | Closed-Freemium | 200 rows free | Expensive, $0.2/row |
| yfinance | Financial-Public | Stocks,ETF,Indices,Mutual Funds,FOREX & more | https://pypi.org/project/yfinance/ | Dynamic | Ndatetime, open, high, low, close, adjClose, volume,Operational data,Ownership,Fundamental Data(Finance Statement,Dividends etc.) | Open | No Restrictions(Cons-Unofficial Library) | Made 7,000 API calls to retrieve and saved data from January 2000 to September 10, 2023, using a ticker list sourced from Kaggle |
| Refinitive Workspace | Financial-Private | NA | [https://dashboard.coresignal.com/pricing](https://www.refinitiv.com/en) | Dynamic | Name, Last funding date, Last funding type, Last funding raised, Acquisition price | Closed(Allowed via MSU) | Allows export upto 100000 rows at a time |  |


