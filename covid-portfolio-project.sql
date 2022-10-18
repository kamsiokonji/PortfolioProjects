--select *
--from coviddeaths
--order by 3,4

--select *
--from covidvaccinations
--order by 3,4

--looking at total_cases vs total_deaths and the percentage of death resulting from it in nigeria
select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as deathpercentage
from coviddeaths
where location = 'nigeria'
order by 1,2

--looking at total_cases vs population in nigeria
select location, date, total_cases, population, (total_cases/population)*100 as percentagepopulationinfected
from coviddeaths
where location = 'nigeria'
order by 1,2

--looking at the highest countries that are infected

select location, population, max(total_cases) as highestcases, max((total_cases/population))*100 as percentagepopulationinfected
from coviddeaths
group by location, population
order by percentagepopulationinfected desc

--showing continent with the highest death count

select continent, max(cast(total_deaths as int)) as totaldeathcount
from coviddeaths
where continent is not null
group by continent
order by totaldeathcount desc


--global numbers
select date, sum(new_cases), sum(cast(new_deaths as int )), sum(cast(new_deaths as int ))/sum(new_cases) *100 as deathpercentage
from coviddeaths
where continent is not null
group by date
order by 1,2


--looking at total population vs vaccinations

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as rollingpeoplevaccinated
from coviddeaths dea
join covidvaccinations vac
	on dea.location = vac.location and dea.date = vac.date
where dea.continent is not null
order by 2,3

--using CTE

With PopvsVac (Continent, Location, Date, Population, new_vaccinations, rollingpeoplevaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as rollingpeoplevaccinated
from coviddeaths dea
join covidvaccinations vac
	on dea.location = vac.location and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)

Select *, (rollingpeoplevaccinated/Population)*100 as percentpopulationvaccinated
from PopvsVac

--using temp table

drop table if exists #percentpopulationvaccinated
create table #percentpopulationvaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
rollingpeoplevaccinated numeric
)

insert into #percentpopulationvaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as rollingpeoplevaccinated
from coviddeaths dea
join covidvaccinations vac
	on dea.location = vac.location and dea.date = vac.date
--where dea.continent is not null
--order by 2,3

Select *, (rollingpeoplevaccinated/Population)*100 as percentpopulationvaccinated
from #percentpopulationvaccinated

--creating views to use for visualizations in tableau

create view percentpopulationvaccinated as 
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint,vac.new_vaccinations)) OVER (Partition by dea.location order by dea.location, dea.date) as rollingpeoplevaccinated
from coviddeaths dea
join covidvaccinations vac
	on dea.location = vac.location and dea.date = vac.date
--where dea.continent is not null
--order by 2,3

select *
from percentpopulationvaccinated


create view totaldeathcount as
select continent, max(cast(total_deaths as int)) as totaldeathcount
from coviddeaths
where continent is not null
group by continent
--order by totaldeathcount desc

select *
from totaldeathcount


create view percentpopulationinfected as
select location, population, max(total_cases) as highestcases, max((total_cases/population))*100 as percentagepopulationinfected
from coviddeaths
group by location, population
--order by percentagepopulationinfected desc

select *
from percentpopulationinfected
order by 4 desc


