
var express   =    require("express");
var mysql     =    require('mysql');
var app       =    express();

var pool      =    mysql.createPool({
    connectionLimit : 100, //important
    host     : 'mysql://mysql:3306/',
    user     : 'user2HA',
    password : 'eBR1gtKtw8VwD2Ad',
    database : 'sampledb',
    debug    :  false
});







const TelegramBot = require('node-telegram-bot-api');

// replace the value below with the Telegram token you receive from @BotFather
const token = '389085214:AAGjB1U46UCeuAiUn09hqDpBUEA-UIERR0s';

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, {polling: true});

// Matches "/echo [whatever]"
// bot.onText(/\/echo (.+)/, (msg, match) => {
//   // 'msg' is the received Message from Telegram
//   // 'match' is the result of executing the regexp above on the text content
//   // of the message

//   const chatId = msg.chat.id;
//   const resp = match[1]; // the captured "whatever"

//   // send back the matched "whatever" to the chat
//   bot.sendMessage(chatId, resp);
// });

bot.onText(/\/echo (.+)/, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  var resp = match[1]; // the captured "whatever"
  const chatId = msg.chat.id;
  
  pool.getConnection(function(err,connection){
    if (err) {
      res.json({"code" : 100, "status" : "Error in connection database"});
      return;
      bot.sendMessage(chatId, "code 100, status: Error in connection database");
    }   
  


  }

  // send back the matched "whatever" to the chat
  bot.sendMessage(chatId, resp);
});


// Listen for any kind of message. There are different kinds of
// messages.
bot.on('message', (msg) => {
  const chatId = msg.chat.id;

  // send a message to the chat acknowledging receipt of their message
  bot.sendMessage(chatId, 'Received your message');
});




