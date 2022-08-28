

		-- Let's look at the top Countries which have the most customers 

select ["customer_state"], count(distinct customers.["customer_unique_id"]) as state_count
from TargetCustomerAnalysis.dbo.customers 
group by ["customer_state"]
order by state_count desc;
-- So, Sao Paolo, Rio de Janeiro and Minas Gerais have the most customers.



		-- Let's look at the top Cities which have the most customers 

select ["customer_state"],["customer_city"], count(["customer_city"]) city_count
from TargetCustomerAnalysis.dbo.customers
group by ["customer_state"],["customer_city"]
order by city_count desc;
-- Among the cities, Sao Paolo, Rio de Janeiro and Belo Horizonte in state Minas Gerais are the top 3 cities which have the most customers.



-- Total number of records in geolocation and customer tables.				

-- TOTAL ROWS in customers table is 99,441
select max(row_num) as total_number_of_rows
from
	(select
	ROW_NUMBER() over(order by ["customer_state"]) as row_num
	from TargetCustomerAnalysis.dbo.customers)x
	
-- TOTAL ROWS in geolocation table is 10,00,163
select max(row_num) as total_number_of_rows
from
	(select
	ROW_NUMBER() over(order by ["geolocation_state"]) as row_num
	from TargetCustomerAnalysis.dbo.geolocation)x


-- So on geolocation table, basically all possible zip codes and their locations are given. So lets visualize the customer distribution on the basis of customers table only.
-- To visualize the state-wise and city-wise customer distribution in Tableau exporting the following query to find Cities and States with their respective counts
select temp2.*, round(((city_count*1.0 / state_count)*100),2) as city_count_percent
from
	(select temp.*, sum(city_count) over(partition by ["customer_state"]) as state_count
		from(
			select ["customer_state"],["customer_city"], count(distinct ["customer_unique_id"]) city_count
			from TargetCustomerAnalysis.dbo.customers
			group by ["customer_state"],["customer_city"]
		)temp)temp2
order by state_count desc, city_count desc







