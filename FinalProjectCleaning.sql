USE final_project;

-- Type_Chart
INSERT
	type_chart
SELECT DISTINCT
	*
FROM
	type_staging;

-- Species
INSERT 
	species(species_id, species_name, egg_group_1, egg_group_2)
SELECT DISTINCT 
	ndex, 
    species, 
    egggroup1, 
    egggroup2 
FROM 
( 
	SELECT 
		*, 
        ROW_NUMBER() OVER(PARTITION BY ndex) AS row_num 
    FROM 
		pokemon_staging
) AS pokemon_staging_dups
WHERE row_num = 1;

-- Abilities
INSERT
	abilities(ability_name, description)
SELECT DISTINCT
	*
FROM
	abilities_staging;

-- Hatching
INSERT
	hatching(species_id, steps)
SELECT DISTINCT
	ID, 
	Gen7Steps
FROM
	hatching_staging
INNER JOIN
	species 
ON 
	hatching_staging.ID = species.species_id;

-- Forms
-- INSERT
-- 	forms (species_id, form_name, type_id, ability_1, ability_2, ability_h, hp, attack, defense, special_attack, special_defense, speed, total_stats, weight_lbs, height_in, description_1, description_2, class, percent_male, percent_female)
-- SELECT
-- 	ndex, forme, type_id, ability_1, ability_2, ability_h, hp, attack, defense, spattack, spdefense, speed, total, 
-- 	CAST(REPLACE(weight, ' lbs', '') AS FLOAT) AS weight_lbs,
-- 	(CAST(SUBSTRING_INDEX(height, '\'\'', 1) AS UNSIGNED) * 12) + CAST(REPLACE(SUBSTRING_INDEX(height, '\'\'', -1), '\"', '') AS UNSIGNED) AS height_in,
--     dex1, dex2, class, percentmale, percentfemale
-- FROM
-- (
-- 	SELECT
-- 		ndex, forme, type1, type2,
-- 		abilities.ability_id as ability_1, 
-- 		ability_2,
-- 		ability_h,
-- 		hp,	attack,
-- 		defense, spattack, spdefense, speed, total, weight, height, dex1, dex2, class, percentmale,	percentfemale
-- 	FROM
-- 	(
-- 		SELECT
-- 			ndex, forme, type1, type2,
-- 			ability1, 
-- 			abilities.ability_id as ability_2,
-- 			ability_h,
-- 			hp,	attack,
-- 			defense, spattack, spdefense, speed, total, weight, height, dex1, dex2, class, percentmale,	percentfemale
-- 		FROM
-- 		(
-- 			SELECT
-- 				ndex, forme, type1, type2,
-- 				ability1, 
-- 				ability2,
-- 				abilities.ability_id as ability_h,
-- 				hp,	attack,
-- 				defense, spattack, spdefense, speed, total, weight, height, dex1, dex2, class, percentmale,	percentfemale
-- 			FROM
-- 				pokemon_staging
-- 			LEFT JOIN
-- 				abilities
-- 			ON
-- 				pokemon_staging.abilityH = abilities.ability_name
-- 		) AS res3
-- 		LEFT JOIN
-- 			abilities
-- 		ON
-- 			res3.ability2 = abilities.ability_name
-- 	) AS res2
-- 	LEFT JOIN
-- 		abilities
-- 	ON
-- 		res2.ability1 = abilities.ability_name
-- ) AS res1
-- INNER JOIN
-- 	type_chart
-- ON
-- 	res1.type1 = type_chart.primary_type and res1.type2 = type_chart.secondary_type;

-- Moves

-- Form_Move

-- Items
INSERT
	items
SELECT DISTINCT 
	id, 
    item, 
    description
FROM 
( 
	SELECT 
		*, 
        ROW_NUMBER() OVER(PARTITION BY item) AS row_num 
    FROM 
		items_staging
	WHERE
		items_staging.item != '???' AND items_staging.description != '- - -'
) AS pokemon_staging_dups
WHERE row_num = 1;

-- Natures
INSERT
	natures(nature_name, attack_mult, special_attack_mult, defense_mult, special_defense_mult, speed_mult)
SELECT DISTINCT
	*
FROM 
	natures_staging;

-- Pokemon

-- Wonder Trades

-- The OOPS Section
-- DROP TABLE wonder_trades;
-- DROP TABLE teams;
-- DROP TABLE pokemon;
-- DROP TABLE natures;
-- DROP TABLE items;
-- DROP TABLE form_move;
-- DROP TABLE moves;
-- DROP TABLE forms;
-- DROP TABLE hatching;
-- DROP TABLE abilities;
-- DROP TABLE species;
-- DROP TABLE passwords;
-- DROP TABLE users;
-- DROP TABLE type_chart;
