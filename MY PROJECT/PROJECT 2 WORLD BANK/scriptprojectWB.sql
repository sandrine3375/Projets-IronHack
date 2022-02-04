create database project2;

use project2;

select * from country;
select * from biz_cost;
select * from biz_proc;
select * from nb_days;


Create table summarnull
Select economy, ID, valeur from nb_days
where year='2018'
and valeur is not null -- delete rows with null
and economy in ('CHN','FRA','DZA','IND','KOR','LBN','POL','RUS','TUN','UKR')
;
 
-- pour supprimer les cases vides
delete from summarnull
where valeur='';

select * from summarnull;
-- pour unifier les titres des colonnes
ALTER TABLE summarnull
rename column valeur to valeur_days; 

-- Pour avoir des datatype numeric
ALTER TABLE summarnull
MODIFY COLUMN valeur_days numeric;

-- POur supprimer collone 
Alter table summarnull
Drop column valeur_proc; 

Alter table summarnull
add column valeur_proc char (100);
update summarnull
inner join biz_proc
on summarnull.ID=biz_proc.ID
Set summarnull.valeur_proc=biz_proc.valeur 
;
-- Pour avoir des datatype numeric
ALTER TABLE summarnull
MODIFY COLUMN valeur_proc numeric;
ALTER TABLE summarnull
MODIFY COLUMN valeur_proc float;

Alter table summarnull
add column valeur_cost char (100);
update summarnull
inner join biz_cost
on summarnull.ID=biz_cost.ID
Set summarnull.valeur_cost=biz_cost.valeur;
-- Pour avoir des datatype numeric
ALTER TABLE summarnull
MODIFY COLUMN valeur_cost numeric;

Alter table summarnull
add column country_name char (100);
update summarnull
inner join country
on summarnull.economy=country.id
Set summarnull.country_name=country.name;

Select * from summarnull
where economy in ('CHN','FRA','DZA','IND','KOR','LBN','POL','RUS','TUN','UKR')
;

select * from summarnull;
select min(valeur_days), max(valeur_days), min(valeur_proc), max(valeur_proc), min(valeur_cost), max(valeur_cost) from summarnull;

CREATE TEMPORARY TABLE summary_temp2
SELECT min(valeur_proc) minProc, max(valeur_proc) maxProc, min(valeur_days) minDays, max(valeur_days) maxDays, min(valeur_cost) minCost, max(valeur_cost) maxCost
FROM summarnull;

ALTER TABLE summarnull ADD COLUMN minProc char(50);
ALTER TABLE summarnull ADD COLUMN maxProc char(50);
ALTER TABLE summarnull ADD COLUMN minDays char(50);
ALTER TABLE summarnull ADD COLUMN maxDays char(50);
ALTER TABLE summarnull ADD COLUMN minCost char(50);
ALTER TABLE summarnull ADD COLUMN maxCost char(50);

select* from summary_temp2;

UPDATE summarnull SET minProc = (SELECT minProc FROM summary_temp2);
UPDATE summarnull SET maxProc = (SELECT maxProc FROM summary_temp2);
UPDATE summarnull SET minDays = (SELECT minDays FROM summary_temp2);
UPDATE summarnull SET maxDays = (SELECT maxDays FROM summary_temp2);
UPDATE summarnull SET minCost = (SELECT minCost FROM summary_temp2);
UPDATE summarnull SET maxCost = (SELECT maxCost FROM summary_temp2);

select* from summarnull ;

ALTER TABLE summarnull ADD COLUMN cost_norm1 float 
generated always as ((valeur_cost - minCost)/(maxCost - minCost)) stored;
ALTER TABLE summarnull ADD COLUMN proc_norm float 
generated always as ((valeur_Proc - minProc)/(maxProc - minProc)) stored;
ALTER TABLE summarnull ADD COLUMN days_norm float 
generated always as ((valeur_days - minDays)/(maxDays - minDays)) stored;

ALTER TABLE summarnull ADD COLUMN comp_ind1 float 
generated always as (cost_norm1 + proc_norm + days_norm) stored;

ALTER TABLE summarnull DROP COLUMN comp_ind1;

select country_name, comp_ind1, valeur_cost, valeur_proc, valeur_days from summarnull
where valeur_proc is not null
order by comp_ind1 asc;
-- proc: Korea, Rep; China; Russian Federation, france
-- days: France, Ukraine, Korea, Rep.China
-- cost: China, France, Russian Federation, Ukraine
-- france et chine, puis russie, korea et ukraine
