									--datatypes of all the column of selected database
USE "TargetCustomerAnalysis"
SELECT 
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME, 
COLUMN_NAME, 
DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS;

									-- Time range for which the data is available.

select min(["order_purchase_timestamp"]) as first_order_date, max(["order_purchase_timestamp"]) as last_order_date
from TargetCustomerAnalysis.dbo.orders
-- So we have data from 2016 September to 2018 October.


-- Different order status, availale in the dataset
select ["order_status"]
from TargetCustomerAnalysis.dbo.orders
group by ["order_status"];


								-- Lets first analyze the percentage of cancelled orders and prroducts under unavailable category :

	select ["order_status"], no_of_orders, 
	(no_of_orders*1.0/total_order_count)*100 as order_percent
	from
		(select base.*,
		sum(no_of_orders) over() as total_order_count
		from
			(select ["order_status"], count(distinct ["order_id"]) as no_of_orders
				from TargetCustomerAnalysis.dbo.orders
				group by ["order_status"])base)base2;
				


									-- lets analyze the REGIONWISE UNAVAILABLE PRODUCTS 

-- To visualize, creating a csv file out of this table.
select cus.["customer_id"], cus.["customer_city"]
from TargetCustomerAnalysis.dbo.customers cus
right join	
	(select * 
	from TargetCustomerAnalysis.dbo.orders
	where ["order_status"] = 'unavailable')temp
on cus.["customer_id"] = temp.["customer_id"];
					


									-- Analyse deliver time issues regionwise


select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"];
									


									-- Top 5 states with lowest freight charge as a whole


-- TOP 5 states with lowwest freight charge as a whole
select top(5) x.*
from
 (select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"])x
	order by freight_value_avg
									

									-- Top 5 states with highest time_to_delivery
select top(5) x.*
from
 (select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"])x
	order by time_to_delivery_avg desc	



									-- Top 5 states with lowest time_to_delivery with respect to estimated delivery date

select top(5) x.*
from
 (select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"])x
	order by diff_estimated_delivery_avg desc


	-- CONCERNING CASES 
									
									-- Top 5 states with highest freight charge as a whole

select top(5) x.*
from
 (select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"])x
	order by freight_value_avg desc



									-- Top 5 states with highest freight charge Year-wise
select top5.*
from
(select row_num.*,
ROW_NUMBER() over(partition by purchase_year order by freight_value_avg desc) as top5_yearwise
from
(select main.["customer_state"],main.purchase_year, avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],DATENAME(YEAR,["order_purchase_timestamp"]) as purchase_year,["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"], main.purchase_year)row_num)top5
	where top5.top5_yearwise < 6;									 									
									

									-- Top5 lowest average time_to_delivery
select top(5) x.*
from
 (select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"])x
	order by time_to_delivery_avg asc	



									-- Top 5 highest time to delivery with respect to estimated delivery


select top(5) x.*
from
 (select main.["customer_state"], avg(time_to_delivery) as time_to_delivery_avg, avg(diff_estimated_delivery) as diff_estimated_delivery_avg, avg(estimated_days_for_delivery) as estimated_days_for_delivery_avg, round(avg(freight_value),2) as freight_value_avg
	from 
	(select base2.*, cast(items.["freight_value"] as float) as freight_value
	from 
		(select
		base.*,customers.["customer_city"],customers.["customer_state"]
			from
				(select ["customer_id"],["order_id"], ["order_purchase_timestamp"],["order_delivered_customer_date"],["order_estimated_delivery_date"],
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_delivered_customer_date"]) as time_to_delivery,
					DATEDIFF(DD, ["order_delivered_customer_date"],["order_estimated_delivery_date"]) as diff_estimated_delivery,
					DATEDIFF(DD, ["order_purchase_timestamp"],["order_estimated_delivery_date"]) as estimated_days_for_delivery
				from TargetCustomerAnalysis.dbo.orders
				where (["order_status"] = 'delivered'))
				base
				join TargetCustomerAnalysis.dbo.customers as customers
				on base.["customer_id"] = customers.["customer_id"]
				where time_to_delivery >= 0)
				base2
				join TargetCustomerAnalysis.dbo.order_items as items
				on items.["order_id"] = base2.["order_id"])
				main
	GROUP BY main.["customer_state"])x
	order by diff_estimated_delivery_avg asc	


									-- Finding the Trend
select temp2.*,
(((temp2.order_count - temp2.previous_month_order_count) * 1.0) / nullif(temp2.previous_month_order_count,0) )*100 as growth_percent
from 
(select temp.*,
		lag(order_count,1,0) over(order by purchase_year,month_number) as previous_month_order_count
		from
			(select DATENAME(YEAR,["order_purchase_timestamp"]) as purchase_year,
					DATENAME(month, ["order_purchase_timestamp"]) as purchase_month, DATEPART(MM,["order_purchase_timestamp"]) as month_number,
					count(distinct ["order_id"]) as order_count
			from TargetCustomerAnalysis.dbo.orders
			group by  DATENAME(YEAR,["order_purchase_timestamp"]), DATENAME(month, ["order_purchase_timestamp"]),DATEPART(MM,["order_purchase_timestamp"])
			)temp)temp2;

	-- Thus we can see the huge growth of the company in 2017  
	



									-- Checking seasonality

with base as
	(select orders.["order_id"],["order_purchase_timestamp"], datename(month, ["order_purchase_timestamp"]) as month
	from TargetCustomerAnalysis.dbo.orders)
select month, count(distinct ["order_id"]) as frequency
from base
group by month
order by frequency desc

-- We can see thaere's peaks start from March upto August. A sudden fall in September and in all over the Winter season.
-- Lets visualize this in tableau




										-- Most of the orders are being placed usually at

with base as  
	(select temp.["order_purchase_timestamp"],
	case when hour <= 3 or hour > 21 then 'night'
		when hour > 3 and hour < 7 then 'dawn'
		when hour >= 7 and hour < 12 then 'morning'
		when hour >= 12 and hour < 17 then 'afternoon'
		else 'evening'
		end as shifts
	from
		(select ["order_purchase_timestamp"], datename(HOUR, ["order_purchase_timestamp"]) as hour
			from TargetCustomerAnalysis.dbo.orders)temp)

select  base.shifts, count(shifts) as frequency
from base
group by shifts
order by frequency
 -- So, most of the orders are being placed in the afternoon shifts that is post 12 at noon upto 5PM in the afternoon. And as expected least amount of orders are placed usually at dawn that is from 3AM in the morning to 7AM.



										-- A detailed order evolution over the time regionwise and statewise.


select top(100) base3.*, products.[product category]
	from
		(select base2.*,order_items.["product_id"],cast(order_items.["price"] as float) as price,cast(order_items.["freight_value"] as float) as freight_value, (cast(order_items.["price"] as float)+cast(order_items.["freight_value"] as float)) as total_price
			from
				(select base.*,orders.["order_id"], orders.["order_purchase_timestamp"]
				from
					(select ["customer_id"],["customer_zip_code_prefix"],["customer_city"],["customer_state"]
						from TargetCustomerAnalysis.dbo.customers)
						base

						join TargetCustomerAnalysis.dbo.orders orders
						on base.["customer_id"] = orders.["customer_id"])
						base2
						join TargetCustomerAnalysis.dbo.order_items as order_items
						on order_items.["order_id"] = base2.["order_id"])
						base3
						join TargetCustomerAnalysis.dbo.products products
						on base3.["product_id"] = products.product_id 

							


		
