var TelegramBot = require('node-telegram-bot-api');

var token = '389085214:AAGjB1U46UCeuAiUn09hqDpBUEA-UIERR0s';
// Setup polling way
var bot = new TelegramBot(token, {polling: true});

// Matches /echo [whatever]
bot.onText(/\/echo (.+)/, function (msg, match) {
  var fromId = msg.from.id;
  var resp = match[1];
  bot.sendMessage(fromId, resp);
});

// Any kind of message
bot.on('message', function (msg) {
  var chatId = msg.chat.id;
  // photo can be: a file path, a stream or a Telegram file_id
  var photo = 'cats.png';
  bot.sendPhoto(chatId, photo, {caption: 'Lovely kittens'});
});

bot.onText(/\/help/, function(msg, match) {
  var fromId = msg.from.id;
  bot.sendMessage(fromId, "This spectacular bot just have one single command.\n/insult - Insult you.");
});