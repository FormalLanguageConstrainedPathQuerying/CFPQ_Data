const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const oauth = require('oauth').OAuth2;

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

const configPath = path.join(__dirname, 'config', 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const clientId = config.clientId;
const clientSecret = config.clientSecret;
const redirectUri = config.redirectUri;
const oauth2 = new oauth(clientId, clientSecret, 'https://github.com/', 'login/oauth/authorize', 'login/oauth/access_token');

app.get('/auth/github', (req, res) => {
  res.redirect(oauth2.getAuthorizeUrl({
    redirect_uri: redirectUri,
    scope: 'repo'
  }));
});

app.get('/auth/callback', async (req, res) => {
  const code = req.query.code;

  try {
    const response = await axios.post('https://github.com/login/oauth/access_token', {
      client_id: clientId,
      client_secret: clientSecret,
      code: code,
    }, {
      headers: {
        'Accept': 'application/json'
      }
    });

    const accessToken = response.data.access_token;
    if (accessToken) {
      res.redirect(`/?access_token=${accessToken}`);
    } else {
      res.status(500).json({ error: 'Failed to obtain access token' });
    }
  } catch (error) {
    console.error('Error exchanging code for access token:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.use(express.static(__dirname));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
