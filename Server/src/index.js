import { WebSocketServer } from "ws";
import { createServer } from "https";
import { readFileSync } from "fs";
import net from "net";

let game = null;

const initGame = () => {
  game = {
    players: 0,
    running: false,
    socket: null,
    clients: [null, null],
  };
};

initGame();

const broacastToClients = (data) =>
  game.clients.forEach((ws) => ws && ws.send(JSON.stringify(data)));

const sendToGame = (data) =>
  game.socket && game.socket.write(JSON.stringify(data));
const sendToClient = (data, ws) => ws.send(JSON.stringify(data));

const ss = net.createServer((socket) => {
  game.socket = socket;

  socket.on("error", (e) => {
    console.log(e);
    initGame();
  });

  socket.on("data", (data) => {
    data = JSON.parse(data);
    console.log(data);

    if (data) {
      switch (data.type) {
        case "game_start":
          game.running = true;
          broacastToClients(data);
        case "game_end":
          game.running = false;
          broacastToClients(data);
      }
    }
  });
});

ss.listen(8081);

const server = createServer({
  cert: readFileSync(
    "/etc/letsencrypt/live/guindaille-sim.duckdns.org/fullchain.pem"
  ),
  key: readFileSync(
    "/etc/letsencrypt/live/guindaille-sim.duckdns.org/privkey.pem"
  ),
});
const wss = new WebSocketServer({ server });

wss.on("connection", (ws) => {
  ws.on("error", console.error);

  if (game.players === 0) {
    ws.player = 0;
    game.players += 1;
    game.clients[0] = ws;
    const msg = {
      type: "player_connected",
      player: ws.player,
    };
    sendToGame(msg);
    sendToClient(msg, ws);
  } else if (game.players === 1) {
    ws.player = 1;
    game.players += 1;
    game.clients[0] = ws;
    const msg = {
      type: "player_connected",
      player: ws.player,
    };
    sendToGame(msg);
    sendToClient(msg, ws);
  } else {
    ws.send(
      JSON.stringify({
        type: "error",
        content: "full",
      })
    );
    ws.close();
  }

  ws.on("close", () => {
    game.players -= 1;
    game.clients[ws.player] = null;

    sendToGame({
      type: "player_disconnected",
      player: ws.player,
    });
  });

  ws.on("message", (data) => {
    console.log(`ws (${ws.player}): ${data}`);
    data = JSON.parse(data);
    if (data) {
      if (data.type === "mic_high") {
        sendToGame({
          type: "mic_high",
          player: ws.player,
        });
      }
    }
  });
});
