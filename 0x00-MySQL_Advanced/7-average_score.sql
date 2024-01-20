-- a SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN users_id INT)
BEGIN
	DECLARE sum_score INT;
	SELECT SUM(score) INTO sum_score
    FROM corrections
    WHERE user_id = users_id;
    UPDATE users
    SET
		average_score = sum_score / (SELECT COUNT(score) FROM corrections WHERE user_id = users_id)
	WHERE id = users_id;
END $$
DELIMITER ;
