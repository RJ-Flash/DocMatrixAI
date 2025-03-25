export default {
  apps: [{
    name: 'docmatrix-api',
    script: './app.js',
    instances: 'max',
    execMode: 'cluster',
    watch: false,
    maxMemoryRestart: '1G',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    envProduction: {
      NODE_ENV: 'production'
    },
    envDevelopment: {
      NODE_ENV: 'development',
      PORT: 3001
    },
    envTest: {
      NODE_ENV: 'test',
      PORT: 3002
    },
    errorFile: './logs/error.log',
    outFile: './logs/out.log',
    logFile: './logs/combined.log',
    time: true,
    mergeLogs: true,
    logDateFormat: 'YYYY-MM-DD HH:mm:ss Z',
    maxLogs: '10d',
    autorestart: true,
    watchOptions: {
      followSymlinks: false
    },
    killTimeout: 3000,
    waitReady: true,
    listenTimeout: 10000,
    expBackoffRestartDelay: 100,
    maxRestarts: 10,
    minUptime: '5s'
  }]
};
