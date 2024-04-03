require('dotenv').config();
const express = require('express');
const app = express();
const {Pool, Client} = require('pg');

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_DBNAME,
  password: process.env.DB_PASS,
  port: process.env.DB_PORT,
});

const port = process.env.EXPRESSPORT || 8081;

function insertData() {
  setTimeout(function () {
    var date = new Date();
    var now =
      '' +
      date.getDate() +
      '/' +
      (date.getMonth() + 1) +
      '/' +
      date.getFullYear() +
      ' ' +
      date.getHours() +
      ':' +
      date.getMinutes() +
      ':' +
      date.getSeconds();
    var geom = `SRID=4326;POINT(${103.860579 + Math.random() * 0.1} ${
      1.284752 + Math.random() * 0.01
    })`;

    pool.query(
      //"INSERT INTO map.assets_location (asset_id, last_update, geom) VALUES ($1::integer, TO_TIMESTAMP($2::text, 'DD/MM/YY HH24:MI:SS'), GeomFromEWKT($3::text))",
      "UPDATE map.assets_location SET asset_id = $1, last_update = TO_TIMESTAMP($2::text, 'DD/MM/YY HH24:MI:SS'), geom = GeomFromEWKT($3::text) WHERE asset_id = 2;",
      [2, now, geom],
      (err, res) => {
        console.log(err, res);
      }
    );

    insertData();
  }, 5000);
}

insertData();

app.use('/', express.static('public'));
app.listen(port, () =>
  console.log(`Running a server listing on port ${port}...`)
);
