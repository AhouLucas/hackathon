let playing = false;
let player = -1;
const startBtn = document.getElementById("start-btn");

console.log(startBtn);

let ws = null;

startBtn.addEventListener("click", () => {
  ws = new WebSocket("ws://146.190.125.98:8080");

  ws.onopen = () => {
    console.log("Connected to ws!");
    document.getElementById("button-text").innerHTML = "Restart Game";
  };

  ws.onerror = (e) => {
    console.log(e);
    document.getElementById("log").innerHTML = "Connection Error";
  };

  ws.onmessage = (msg) => {
    msg = JSON.parse(msg.data);
    console.log(msg);

    switch (msg.type) {
      case "error": {
        if (msg.content === "full") {
          document.getElementById("log").innerHTML = "Game is full!";
        } else {
          document.getElementById("log").innerHTML = "Service Error";
        }
        break;
      }
      case "player_connected":
        document.getElementById("log").innerHTML = `Waiting for players...`;
        player = msg.player;
        break;
      case "game_start":
        document.getElementById(
          "log"
        ).innerHTML = `Game started!\nYou are player ${player + 1}.`;
        break;
      default:
        document.getElementById("log").innerHTML =
          "Unknown message from server!";
        break;
    }
  };
});

navigator.mediaDevices
  .getUserMedia({ video: false, audio: true })
  .then((stream) => {
    // Create and configure the audio pipeline
    const audioContext = new AudioContext();
    const analyzer = audioContext.createAnalyser();
    analyzer.fftSize = 512;
    analyzer.smoothingTimeConstant = 0.1;
    const sourceNode = audioContext.createMediaStreamSource(stream);
    sourceNode.connect(analyzer);

    // Analyze the sound
    setInterval(() => {
      // Compute the max volume level (-Infinity...0)
      const fftBins = new Float32Array(analyzer.frequencyBinCount); // Number of values manipulated for each sample
      analyzer.getFloatFrequencyData(fftBins);
      // audioPeakDB varies from -Infinity up to 0
      const audioPeakDB = Math.max(...fftBins);

      // Compute a wave (0...)
      const frequencyRangeData = new Uint8Array(analyzer.frequencyBinCount);
      analyzer.getByteFrequencyData(frequencyRangeData);
      const sum = frequencyRangeData.reduce((p, c) => p + c, 0);
      // audioMeter varies from 0 to 10
      const audioMeter = Math.sqrt(sum / frequencyRangeData.length);

      console.log(audioMeter);
      if (audioMeter > 8 && playing) {
        ws.send(
          JSON.stringify({
            type: "mic_high",
          })
        );
      }
    }, 100);
  })
  .catch((err) => {
    console.error(`you got an error: ${err}`);
  });
