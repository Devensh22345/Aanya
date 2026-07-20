module.exports = {
  apps: [
    {
      name: "url-replace-bot",
      script: "/light-bot/url-replace/bot.py",
      interpreter: "/light-bot/url-replace/venv/bin/python"
    },
    {
      name: "url-replace-bots",
      script: "/light-bot/url-replace/bots.py",
      interpreter: "/light-bot/url-replace/venv/bin/python"
    }
  ]
};
