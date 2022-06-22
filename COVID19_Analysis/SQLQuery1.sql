--SELECT *
--FROM Project_COVID19..covid_death$
--ORDER BY 3,4 

-- SELECT *
-- FROM Project_COVID19..covid_vaccination$
-- ORDER BY 3,4


-- Select Data to use :::
--SELECT location, date, total_cases, new_cases, total_deaths, population
--FROM Project_COVID19..covid_death$
--ORDER BY 1,2


-- Looking at Total Percentage of the Population affected and the Mortality rate  :::
--SELECT location, date, population, total_cases, total_deaths, (total_cases/population)*100 AS affected_percentage, (total_deaths/total_cases)*100 AS mortality_percentage
--FROM Project_COVID19..covid_death$
--WHERE location='India'
--ORDER BY affected_percentage DESC


-- Looking at Countries with highest Affected Percentage and Highest Mortality :::
							-- Here, we came across a problem, for so many countries it's showing mortality rate greater than expected value and even greater than 100 for some cases. So we are gonna check for few countriws for detailed view at this issue. Then we found out that for North Korea,it says, total cases is 1 but total deaths are 6.
--SELECT location,population, MAX(total_cases) AS max_total_cases, MAX(total_deaths) AS max_total_deaths, 
--		MAX((total_cases/population))*100 AS max_affected_percentage,
--		MAX((total_deaths/total_cases))*100 AS max_mortality
--	FROM Project_COVID19..covid_death$
--	GROUP BY location, population
--	ORDER BY max_mortality DESC


-- Looking at Nrth Korea datasets :::
--SELECT location, total_cases, total_deaths
--	FROM Project_COVID19..covid_death$
--	WHERE location = 'North Korea'
--	ORDER BY total_deaths DESC




--SELECT location,population, MAX(total_cases) AS max_total_cases, MAX((total_cases/population)*100) AS max_affected_percentage 
--	FROM Project_COVID19..covid_death$
--	GROUP BY location, population
--	ORDER BY max_affected_percentage DESC;

							-- This above particular query reveals a really shocking fact. 70 percent of the total population of a country called Faeroe Islands, are affected right now !! For Gibraltar, Andorra, Cyprus and others are also not in a good condition as well. Truely disapoynting.

-- Looking at the growth of the cases in Faeroe Islands in detail :::
--SELECT location, date, total_cases, population, (total_cases/population)*100 AS affected_percentage
--	FROM Project_COVID19..covid_death$
--	WHERE location = 'Faeroe Islands'
--	ORDER BY total_cases DESC;

--Looking at the growth of the cases in India :::
SELECT location, date, population, total_cases, total_deaths, (total_cases/population)*100 AS affected_percentage
	FROM Project_COVID19..covid_death$
	WHERE location = 'India'
	ORDER BY total_cases DESC;



-- Looking at the Death Rates per Population :::
							--if we dont mention continent is not null, then the data for 'world', 'high income', 'low income' all other irrelevant data points also would be added.
SELECT  location, MAX (CAST(total_deaths as INT)) AS total_death_counts
	FROM Project_COVID19..covid_death$
	WHERE continent IS NOT NULL
	GROUP BY location
	ORDER BY total_death_counts DESC



-- LET'S BREAK THINGS DOWN BY CONTINENTS
SELECT  location, MAX (CAST(total_deaths as INT)) AS total_death_counts
	FROM Project_COVID19..covid_death$
	WHERE continent IS NULL
	GROUP BY location
	ORDER BY total_death_counts DESC


-- Showing Continents with the Highest Death Counts
SELECT  continent, MAX (CAST(total_deaths as INT)) AS total_death_counts
	FROM Project_COVID19..covid_death$
	WHERE continent IS NOT NULL
	GROUP BY continent
	ORDER BY total_death_counts DESC



-- GLOBAL NUMBERS
-- ie. total cases and deaths across teh Globe on a given particular date.
SELECT date, SUM(new_cases) AS total_cases, SUM(CAST(new_deaths AS INT)) AS total_deaths, (SUM(CAST(new_deaths AS INT))/SUM(new_cases))*100 AS death_percentage
	FROM Project_COVID19..covid_death$
	--Where location like '%states%'
	WHERE continent IS NOT NULL 
	GROUP BY date
	ORDER BY date DESC








---- EXPLORING covid_vaccination dataset and JOINING with covid_death
SELECT *
	FROM Project_COVID19..covid_death$
	JOIN Project_COVID19..covid_vaccination$
	ON Project_COVID19..covid_death$.location = Project_COVID19..covid_vaccination$.location
		AND Project_COVID19..covid_death$.date = Project_COVID19..covid_vaccination$.date


--Total Population and Vaccination :::
SELECT deaths.continent, deaths.location, deaths.date, deaths.population, vac.new_vaccinations,
	SUM(CONVERT(int, vac.new_vaccinations)) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS cumulative_sum
	FROM Project_COVID19..covid_death$ deaths    -- we used alias as deaths and vac for convenience.
	JOIN Project_COVID19..covid_vaccination$ vac
	ON deaths.location = vac.location
		AND deaths.date = vac.date
	WHERE deaths.continent IS NOT NULL
	ORDER BY 2,3



-- USE CTE
WITH PopvsVac (continent, location, date, population, new_vaccinations, Cumulative_Sum)
AS
(
SELECT death.continent, death.location, death.date, death.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (PARTITION BY death.location ORDER BY death.location, death.date) AS Cumulative_Sum
--, (Cumulative_Sum/population)*100
	FROM Project_COVID19..covid_death$ death
	JOIN Project_COVID19..covid_vaccination$ vac
		ON death.location = vac.location
		AND death.date = vac.date
	WHERE death.continent IS NOT NULL
--order by 2,3
)
SELECT *, (Cumulative_Sum/population)*100
From PopvsVac
