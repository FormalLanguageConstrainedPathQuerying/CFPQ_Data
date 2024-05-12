const express = require('express');
const router = express.Router();
const { Pool } = require('pg');
const secrets = require('../config/config.json');

const pool = new Pool({
  user: secrets.db.user,
  host: secrets.db.host,
  database: secrets.db.database,
  password: secrets.db.password,
  port: secrets.db.port
});

router.get('/getdata', async (req, res) => {
  try {
    const client = await pool.connect();
    const query = `
      SELECT graphs.*, grammars.*
      FROM graphs
      JOIN graph_grammars ON graphs.id = graph_grammars.graph_id
      JOIN grammars ON graph_grammars.grammar_id = grammars.id
    `;
    const result = await client.query(query);

    const data = result.rows.map(row => ({
      Graph: row.graph,
      NumNodes: row.num_nodes,
      NumEdges: row.num_edges,
      DownloadLink: row.download_link,
      Grammar: row.grammar,
      Class: row.class,
      Kind: row.kind,
      GrammarLink: row.examples
    }));

    res.json(data);

    client.release();
  } catch (err) {
    console.error('Error fetching data:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
