-- Créer la base de données "qcm" s'il n'existe pas déjà
CREATE DATABASE IF NOT EXISTS qcm;

-- Utiliser la base de données "qcm"
USE qcm;

-- Créer la table quiz_questions
CREATE TABLE IF NOT EXISTS quiz_questions (
  id INT NOT NULL AUTO_INCREMENT,
  question TEXT,
  option1 TEXT,
  option2 TEXT,
  option3 TEXT,
  option4 TEXT,
  correct_answer TEXT,
  PRIMARY KEY (id)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insérer des données dans la table quiz_questions
INSERT INTO quiz_questions VALUES 
(1,'Quelle application utilise-t-on pour créer une image docker','Docker','Mysql','Python','Java','Docker'),
(2,'Choisir la méthode d\'apprentissage qui est non supervisée parmi les options suivantes.','Decision Trees','SVM','Random Forests','K-means','K-means');

-- Créer la table resultat
CREATE TABLE IF NOT EXISTS resultat (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) DEFAULT NULL,
  score INT DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insérer des données dans la table resultat
INSERT INTO resultat VALUES (1,'10',0),(2,'10',50),(3,'10',100),(4,'10',100);

-- Créer la table users
CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(255) DEFAULT NULL,
  user_type VARCHAR(20) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insérer des données dans la table users
INSERT INTO users VALUES 
(1,'Admin','pbkdf2:sha256:600000$QmStjS7jay3Vgts6$dfb3692061eb9181e3996036f9289366cffb5300c8530fadc06b4d37d1e29b','admin'),
(2,'Guo','pbkdf2:sha256:600000$MSDjVSMx5CTzH48D$cfdec0a72da1819470abf5cda86521621a40b5daa3e49d9e30e6feb14be28baf','joueur');
