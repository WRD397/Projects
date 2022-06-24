/*

Queries used for Tableau Visualization
Tableau Visualization : https://public.tableau.com/views/COVID19Analysis_16560132564910/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link

*/



			-- T A B L E   1 

SELECT SUM(new_cases) AS total_cases, SUM(CAST(new_deaths AS BIGINT)) AS total_deaths, SUM(CAST(new_deaths AS INT))/SUM(new_Cases)*100 AS death_percentage
	FROM  Project_COVID19..covid_death$
	--Where location = 'India'
	WHERE continent is not null 
	--GROUP BY date
	ORDER BY 1,2

-- Just a double check based off the data provided
-- numbers are extremely close so we will keep them - The Second includes "International"  Location

/*
SELECT SUM(new_cases) AS total_cases, SUM(CAST(new_deaths AS BIGINT)) AS total_deaths, SUM(CAST(new_deaths AS BIGINT))/SUM(new_cases)*100 AS death_percentage
	FROM Project_COVID19..covid_death$
	--WHERE location = 'India'
	WHERE location = 'World'
	GROUP BY date
	ORDER BY 1,2
*/



			-- T A B L E   2

-- We take these out as they are not inluded in the above queries and want to stay consistent
-- European Union is part of Europe

SELECT location, SUM(CAST(new_deaths AS BIGINT)) AS total_death_count
	FROM Project_COVID19..covid_death$
	--WHERE location = 'India'
	WHERE continent is null 
	AND location not in ('World', 'European Union', 'International', 'Upper middle income', 'High income', 'Lower middle income', 'Low income')
	GROUP BY location
	ORDER BY total_death_count DESC


			-- T A B L E   3

-- we are looking at total percentage of the population infected during whole COVID era till date. This is a locationwise classification.
SELECT Location, population, MAX(total_cases) AS highest_infection_count,  MAX((total_cases/population))*100 AS total_percentage_population_infected
	FROM Project_COVID19..covid_death$
	--WHERE location = 'India'
	GROUP BY location, population
	ORDER BY total_percentage_population_infected DESC


			--T A B L E    4

-- Here we are looking at the growth of the infection as the time passes by. So, naturally it's a date-wise classification.
SELECT location, population, date, total_cases,  (total_cases/population)*100 AS percentage_population_infection_growth
	FROM Project_COVID19..covid_death$
	WHERE location not in ('World', 'European Union', 'International', 'Upper middle income', 'High income', 'Lower middle income', 'Low income')
	--Where location = 'India'
	ORDER BY percentage_population_infection_growth DESC

-- An alternative approach
SELECT location, population, date, MAX(total_cases) as highest_infection_count,  Max((total_cases/population))*100 as percent_population_infected
	FROM Project_COVID19..covid_death$
	GROUP BY location, population, date
	ORDER BY percent_population_infected DESC

