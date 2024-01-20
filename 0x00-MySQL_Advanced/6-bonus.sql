-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student

DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT,
                          IN project_name VARCHAR(255),
                          IN score INT)
BEGIN
    -- Declaring projects_id's type
    DECLARE projects_id INT;
    -- Checking if project_name already exists
    SELECT id INTO projects_id FROM projects WHERE name = project_name;

    IF projects_id IS NULL THEN
        -- Inserting New Project if it doesn't exist
        INSERT INTO projects (name) VALUES (project_name);
        SET projects_id = LAST_INSERT_ID();
    END IF;
    -- Inserting new scores into corrections table
    INSERT INTO corrections VALUES (user_id, projects_id, score);
END $$
DELIMITER ;
