create database project2;

use project2;

select * from country;
select * from biz_cost;
select * from biz_proc;
select * from nb_days;

Create table summaryear
Select economy, ID, valeur from nb_days
where year='2019';
select * from summaryear;

ALTER TABLE summaryear
rename column valeur to valeur_days; 

Alter table summaryear
add column valeur_proc char (100);
update summaryear
inner join biz_proc
on summaryear.economy=biz_proc.economy
Set summaryear.valeur_proc=biz_proc.valeur;

Alter table summaryear
add column valeur_cost char (100);
update summaryear
inner join biz_cost
on summaryear.economy=biz_cost.economy
Set summaryear.valeur_cost=biz_cost.valeur;

Alter table summaryear
add column country_name char (100);
update summaryear
inner join country
on summaryear.economy=country.id
Set summaryear.country_name=country.name;

Select * from summaryear
where economy in ('CHN','FRA','DZA','IND','KOR','LBN','POL','RUS','TUN','UKR');

