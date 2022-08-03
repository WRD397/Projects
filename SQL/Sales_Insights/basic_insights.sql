		 
					-- B A S I C 	D A T A 	A N A L Y S I S 	A N D 	I N S I G H T S
         
         
SELECT * FROM sales_updated.customers;

select count(*) from customers; 
-- So, total number of customers --> 38

select distinct customer_type from customers; 
-- Basically, only, two types of customers are there.

 -- Lets focus on TRANSACTIONS TABLE.
 select * from transactions;

select count(distinct product_code) from transactions;
-- So, there are 338 total different products we are dealing with.

select distinct currency from transactions;
-- transactions have been done in two types of currencies only, INR and USD
select * from transactions 
where currency='USD';


-- Lets look into the currencies and transaction detail in that currency
select c.customer_name, subquery.markets_name, subquery.order_date, subquery.product_code, subquery.currency,
		subquery.profit_margin, subquery.cost_price
	from customers c
	join (select * 
		from transactions t
		join markets m
		on t.market_code = m.markets_code
		where currency = 'USD') subquery
	using (customer_code);
    
-- So, basically in November 2017, two transactions were done with customer 'Premium Stores' in USD. The transactions placed in Delhi NCR.

		-- DATES
-- Start and End dates of the records.
select min(date), max(date) from date;
 -- the total transactions from 2017 june to 2020 june are recorded in the database.
 
		-- RECORDS IN 2020
 -- Total number of transactions done in last year.
 select count(*) 
 from date 
 where year = 2020;
 
 
 -- filter data for negative values
 select * from transactions
 where sales_amount < 0;
 
 
 -- TOTAL REVENUE IN 2020
 select sum(sales_amount) 
 from transactions
 where order_date in
	(select date.date
    from date
    where year = 2020);
 