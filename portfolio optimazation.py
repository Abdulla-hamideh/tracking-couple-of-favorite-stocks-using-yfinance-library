import yfinance as yf
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

stocks = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA", "FB", "GOOG", "JPM", "NFLX","BA","NKE","WMT","V","PYPL","BAC"]
df = yf.download(stocks, start= "1980-12-12")["Close"]

#calculate the expected annualized returns and the annulaized sample covriance matrix returns
# expected return
mu = expected_returns.mean_historical_return(df)
# sample coveriance
S = risk_models.sample_cov(df)

# optimize for the miximal sharpe ratio
# create the efficient fortier object
ef = EfficientFrontier(mu,S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print(cleaned_weights)
ef.portfolio_performance(verbose=True)

# get the discrete allocation of each share per stock
# your budget for investing
my_budget = 25000
latest_prices= get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights,latest_prices,total_portfolio_value=my_budget)
allocation,leftover = da.lp_portfolio()
print("Discrete allocation:", allocation)
print("funds Remaining:","$", leftover)

