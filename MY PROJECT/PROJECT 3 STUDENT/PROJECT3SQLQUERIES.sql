use project5;
select* from df ;

-- first query: which gender are more Competitiveness and SelfReliance? 
Select gender, 
round(avg(StrongNeedToAchieve),1) as StrongNeedToAchieve_Avg, 
round(avg(Competitiveness),1) as Competitveness_avg, 
round(avg (SelfReliance),1) as SelfReliance_avg, 
round(avg(perseverance),1) as Perserance_avg
from df
group by Gender
order by Perserance_avg desc;

-- second query: which genre have more implication? 
Select Gender, 
round((StrongNeedToAchieve_Avg + Competitveness_avg + SelfReliance_avg + Perserance_avg)/4,1) as implication_avg 
from
(select Gender,
round(avg(StrongNeedToAchieve),1) as StrongNeedToAchieve_Avg, 
round(avg(Competitiveness),1) as Competitveness_avg, 
round(avg (SelfReliance),1) as SelfReliance_avg, 
round(avg(perseverance),1) as Perserance_avg
from df
group by gender
) as new_tableS
order by implication_avg desc;

-- third query: which keyTraits shows less Competitiveness and SelfReliance? 
select KeyTraits,
round(avg(StrongNeedToAchieve),1) as StrongNeedToAchieve_Avg, 
round(avg(Competitiveness),1) as Competitveness_avg, 
round(avg (SelfReliance),1) as SelfReliance_avg, 
round(avg(perseverance),1) as Perserance_avg
from df
group by KeyTraits
order by Perserance_avg ;

-- fourth query: which keyTraits shows more Competitiveness and SelfReliance? with indice global
Select KeyTraits, 
round((StrongNeedToAchieve_Avg + Competitveness_avg + SelfReliance_avg + Perserance_avg)/4,1) as implication_avg 
from
(select KeyTraits,
round(avg(StrongNeedToAchieve),1) as StrongNeedToAchieve_Avg, 
round(avg(Competitiveness),1) as Competitveness_avg, 
round(avg (SelfReliance),1) as SelfReliance_avg, 
round(avg(perseverance),1) as Perserance_avg
from df
group by KeyTraits
) as new_table
order by implication_avg desc; 

-- fifth query : KeyTraits by gender  
select gender, count(*) from df where gender = "female"; 
select KeyTraits, count(*)*100/(select count(*) from df where gender = "female") as female_pourcentage from df
where gender = "female"
group by  gender, KeyTraits 
order by count(*) desc; 

select KeyTraits, count(*)/(select count(*) from df where gender = "Male")*100 as Male_pourcentage from df
where gender = "Male"
group by  gender, KeyTraits 
order by count(*) desc; 

 -- sixth query: how many student live in the city, group by age?
 select count(*) from data; -- total of student
 select count(*) from data -- number of student lives in city
 where City ='Yes';
 select city, count(City)*100 / (select count(*) from data ) as pourcentage_of_student from data
 group by City; -- pourcentage of student living in or not in city
select age,(count(City)*100 / (select count(*) from data )) from data
where City = 'Yes' -- pourcentage of student living in city, by age
group by age
order by age;
 
 