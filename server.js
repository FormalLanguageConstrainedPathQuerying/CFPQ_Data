const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const dataRoutes = require('./routes/database');

const app = express();

app.use(cors());

app.use('/api', dataRoutes);

app.get('/config', (req, res) => {
  const configPath = path.join(__dirname, 'config', 'config.json');
  fs.readFile(configPath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading config file:', err);
      res.status(500).json({ error: 'Internal server error' });
      return;
    }
    const config = JSON.parse(data);
    res.json(config);
  });
});

app.use(express.static(__dirname));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Сервер запущен на порту ${PORT}`);
});
