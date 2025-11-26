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
	forms(species_id, form_name, type_id, hp, attack, defense, special_attack, special_defense, speed, total_stats)
SELECT DISTINCT
	ndex, forme, type_id, hp, attack, defense, spattack, spdefense, speed, total
FROM
	pokemon_staging
INNER JOIN type_chart ON pokemon_staging.type1 = type_chart.primary_type AND (pokemon_staging.type2 = type_chart.secondary_type OR (pokemon_staging.type2 IS NULL AND type_chart.secondary_type IS NULL))
WHERE (pokemon_staging.ndex != 718 OR pokemon_staging.ability1 IS NOT NULL) AND (pokemon_staging.ndex != 774 OR pokemon_staging.dex1 IS NOT NULL); -- Remove Zygarde and Minior DUPS

-- Form Info
INSERT
	form_info(form_id, ability_1, ability_2, ability_h, weight_lbs, height_in, description_1, description_2, class, percent_male, percent_female)
SELECT DISTINCT
	form_id,
	abilities1.ability_id as ability_1, 
    abilities2.ability_id as ability_2, 
    abilitiesH.ability_id as ability_h,
    CAST(TRIM(TRAILING '.' FROM TRIM(REPLACE(weight, ' lbs', ''))) AS FLOAT) AS weight_lbs,
	(CAST(SUBSTRING_INDEX(height, '\'', 1) AS UNSIGNED) * 12) + (CAST(TRIM(TRAILING '\"' FROM SUBSTRING_INDEX(height, '\'', -1)) AS UNSIGNED)) AS height_in,
    dex1, dex2, class, percentmale, percentfemale
FROM
	pokemon_staging
LEFT JOIN abilities AS abilitiesH ON pokemon_staging.abilityH = abilitiesH.ability_name
LEFT JOIN abilities AS abilities2 ON pokemon_staging.ability2 = abilities2.ability_name
LEFT JOIN abilities AS abilities1 ON pokemon_staging.ability1 = abilities1.ability_name
INNER JOIN forms ON forms.form_name = pokemon_staging.forme
WHERE (pokemon_staging.ndex != 718 OR pokemon_staging.ability1 IS NOT NULL) AND (pokemon_staging.ndex != 774 OR pokemon_staging.dex1 IS NOT NULL); -- Remove Zygarde and Minior DUPS

-- Moves
INSERT
	moves(move_name, description, type_id, category, power, accuracy, pp, z_effect, priority, crit)
SELECT DISTINCT
	move,
	description,
	type_id,
    CASE
		WHEN category = '#N/A' THEN NULL
        ELSE category
	END AS optional_category,
    CASE
        WHEN power = '—' THEN NULL
        ELSE CAST(power AS UNSIGNED)
    END AS optional_power,
    CASE
        WHEN accuracy = '—' THEN NULL
        ELSE CAST(TRIM(TRAILING '%' FROM accuracy) AS UNSIGNED)
    END AS optional_accuracy,
	pp,
	zeffect,
	priority,
	crit
FROM
	move_staging
INNER JOIN type_chart ON move_staging.type = type_chart.primary_type AND type_chart.secondary_type IS NULL;

-- Form_Move
CREATE TABLE
	temp_move_staging(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
        renamed_pokemon VARCHAR(50) NOT NULL,
        move VARCHAR(30) NOT NULL,
        from_where VARCHAR(30) NOT NULL
);

INSERT
	temp_move_staging (renamed_pokemon, move, from_where)
SELECT
	t.renamed_pokemon,
    CASE
		WHEN t.move_value LIKE '%Safe Guard' THEN 'Safeguard' -- Data has a typo
		ELSE TRIM(SUBSTRING_INDEX(t.move_value, ' - ', -1)) 
    END AS move,
	TRIM(SUBSTRING_INDEX(t.move_value, ' - ', 1)) AS from_where
FROM
(
	SELECT
		*,
		CASE
			WHEN forme = 'Raticate (2)' THEN 'Raticate (1)'
			WHEN forme = 'Castform' THEN 'Castform (Normal)'
			WHEN forme = 'Burmy' THEN 'Burmy (ALL)'
			WHEN forme = 'Cherrim' THEN 'Cherrim (Overcast Form)'
			WHEN forme = 'Gastrodon' THEN 'Gastrodon (West Sea)'
			WHEN forme = 'Rotom' THEN 'Rotom (Rotom)'
			WHEN forme = 'Arceus' THEN 'Arceus (ALL)'
			WHEN forme = 'Basculin' THEN 'Basculin (Red-Striped Form)'
			WHEN forme = 'Darmanitan' THEN 'Darmanitan (Standard Mode)'
			WHEN forme = 'Deerling' THEN 'Deerling (ALL)'
			WHEN forme = 'Sawsbuck' THEN 'Sawsbuck (ALL)'
			WHEN forme = 'Tornadus' THEN 'Tornadus (Incarnate Forme)'
			WHEN forme = 'Thundurus' THEN 'Thundurus (Incarnate Forme)'
			WHEN forme = 'Landorus' THEN 'Landorus (Incarnate Forme)'
			WHEN forme = 'Kyurem' THEN 'Kyurem (Kyurem)'
			WHEN forme = 'Keldeo' THEN 'Keldeo (Ordinary Form)'
			WHEN forme = 'Genesect' THEN 'Genesect (Genesect)'
			WHEN forme = 'Vivillon' THEN 'Vivillon (ALL)'
			WHEN forme = 'Flabébé' THEN 'Flabébé (ALL)'
			WHEN forme = 'Floette' THEN 'Floette (Red Flower)'
			WHEN forme = 'Florges' THEN 'Florges (ALL)'
			WHEN forme = 'Furfrou' THEN 'Furfrou (Natural Form)'
			WHEN forme = 'Aegislash' THEN 'Aegislash (Shield Forme)'
			WHEN forme = 'Xerneas' THEN 'Xerneas (ALL)'
			WHEN forme = 'Hoopa' THEN 'Hoopa (Hoopa Confined)'
			WHEN forme = 'Oricorio' THEN 'Oricorio (Baile Style)'
			WHEN forme = 'Wishiwashi' THEN 'Wishiwashi (Solo Form)'
			WHEN forme = 'Silvally' THEN 'Silvally (ALL)'
			WHEN forme = 'Minior' THEN 'Minior (Meteor Form)'
			WHEN forme = 'Mimikyu' THEN 'Mimikyu (Disguised Form)'
			ELSE forme
		END AS renamed_pokemon
	FROM
		moveset_staging
	WHERE forme != 'Zygarde' -- Cut all problamatic ones
) AS ms
CROSS JOIN LATERAL
(
	VALUES 
	ROW(renamed_pokemon, ms.move1), ROW(renamed_pokemon, ms.move2), ROW(renamed_pokemon, ms.move3), ROW(renamed_pokemon, ms.move4), ROW(renamed_pokemon, ms.move5), ROW(renamed_pokemon, ms.move6), ROW(renamed_pokemon, ms.move7), ROW(renamed_pokemon, ms.move8), ROW(renamed_pokemon, ms.move9), ROW(renamed_pokemon, ms.move10),
	ROW(renamed_pokemon, ms.move11), ROW(renamed_pokemon, ms.move12), ROW(renamed_pokemon, ms.move13), ROW(renamed_pokemon, ms.move14), ROW(renamed_pokemon, ms.move15), ROW(renamed_pokemon, ms.move16), ROW(renamed_pokemon, ms.move17), ROW(renamed_pokemon, ms.move18), ROW(renamed_pokemon, ms.move19), ROW(renamed_pokemon, ms.move20),
	ROW(renamed_pokemon, ms.move21), ROW(renamed_pokemon, ms.move22), ROW(renamed_pokemon, ms.move23), ROW(renamed_pokemon, ms.move24), ROW(renamed_pokemon, ms.move25), ROW(renamed_pokemon, ms.move26), ROW(renamed_pokemon, ms.move27), ROW(renamed_pokemon, ms.move28), ROW(renamed_pokemon, ms.move29), ROW(renamed_pokemon, ms.move30),
	ROW(renamed_pokemon, ms.move31), ROW(renamed_pokemon, ms.move32), ROW(renamed_pokemon, ms.move33), ROW(renamed_pokemon, ms.move34), ROW(renamed_pokemon, ms.move35), ROW(renamed_pokemon, ms.move36), ROW(renamed_pokemon, ms.move37), ROW(renamed_pokemon, ms.move38), ROW(renamed_pokemon, ms.move39), ROW(renamed_pokemon, ms.move40),
	ROW(renamed_pokemon, ms.move41), ROW(renamed_pokemon, ms.move42), ROW(renamed_pokemon, ms.move43), ROW(renamed_pokemon, ms.move44), ROW(renamed_pokemon, ms.move45), ROW(renamed_pokemon, ms.move46), ROW(renamed_pokemon, ms.move47), ROW(renamed_pokemon, ms.move48), ROW(renamed_pokemon, ms.move49), ROW(renamed_pokemon, ms.move50),
	ROW(renamed_pokemon, ms.move51), ROW(renamed_pokemon, ms.move52), ROW(renamed_pokemon, ms.move53), ROW(renamed_pokemon, ms.move54), ROW(renamed_pokemon, ms.move55), ROW(renamed_pokemon, ms.move56), ROW(renamed_pokemon, ms.move57), ROW(renamed_pokemon, ms.move58), ROW(renamed_pokemon, ms.move59), ROW(renamed_pokemon, ms.move60),
	ROW(renamed_pokemon, ms.move61), ROW(renamed_pokemon, ms.move62), ROW(renamed_pokemon, ms.move63), ROW(renamed_pokemon, ms.move64), ROW(renamed_pokemon, ms.move65), ROW(renamed_pokemon, ms.move66), ROW(renamed_pokemon, ms.move67), ROW(renamed_pokemon, ms.move68), ROW(renamed_pokemon, ms.move69), ROW(renamed_pokemon, ms.move70),
	ROW(renamed_pokemon, ms.move71), ROW(renamed_pokemon, ms.move72), ROW(renamed_pokemon, ms.move73), ROW(renamed_pokemon, ms.move74), ROW(renamed_pokemon, ms.move75), ROW(renamed_pokemon, ms.move76), ROW(renamed_pokemon, ms.move77), ROW(renamed_pokemon, ms.move78), ROW(renamed_pokemon, ms.move79), ROW(renamed_pokemon, ms.move80),
	ROW(renamed_pokemon, ms.move81), ROW(renamed_pokemon, ms.move82), ROW(renamed_pokemon, ms.move83), ROW(renamed_pokemon, ms.move84), ROW(renamed_pokemon, ms.move85), ROW(renamed_pokemon, ms.move86), ROW(renamed_pokemon, ms.move87), ROW(renamed_pokemon, ms.move88), ROW(renamed_pokemon, ms.move89), ROW(renamed_pokemon, ms.move90),
	ROW(renamed_pokemon, ms.move91), ROW(renamed_pokemon, ms.move92), ROW(renamed_pokemon, ms.move93), ROW(renamed_pokemon, ms.move94), ROW(renamed_pokemon, ms.move95), ROW(renamed_pokemon, ms.move96), ROW(renamed_pokemon, ms.move97), ROW(renamed_pokemon, ms.move98), ROW(renamed_pokemon, ms.move99), ROW(renamed_pokemon, ms.move100),
	ROW(renamed_pokemon, ms.move101), ROW(renamed_pokemon, ms.move102), ROW(renamed_pokemon, ms.move103), ROW(renamed_pokemon, ms.move104), ROW(renamed_pokemon, ms.move105), ROW(renamed_pokemon, ms.move106), ROW(renamed_pokemon, ms.move107), ROW(renamed_pokemon, ms.move108), ROW(renamed_pokemon, ms.move109), ROW(renamed_pokemon, ms.move110),
	ROW(renamed_pokemon, ms.move111), ROW(renamed_pokemon, ms.move112), ROW(renamed_pokemon, ms.move113), ROW(renamed_pokemon, ms.move114), ROW(renamed_pokemon, ms.move115), ROW(renamed_pokemon, ms.move116), ROW(renamed_pokemon, ms.move117), ROW(renamed_pokemon, ms.move118), ROW(renamed_pokemon, ms.move119), ROW(renamed_pokemon, ms.move120),
	ROW(renamed_pokemon, ms.move121), ROW(renamed_pokemon, ms.move122), ROW(renamed_pokemon, ms.move123), ROW(renamed_pokemon, ms.move124), ROW(renamed_pokemon, ms.move125), ROW(renamed_pokemon, ms.move126), ROW(renamed_pokemon, ms.move127), ROW(renamed_pokemon, ms.move128), ROW(renamed_pokemon, ms.move129), ROW(renamed_pokemon, ms.move130),
	ROW(renamed_pokemon, ms.move131), ROW(renamed_pokemon, ms.move132), ROW(renamed_pokemon, ms.move133), ROW(renamed_pokemon, ms.move134), ROW(renamed_pokemon, ms.move135), ROW(renamed_pokemon, ms.move136), ROW(renamed_pokemon, ms.move137), ROW(renamed_pokemon, ms.move138), ROW(renamed_pokemon, ms.move139), ROW(renamed_pokemon, ms.move140),
	ROW(renamed_pokemon, ms.move141), ROW(renamed_pokemon, ms.move142), ROW(renamed_pokemon, ms.move143), ROW(renamed_pokemon, ms.move144), ROW(renamed_pokemon, ms.move145), ROW(renamed_pokemon, ms.move146), ROW(renamed_pokemon, ms.move147), ROW(renamed_pokemon, ms.move148), ROW(renamed_pokemon, ms.move149), ROW(renamed_pokemon, ms.move150),
	ROW(renamed_pokemon, ms.move151), ROW(renamed_pokemon, ms.move152), ROW(renamed_pokemon, ms.move153), ROW(renamed_pokemon, ms.move154), ROW(renamed_pokemon, ms.move155), ROW(renamed_pokemon, ms.move156), ROW(renamed_pokemon, ms.move157), ROW(renamed_pokemon, ms.move158), ROW(renamed_pokemon, ms.move159), ROW(renamed_pokemon, ms.move160), 
	ROW(renamed_pokemon, ms.move161), ROW(renamed_pokemon, ms.move162), ROW(renamed_pokemon, ms.move163), ROW(renamed_pokemon, ms.move164), ROW(renamed_pokemon, ms.move165), ROW(renamed_pokemon, ms.move166), ROW(renamed_pokemon, ms.move167), ROW(renamed_pokemon, ms.move168), ROW(renamed_pokemon, ms.move169), ROW(renamed_pokemon, ms.move170),
	ROW(renamed_pokemon, ms.move171), ROW(renamed_pokemon, ms.move172), ROW(renamed_pokemon, ms.move173), ROW(renamed_pokemon, ms.move174)
) AS t (renamed_pokemon, move_value)
WHERE
	t.move_value IS NOT NULL;

INSERT
	form_move (form_id, move_id, get_from)
SELECT DISTINCT
	form_id, 
	move_id,
	from_where
FROM
	temp_move_staging
LEFT JOIN moves ON temp_move_staging.move = moves.move_name
LEFT JOIN forms ON temp_move_staging.renamed_pokemon = forms.form_name OR 
(temp_move_staging.renamed_pokemon LIKE '%(ALL)' AND forms.form_name LIKE REPLACE(temp_move_staging.renamed_pokemon, ' (ALL)', '%'));

DROP TABLE temp_move_staging;

-- Items
INSERT
	items(item_name, description)
SELECT DISTINCT 
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

-- Wonder Trades
INSERT
	wonder_trades(trade_time, form_id, gender, nature_id)
SELECT
	STR_TO_DATE(CONCAT(`Date`, ' ' ,`Time`), '%c/%d/%y %H:%i') AS date_time,
    forms.form_id,
    CASE
        WHEN `Gender` = 'N' THEN NULL
        ELSE `Gender`
    END AS optional_gender,
    nature_id
FROM
(
	SELECT
		*,
        CASE
			WHEN `Pokemon` LIKE 'A.%' THEN CONCAT(REPLACE(`Pokemon`, 'A.', ''), ' (Alola Form)')
            WHEN `Pokemon` = 'Oricorio' THEN 'Oricorio (Baile Style)'
            WHEN `Pokemon` = 'Mimikyu' THEN 'Mimikyu (Disguised Form)'
            WHEN `Pokemon` = 'Shellos' THEN 'Shellos (East Sea)'
            WHEN `Pokemon` = 'Minior' THEN 'Minior (Meteor Form)'
            WHEN `Pokemon` = 'Gastrodon' THEN 'Gastrodon (East Sea)'
            WHEN `Pokemon` = 'Wishiwashi' THEN 'Wishiwashi (Solo Form)'
			ELSE `Pokemon`
		END AS renamed_pokemon
	FROM
		wonder_trade_staging
) AS wt_staging
INNER JOIN natures ON wt_staging.`Nature` = natures.nature_name
INNER JOIN forms ON wt_staging.renamed_pokemon = forms.form_name;

-- Pokemon Popularity
INSERT
	pokemon_popularity
SELECT
	form_id, 0, 1, 0.0
FROM
	forms;

-- Type Popularity
INSERT
	type_popularity
SELECT
	type_id, 0, 1, 0.0
FROM
	type_chart;

-- Item Popularity
INSERT
	item_popularity
SELECT
	item_id, 0, 1, 0.0
FROM
	items;

-- Move Popularity
INSERT
	move_popularity
SELECT
	move_id, 0, 1, 0.0
FROM
	moves;
