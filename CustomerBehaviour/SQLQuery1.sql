

		-- Let's look at the top Countries which have the most customers 

select ["customer_state"], count(*) as state_count
from customers
group by ["customer_state"]
order by state_count desc;
-- So, Sao Paolo, Rio de Janeiro and Minas Gerais have the most customers.



		-- Let's look at the top Cities which have the most customers 

select ["customer_state"],["customer_city"], count(["customer_city"]) city_count
from customers
group by ["customer_state"],["customer_city"]
order by city_count desc
-- Among the cities, Sao Paolo, Rio de Janeiro and Belo Horizonte in state Minas Gerais are the top 3 cities which have the most customers.



-- To visualize the country-wise customer distribution in Tableau export the following query to find Cities and States with their respective counts
select temp.["customer_city"],geo.longitude,geo.latitude, temp.city_count,
c.["customer_state"],
sum(city_count) over (partition by ["customer_state"]) as state_count
from (
	select ["customer_city"], count(["customer_city"]) as city_count
	from customers
	group by ["customer_city"] ) temp
left join (select ["geolocation_city"],cast(avg(cast(["geolocation_lng"] as numeric(10,7))) as varchar) as longitude , cast(avg(cast(["geolocation_lat"] as numeric(10,7))) as varchar) as latitude
			from geolocation
			group by ["geolocation_city"]) geo
	on temp.["customer_city"] = geo.["geolocation_city"]

left join (select distinct ["customer_city"],["customer_state"] 
			from customers) c 
	on temp.["customer_city"] = c.["customer_city"]

order by state_count


