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
INSERT
	forms (species_id, form_name, type_id, ability_1, ability_2, ability_h, hp, attack, defense, special_attack, special_defense, speed, total_stats, weight_lbs, height_in, description_1, description_2, class, percent_male, percent_female)
SELECT DISTINCT
	ndex, forme, type_id, 
    abilities1.ability_id as ability_1, 
    abilities2.ability_id as ability_2, 
    abilitiesH.ability_id as ability_h, 
    hp, attack, defense, spattack, spdefense, speed, total, 
	CAST(TRIM(TRAILING '.' FROM TRIM(REPLACE(weight, ' lbs', ''))) AS FLOAT) AS weight_lbs,
	(CAST(SUBSTRING_INDEX(height, '\'', 1) AS UNSIGNED) * 12) + (CAST(TRIM(TRAILING '\"' FROM SUBSTRING_INDEX(height, '\'', -1)) AS UNSIGNED)) AS height_in,
    dex1, dex2, class, percentmale, percentfemale
FROM
	pokemon_staging
LEFT JOIN abilities AS abilitiesH ON pokemon_staging.abilityH = abilitiesH.ability_name
LEFT JOIN abilities AS abilities2 ON pokemon_staging.ability2 = abilities2.ability_name
LEFT JOIN abilities AS abilities1 ON pokemon_staging.ability1 = abilities1.ability_name
INNER JOIN type_chart ON pokemon_staging.type1 = type_chart.primary_type AND (pokemon_staging.type2 = type_chart.secondary_type OR (pokemon_staging.type2 IS NULL AND type_chart.secondary_type IS NULL))
WHERE (pokemon_staging.ndex != 718 OR pokemon_staging.ability1 IS NOT NULL) AND (pokemon_staging.ndex != 774 OR pokemon_staging.dex1 IS NOT NULL); -- Remove Zygarde and Minior DUPS

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

