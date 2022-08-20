								-- Payment type evolution 

with base as
	 (select 
		payments.order_id,orders.["order_purchase_timestamp"],
		DATENAME(year,orders.["order_purchase_timestamp"]) as purchase_year,
		DATENAME(MONTH,orders.["order_purchase_timestamp"]) as purchase_month,
		payments.payment_type, 
		payments.payment_installments
	 from TargetCustomerAnalysis.dbo.payments
	 join TargetCustomerAnalysis.dbo.orders
	 on orders.["order_id"] = payments.order_id)

select base.purchase_year, base.purchase_month, base.payment_type, count(base.order_id) as order_count
from base
group by base.purchase_year, base.purchase_month, base.payment_type;


								-- Payment Installments and Order Counts

select
DATENAME(year,orders.["order_purchase_timestamp"]) as purchase_year,
payment_installments, count(distinct order_id) as order_counts
from TargetCustomerAnalysis.dbo.payments
join TargetCustomerAnalysis.dbo.orders
on orders.["order_id"] = payments.order_id
group by DATENAME(year,orders.["order_purchase_timestamp"]),payment_installments
order by purchase_year



										-- Price variation
-- Lets verify the payment value column in payments table and total price calculated in order_items table.

select cast(["price"] as float), cast(["freight_value"] as float), (cast(["price"] as float)+ cast(["freight_value"] as float))as total_price, payments.payment_value
from TargetCustomerAnalysis.dbo.order_items
join TargetCustomerAnalysis.dbo.payments
on order_items.["order_id"] = payments.order_id

--So, yes they are exactly the same. payment_value is basically the total price for a particular order.

								
								-- Now lets calculate the percentage increase in order cost from 2017 to 2018 ( only January to August data is considered )


select percent_inc as percent_inc_order_cost_2017_18
from
(select (next_year_order_cost - order_cost_avg) / order_cost_avg * 100 as percent_inc
from
	(select base3.*,
	LEAD(order_cost_avg,1,0) over(order by year) as next_year_order_cost
	from
	(select year, AVG(payment_value) as order_cost_avg
	from
		(select datename(year,base.["order_purchase_timestamp"]) as year, payment_value
		from
		(select orders.["order_id"], orders.["order_purchase_timestamp"], payments.payment_value	
			from payments
			join orders
			on orders.["order_id"] = payments.order_id
			where (orders.["order_purchase_timestamp"] between '2017-01-01 00:00:00' and '2017-08-01 00:00:00')
					or (orders.["order_purchase_timestamp"] between '2018-01-01 00:00:00' and '2018-08-01 00:00:00')
					)base
					)base2
	group by year
	)base3
	)base4
	)base5
	where percent_inc > 0 
			
-- So, from 2017 to 2018 order cost increased 3.53%.



									-- Mean and sum of price and freigt value

select base2.["customer_state"], round(sum(base2.price),2) as total_order_price, round(AVG(price),2) as avg_order_price, round(SUM(base2.freight_value),2) as total_freight, round(avg(base2.freight_value),2) as avg_freight
from
	(select customers.["customer_state"],base.price, base.freight_value 
	from
		(select orders.["customer_id"], cast(["price"] as float) as price, cast(["freight_value"] as float) as freight_value
		from TargetCustomerAnalysis.dbo.order_items
		join orders
		on orders.["order_id"] = order_items.["order_id"])base

		join customers 
		on customers.["customer_id"] = base.["customer_id"])base2
group by ["customer_state"]



