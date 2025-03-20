# Azure Function App (timer triggered)

BAIS:3400 Cloud Computing

![Azure Functions badge](https://img.shields.io/badge/Azure_Functions-0062AD?style=for-the-badge&logo=azure-functions&logoColor=white) ![Python badge](https://img.shields.io/static/v1?message=python&logo=python&labelColor=5c5c5c&color=3776AB&logoColor=white&label=%20&style=for-the-badge)

## Summary

[Azure Function app](https://azure.microsoft.com/en-us/products/functions)

[Coinmarketcap](https://coinmarketcap.com/)
[Coinmarketcap API](https://coinmarketcap.com/api/)

[Azure Functions documentation](https://learn.microsoft.com/en-us/azure/azure-functions/)
[Microsoft Learn - Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview?pivots=programming-language-python)

## Prerequisites

### MySQL database to hold cryptocurrency prices

Azure MySQL Database
MySQL v8

Using [MySQL Workbench](https://www.mysql.com/products/workbench/)
Create a database and table

```
DROP DATABASE IF EXISTS hw9b;

CREATE DATABASE hw9b;
USE hw9b;

DROP TABLE IF EXISTS `crypto_prices`;

CREATE TABLE crypto_prices (
priceId int NOT NULL AUTO_INCREMENT,
readTime TIMESTAMP NOT NULL,
hawkid varchar(128) NOT NULL,
cryptocurrency varchar(128) NOT NULL,
price DECIMAL(9,2) NOT NULL,
last_updated TIMESTAMP NOT NULL,
PRIMARY KEY (priceId)
)
AUTO_INCREMENT=1;

```

Create a user to connect and write the data

```
DROP USER 'hw9b_app'@'%';

CREATE USER 'hw9b_app'@'%' IDENTIFIED BY 'sdf234ser85eieonm3m;oi)(EW*s2CQ2e';

GRANT SELECT, INSERT, DELETE, UPDATE ON hw9b.crypto_prices TO 'hw9b_app'@'%';

FLUSH PRIVILEGES;
```

Log in as the new user and test

```
USE hw9b;

INSERT INTO crypto_prices (`readTime`, `hawkid`, `cryptocurrency`, `price`, `last_updated`) VALUES (CURRENT_TIMESTAMP(), 'colbert', 'btc', 19999.99, CURRENT_TIMESTAMP);

SELECT * FROM crypto_prices;
```

### Azure Functions Core Tools

https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python

### Azurite for local storage

https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio-code%2Cblob-storage

## Azure Function app structure

├── README.md
├── crypto*function
│   ├── \_\_\_init*\_\_.py
│   └── function.json
├── host.json
├── local.settings.json
└── requirements.txt

Sample local.settings.json

```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "COINMARKETCAP_API_KEY": " put your API key here ",
    "MYSQL_HOST": " put the url to your database server here ",
    "MYSQL_USER": " put your db username here ",
    "MYSQL_PASSWORD": " put your db password here ",,
    "MYSQL_DATABASE": " put your db name here ",
    "MYSQL_PORT": "3306"
  }
}
```

## Testing locally

## Executing on Azure

### Setting environment variables for your Azure Function app

\
