CREATE TABLE home_price(
             TransactionId CHAR(50) PRIMARY KEY NOT NULL,
             Price INT NOT NULL,
             Date CHAR(25),
             Zip CHAR(25),
             Type CHAR(1),
             NewBuild CHAR(1),
             EstateType CHAR(1),
             PAON VARCHAR(50),
             SAON VARCHAR(50),
             Street VARCHAR(50),
             Locality VARCHAR(50),
             Town VARCHAR(50),
             District VARCHAR(50),
             County VARCHAR(50),
             TransCategory VARCHAR(50),
             RecStatus VARCHAR(50)
             );
