use final_project;
SELECT species_id
FROM species
WHERE species_name = "Snorlax";

SELECT form_id, form_name
FROM forms
WHERE species_id = 143;

SELECT nature_id, nature_name
FROM natures;

SELECT ability_id
FROM abilities
WHERE ability_name = "Air Lock";

INSERT INTO pokemon
(form_id, nickname, gender, nature_id, ability_id)
VALUES (65, "John", "M", 5, 4);

DELETE FROM pokemon WHERE pokemon_id = 1;

INSERT INTO users 
(username)
VALUES ("Testuser");

INSERT INTO teams
(user_id, team_name)
VALUES (1, "Team");

DELETE FROM teams WHERE team_id = 1;

UPDATE teams SET pokemon_1 = 8 WHERE team_id = 5;

SELECT *
FROM teams
WHERE team_id = 5;

SELECT p.nickname, p.gender, f.form_name, n.nature_name, a.ability_name
FROM pokemon p
JOIN forms f
ON f.form_id = p.form_id
JOIN natures n
ON n.nature_id = p.nature_id
JOIN abilities a
ON a.ability_id = p.ability_id
WHERE pokemon_id = 10;

