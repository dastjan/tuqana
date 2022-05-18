import pandas as pd
import yfinance as yf

# Method for retrieving the free-cash-flow (fcf) ratio from yahoo finance
def get_yahoo_fcf_ratio(ticker):
    cashflows = ticker.cashflow
    capital_expenditures = cashflows.loc['Capital Expenditures'].values
    operating_cash = cashflows.loc['Total Cash From Operating Activities'].values
    net_incomes = cashflows.loc['Net Income'].values    
    fcf = operating_cash - capital_expenditures
    ratios = []    
    for y in range(len(fcf)):
        ratios.append(float(fcf[y])/float(net_incomes[y]))  
    fcf_ratio = sum(ratios)/len(ratios)
    return fcf_ratio

# Method for calculating the weighted average cost of capital (WACC)
def get_wacc(ticker):
    # average growth of the market (roughly 10% annually)
    avg_market_growth = 10    
    info = ticker.info
    financials = ticker.financials
    beta = info['beta3Year'] if info['beta3Year'] is not None else info['beta']    
    interest_expense = financials.loc['Interest Expense', financials.columns[0]]
    total_debt = info['totalDebt']   
    # Should actually be: interest expense/(short-term/current debt + long term debt)
    # mathematical absolute operator as interest expense is reported as a negative number
    cost_of_debt = (abs(interest_expense)/total_debt)*100    
    income_before_tax = financials.loc['Income Before Tax', financials.columns[0]]
    income_tax_expense = financials.loc['Income Tax Expense', financials.columns[0]]    
    corporate_tax_rate = income_tax_expense/income_before_tax    
    market_cap = info['marketCap']    
    weight_of_debt = total_debt/(total_debt + market_cap)
    weight_of_equity = market_cap/(total_debt + market_cap)    
    treasury_ten_year_yield = yf.Ticker('^TNX').info['previousClose']    
    cost_of_equity = treasury_ten_year_yield + beta*(avg_market_growth - treasury_ten_year_yield)    
    WACC = weight_of_debt * cost_of_debt * (1-corporate_tax_rate) + weight_of_equity * cost_of_equity

    variable_list = [beta, interest_expense, total_debt, weight_of_debt, cost_of_debt, weight_of_equity, cost_of_equity, corporate_tax_rate, avg_market_growth, treasury_ten_year_yield, WACC]
    return WACC, variable_list

def get_dcf(ticker):  
    # The perpetuity growth rate is typically between the historical inflation rate of 2-3%
    perpetual_growth = 2.5    
    ticker = yf.Ticker(ticker)
    info = ticker.info
    financials = ticker.financials
    shares_outstanding = info['sharesOutstanding'] 
    total_revenues = financials.loc['Total Revenue']
    net_incomes = financials.loc['Net Income'].values
    free_cashflow_ratio = get_yahoo_fcf_ratio(ticker)    
    
    latest_revenue = total_revenues[0]
    revenue_growth = total_revenues.pct_change(-1)
    revenue_growth = [x for x in revenue_growth if str(x) != 'nan']
    avg_revenue_growth = sum(revenue_growth)/len(revenue_growth)
    growth_factor = 1 + avg_revenue_growth
    projected_revenues = [latest_revenue, latest_revenue*growth_factor**2, latest_revenue*growth_factor**3, latest_revenue*growth_factor**4, latest_revenue*growth_factor**5]   
     
    income_margins = [float(net_incomes[y])/float(total_revenues[y]) for y in range(len(net_incomes))]
    income_margin = sum(income_margins)/len(income_margins)  
      
    projected_incomes = [x * income_margin for x in projected_revenues]
    projected_cashflows = [x * free_cashflow_ratio for x in projected_incomes]    
    WACC, variable_list = get_wacc(ticker)
    terminal_value = (projected_cashflows[-1] * (1+perpetual_growth/100))/(WACC/100 - perpetual_growth/100)    
    projected_cashflows.append(terminal_value)
    # The discount factor for the terminal value is the same as the last year
    discount_factors = [(1+WACC/100), (1+WACC/100)**2, (1+WACC/100)**3, (1+WACC/100)**4, (1+WACC/100)**5, (1+WACC/100)**5]    
    discounted_values = [projected_cashflows[i]/discount_factors[i] for i in range(len(discount_factors))]
        
    todays_value = sum(discounted_values)
    intrinsic_value = todays_value/shares_outstanding
    
    full_list = []
    full_list.append([len(total_revenues)])
    full_list.append(total_revenues.iloc[::-1])
    full_list.append([avg_revenue_growth])
    full_list.append([growth_factor])
    full_list.append(projected_revenues)
    full_list.append(financials.loc['Net Income'].iloc[::-1])
    full_list.append(list(reversed(income_margins)))
    full_list.append([income_margin])
    full_list.append(projected_incomes)
    full_list.append(projected_cashflows)
    full_list.append([WACC])
    full_list.append(discount_factors)
    full_list.append(discounted_values)   
    full_list.append([todays_value])
    full_list.append([shares_outstanding])
    full_list.append([intrinsic_value])
    
    df = pd.DataFrame(full_list)
    df.index = ['N of Reference Years', 'Previous Revenues', 'Revenue Growth', 'Revenue Growth Factor',
                'Projected Revenues', 'Previous Net Incomes', 'Net Income/Revenue Ratios',
                'Net Income/Revenue Ratio',  'Projected Net Incomes', 
                'Projected Cash Flows', 'WACC', 'Discount Factors', 
                'Discounted Values', 'Todays Value', 'Outstanding Shares', 
                'Fair Share Value']
    
    wacc_columns = ['beta', 'interest_expense', 'total_debt', 'weight_of_debt', 
                    'cost_of_debt', 'weight_of_equity', 'cost_of_equity', 'corporate_tax_rate', 
                    'avg_market_growth', 'treasury_ten_year_yield', 'wacc']
    
    wacc_df = pd.DataFrame(variable_list)
    wacc_df.index = wacc_columns
    
    return df, wacc_df

def analyze(shares):
    shares = sorted(shares)
    disclaimer_msg = 'Calculation started! This takes some time dependent on the number of stocks... please read the disclaimer:\n\n'
    disclaimer_msg += 'A company is subjective to the discounted cash flow (DCF) calculation if it meets one of the following citeria:\n'
    disclaimer_msg += '\n1. Company does not pay dividends'
    disclaimer_msg += "\n2. Company pays dividend, but dividends are very different from the company's ability to pay"
    disclaimer_msg += '\n3. Free cash flow aligns with profitability'
    disclaimer_msg += '\n4. Investor is taking a control perspective'
    disclaimer_msg += '\n\nBased on the last 4 years, the annual revenue growth is estimated and projected over 5 years. With this growth, the DCF and intrinsic share value is calculated.'
    print(disclaimer_msg)
    msg = 'Results of DCF analysis:'
    for share in shares:
        try:
            info = yf.Ticker(share).info
            currency = info['currency']
            recommendation_key = info['recommendationKey'].title() if 'recommendationKey' in info else False
            current_price = round(info['currentPrice'],2) if 'currentPrice' in info else round(info['previousClose'],2)
            df, df_wacc = get_dcf(share) 
            share_value = round(df.loc['Fair Share Value'].values[0],2)
            revenue_growth = round(float(df.loc['Revenue Growth'].values[0]) * 100, 2)
            msg += f'\n\n{share}:'
            msg += f'\nExpected annual revenue growth: {revenue_growth}%'
            msg += f'\nIntrinsic share value: {share_value} {currency}'
            msg += f'\nCurrent share price: {current_price} {currency}'
            if recommendation_key:
                msg += f'\nAnalyst recommendation: {recommendation_key}'                        
            if share_value > current_price:
                msg += '\nDCF share evaluation: Undervalued'
            else:
                msg += '\nDCF share evaluation: Overvalued'
        except:
            msg += f'\n\n{share}: Not available'
    
    return msg

    
if __name__ == '__main__':
    # Enter your ticker(s) in the list below
    tickers = ['AAPL', 'ASML.AS']
    msg = analyze(tickers)
    print(msg)
    
