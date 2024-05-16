#!/usr/bin/env bash
airflow db init
airflow users create --username admin --password admin --firstname Vera --lastname Zhao --role Admin --email verabunny321@gmail.com
airflow webserver -p 8080
airflow scheduler