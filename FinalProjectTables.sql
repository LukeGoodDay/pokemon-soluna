USE final_project;

CREATE TABLE
	users(
		user_id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(30) UNIQUE NOT NULL
    );

CREATE TABLE
	user_auth(
		user_id INT UNIQUE NOT NULL,
        email VARCHAR(256) NOT NULL,
        hashed_password VARCHAR(256) NOT NULL,
		FOREIGN KEY (user_id) REFERENCES users(user_id)
	);

CREATE TABLE
	sessions(
		session_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        started DATETIME NOT NULL,
        ended DATETIME,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

CREATE TABLE
	activity_log(
		log_id INT PRIMARY KEY AUTO_INCREMENT,
        session_id INT NOT NULL,
        action_taken VARCHAR(30) NOT NULL,
        action_time DATETIME NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    );

CREATE TABLE
    type_chart(
		type_id INT PRIMARY KEY,
		primary_type ENUM('normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy') NOT NULL,
		secondary_type ENUM('normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy'),
		normal_mult FLOAT NOT NULL,
        fire_mult FLOAT NOT NULL,
        water_mult FLOAT NOT NULL,
        electric_mult FLOAT NOT NULL,
        grass_mult FLOAT NOT NULL,
        ice_mult FLOAT NOT NULL,
        fighting_mult FLOAT NOT NULL,
        poison_mult FLOAT NOT NULL,
        ground_mult FLOAT NOT NULL,
        flying_mult FLOAT NOT NULL,
        psychic_mult FLOAT NOT NULL,
        bug_mult FLOAT NOT NULL,
        rock_mult FLOAT NOT NULL,
        ghost_mult FLOAT NOT NULL,
        dragon_mult FLOAT NOT NULL,
        dark_mult FLOAT NOT NULL,
        steel_mult FLOAT NOT NULL,
        fairy_mult FLOAT NOT NULL
    );

CREATE TABLE
	species(
		species_id INT PRIMARY KEY,
        species_name VARCHAR(20) UNIQUE NOT NULL,
        preevolution INT,
        egg_group_1 ENUM('Amorphous','Bug','Ditto','Dragon','Fairy','Field','Flying','Grass','Human-Like','Mineral','Monster','Undiscovered','Water 1','Water 2','Water 3','Water 4') NOT NULL,
        egg_group_2 ENUM('Amorphous','Bug','Ditto','Dragon','Fairy','Field','Flying','Grass','Human-Like','Mineral','Monster','Undiscovered','Water 1','Water 2','Water 3','Water 4'),
        FOREIGN KEY (preevolution) REFERENCES species(species_id)
    );
    
CREATE TABLE
	abilities(
		ability_id INT PRIMARY KEY AUTO_INCREMENT,
		ability_name VARCHAR(30) UNIQUE NOT NULL,
        description VARCHAR(150) NOT NULL
    );

CREATE TABLE
	hatching(
		species_id INT PRIMARY KEY,
		steps INT NOT NULL,
        FOREIGN KEY (species_id) REFERENCES species(species_id)
    );

CREATE TABLE
	forms(
		form_id INT PRIMARY KEY AUTO_INCREMENT,
        species_id INT NOT NULL,
        form_name VARCHAR(30) UNIQUE NOT NULL,
        type_id INT,
        hp INT NOT NULL,
        attack INT NOT NULL,
        defense INT NOT NULL,
        special_attack INT NOT NULL,
        special_defense INT NOT NULL,
        speed INT NOT NULL,
        total_stats INT NOT NULL,
	    FOREIGN KEY (species_id) REFERENCES species(species_id),
	    FOREIGN KEY (type_id) REFERENCES type_chart(type_id)
    );
    
CREATE TABLE
	form_info(
		form_id INT PRIMARY KEY,
        ability_1 INT,
        ability_2 INT,
        ability_h INT,
        weight_lbs FLOAT NOT NULL,
        height_in INTEGER NOT NULL,
        description_1 VARCHAR(250),
		description_2 VARCHAR(250),
        class VARCHAR(30) NOT NULL,
        percent_male FLOAT,
        percent_female FLOAT,
	    FOREIGN KEY (form_id) REFERENCES forms(form_id),
        FOREIGN KEY (ability_1) REFERENCES abilities(ability_id),
        FOREIGN KEY (ability_2) REFERENCES abilities(ability_id),
        FOREIGN KEY (ability_h) REFERENCES abilities(ability_id)
    );
    
CREATE TABLE
	images(
		image_id INT PRIMARY KEY AUTO_INCREMENT,
		form_id INT NOT NULL,
        image_name VARCHAR(30) NOT NULL,
        image_path VARCHAR(256) NOT NULL,
        FOREIGN KEY (form_id) REFERENCES forms(form_id)
    );

CREATE TABLE
	moves(
		move_id INT PRIMARY KEY AUTO_INCREMENT,
		move_name VARCHAR(30) UNIQUE NOT NULL,
        description VARCHAR(250) NOT NULL,
        type_id INT NOT NULL,
        category ENUM('physical', 'status', 'special'),
        power INT,
        accuracy INT,
        pp INT NOT NULL,
        z_effect VARCHAR(65) NOT NULL,
        priority INT NOT NULL,
        crit INT NOT NULL,
	    FOREIGN KEY (type_id) REFERENCES type_chart(type_id)
    );

CREATE TABLE
	form_move(
		form_move_id INTEGER PRIMARY KEY AUTO_INCREMENT,
		form_id INT,
        move_id INT,
        get_from VARCHAR(5),
        FOREIGN KEY (form_id) REFERENCES forms(form_id),
        FOREIGN KEY (move_id) REFERENCES moves(move_id)
    );
    
CREATE TABLE
	items(
		item_id INT PRIMARY KEY AUTO_INCREMENT,
		item_name VARCHAR(20) UNIQUE NOT NULL,
        description VARCHAR(250) NOT NULL
    );

CREATE TABLE
	natures(
		nature_id INT PRIMARY KEY AUTO_INCREMENT,
		nature_name VARCHAR(20) UNIQUE NOT NULL,
        attack_mult FLOAT NOT NULL,
        special_attack_mult FLOAT NOT NULL,
        defense_mult FLOAT NOT NULL,
        special_defense_mult FLOAT NOT NULL,
        speed_mult FLOAT NOT NULL
    );
    
CREATE TABLE
	pokemon(
		pokemon_id INT PRIMARY KEY AUTO_INCREMENT,
        form_id INT NOT NULL,
        nickname VARCHAR(12),
        gender ENUM('M','F'),
        nature_id INT NOT NULL,
        ability_id INT NOT NULL,
        item_id INT,
        move_1 INT,
        move_2 INT,
        move_3 INT,
        move_4 INT,
        FOREIGN KEY (form_id) REFERENCES forms(form_id),
        FOREIGN KEY (nature_id) REFERENCES natures(nature_id),
        FOREIGN KEY (ability_id) REFERENCES abilities(ability_id),
        FOREIGN KEY (item_id) REFERENCES items(item_id),
        FOREIGN KEY (move_1) REFERENCES moves(move_id),
        FOREIGN KEY (move_2) REFERENCES moves(move_id),
        FOREIGN KEY (move_3) REFERENCES moves(move_id),
        FOREIGN KEY (move_4) REFERENCES moves(move_id)
    );

CREATE TABLE
	teams(
		team_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        team_name VARCHAR(30) NOT NULL,
        pokemon_1 INT,
        pokemon_2 INT,
        pokemon_3 INT,
        pokemon_4 INT,
        pokemon_5 INT,
        pokemon_6 INT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (pokemon_1) REFERENCES pokemon(pokemon_id),
        FOREIGN KEY (pokemon_2) REFERENCES pokemon(pokemon_id),
        FOREIGN KEY (pokemon_3) REFERENCES pokemon(pokemon_id),
        FOREIGN KEY (pokemon_4) REFERENCES pokemon(pokemon_id),
        FOREIGN KEY (pokemon_5) REFERENCES pokemon(pokemon_id),
        FOREIGN KEY (pokemon_6) REFERENCES pokemon(pokemon_id)
    );

CREATE TABLE
    wonder_trades(
		trade_id INT PRIMARY KEY AUTO_INCREMENT,
        trade_time DATETIME NOT NULL,
        form_id INT NOT NULL,
        gender ENUM('M','F'),
        nature_id INT,
        FOREIGN KEY (form_id) REFERENCES forms(form_id),
        FOREIGN KEY (nature_id) REFERENCES natures(nature_id)
    );

CREATE TABLE
    challenges(
		challenge_id INT PRIMARY KEY AUTO_INCREMENT,
        description VARCHAR(256)
    );

CREATE TABLE
    pokemon_popularity(
		form_id INT,
        count INT,
        rank INT,
        total_percentage double,
        FOREIGN KEY (form_id) REFERENCES forms(form_id)
    );

CREATE TABLE
    type_popularity(
		type_id INT,
        count INT,
        rank INT,
        total_percentage double,
        FOREIGN KEY (type_id) REFERENCES type_chart(type_id)
    );

CREATE TABLE
    item_popularity(
		item_id INT,
        count INT,
        rank INT,
        total_percentage double,
        FOREIGN KEY (item_id) REFERENCES items(items_id)
    );

CREATE TABLE
    move_popularity(
		move_id INT,
        count INT,
        rank INT,
        total_percentage double,
        FOREIGN KEY (move_id) REFERENCES moves(move_id)
    );